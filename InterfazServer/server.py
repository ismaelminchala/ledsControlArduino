#! /usr/bin/env python2.7
#________________- Librerias Snap7-_______________________
import sys
sys.path.insert(0, "/home/pi/FreeOpcUa/python-opcua")
from opcua import S71200
import snap7
from snap7.util import *
import struct
import threading
import database 

#_______________- Librerias FreeOpcUa-____________________
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code

def embed(): 
    global connected
    vars = globals()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)           
    connected = True
    shell.interact()

def EstadoServidor():
    global connected
    return connected

from opcua import ua
from opcua.server import server

class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def data_change(self, handle, node, val, attr):
        print("Python: New data change event", handle, node, val, attr)

    def event(self, handle, event):
        print("Python: New event", handle, event)
        

class UaServer(object):
    
    def __init__(self):
        global connected        
        self.server = None
        connected = False
        self.idx = None
        self.objects = None
        self.conexionesPLC = []
        self.obj_id = []
        self._datachange_sub = None
        #self._event_sub = None
        self._subs_dc = {}
        self.IPs_PLC = []
        #self._subs_ev = {}
    
    def Conectar(self, ip, puerto):   
        self.server = server.Server()
        self.server.set_endpoint('opc.tcp://'+ip+':'+puerto+'/freeopcua/server/')        
        self.server.set_server_name("Server")
        # load server certificate and private key. This enables endpoints
        # with signing and encryption.
        #server.load_certificate("example-certificate.der")
        #server.load_private_key("example-private-key.pem")
        uri = "http://examples.freeopcua.github.io"
        self.idx = self.server.register_namespace(uri)

        self.objects = self.server.get_objects_node()

        #_____-Variables de prueba del Servidor
        myfolder = self.objects.add_folder(self.idx, "myEmptyFolder")
        myobj = self.objects.add_object(self.idx, "MyObject")
        self.CrearTag( myobj, 'Varible1', "" , 'var_prueba', 2, 'Int32')
        self.CrearTag( myobj, 'Arrary', "" , 'var_prueba', [6.7, 7.9], 'Double')

        myprop = myobj.add_property(self.idx, "myproperty", "I am a property")
        mymethod = myobj.add_method(self.idx, "mymethod", self.func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
        Multiplicacion_node = myobj.add_method(self.idx, "Multiplicacion", self.Multiplicacion, [ua.VariantType.Int64, ua.VariantType.Int64], [ua.VariantType.Int64])

        # import some nodes from xml
        #self.server.import_xml("custom_nodes.xml")

        # creating an event object
        # The event object automatically will have members for all events properties
        myevent = self.server.get_event_object(ua.ObjectIds.BaseEventType)
        myevent.Message.Text = "This is my event"
        myevent.Severity = 300        
        
        # starting!
        self.server.start()
        self.Objetos_id()
        try:
            embed()
        finally:
            self.disconnect()
    
    def disconnect(self):
        global connected
        if connected:
            database.BorrarBase()
            print("Servidor Desconectado")
            self._subs_dc = {}
            #self._subs_ev = {}
            connected = False
            self.server.stop()
            self.server = None
    
    def registroConexiones(self, handler):
        self.server.registroConexion(handler)
    
    #______Obtencion del nodo Raiz____________________________            
    def get_root_node_and_desc(self):       
        node = self.server.get_root_node()
        attrs = node.get_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId, ua.AttributeIds.NodeClass])
        desc = ua.ReferenceDescription()
        desc.DisplayName = attrs[0].Value.Value
        desc.BrowseName = attrs[1].Value.Value
        desc.NodeId = attrs[2].Value.Value
        desc.NodeClass = attrs[3].Value.Value
        desc.TypeDefinition = ua.TwoByteNodeId(ua.ObjectIds.FolderType)
        return node, desc

    #___---Funcion para obtener los nodos hijos de un nodo padre-    
    def get_children(self, node):
        descs = node.get_children_descriptions()
        children = []
        for desc in descs:
            children.append((self.server.get_node(desc.NodeId), desc))
        return children

    #___---Funcion Para obtener todos los atributos de un nodo dado-
    def get_all_attrs(self, node):
        names = []
        vals = []
        for name, val in ua.AttributeIds.__dict__.items():
            if not name.startswith("_"):
                names.append(name)
                vals.append(val)        
        attrs = node.get_attributes(vals)
        res = {}
        for idx, name in enumerate(names):
            if attrs[idx].StatusCode.is_good():
                temp = repr(attrs[idx].Value.Value)
                if '<' in temp:
                    res[name] = temp[temp.find(':')+1:-1]
                elif 'Id(i=' in temp:
                    id = temp[temp.find('Id(i=')+5 : temp.find(')')]
                    res[name] = self.Id_a_Nombre(int(id))
                else:
                    res[name] = attrs[idx].Value.Value
        return res
    
    def ConexionPLC(self, ip):
        return S71200.S71200(ip)
        
    def desc_nodo(self, node):
        return  node.get_description()   

    def listaTagObj(self, Obj):
        lista1 = []
        lista2 = []
        for node, attrs in self.get_children(Obj):
                des = str(self.desc_nodo(node))
                tagPLC = des[des.find('Tag:')+5 : des.find('-')]
                lista1.append(tagPLC)
                var = des[des.find('->')+3 : des.find(':)')-2]
                lista2.append(var)
        return lista1, lista2
    
    def listaIpPLC(self):
        lista = []
        for x in range(0, len(self.IPs_PLC)):
            lista.append(self.IPs_PLC[x][1])
        return lista
        
    def CrearTag(self, objeto, nombreTag, tagPLC, desc, val = 1, valTipo = None):        
        descripcion = 'Tag: '+ tagPLC + '-> '+ nombreTag + ': ' +desc        
        for x in range(0, len(self.conexionesPLC)):            
            if objeto in self.conexionesPLC[x]:  
                objeto = self.conexionesPLC[x][0]
                plc = self.conexionesPLC[x][1]
                val = self.obtener_valorPLC(plc, tagPLC)        
        if valTipo == 'SByte': valTipo = ua.VariantType.SByte
        elif valTipo == 'Int16': valTipo = ua.VariantType.Int16
        elif valTipo == 'Int32': valTipo = ua.VariantType.Int32
        elif valTipo == 'Int64': valTipo = ua.VariantType.Int64
        elif valTipo == 'UInt8': valTipo = ua.VariantType.UInt8
        elif valTipo == 'Char': valTipo = ua.VariantType.Char
        elif valTipo == 'Byte': valTipo = ua.VariantType.Byte
        elif valTipo == "UInt16":valTipo = ua.VariantType.UInt16
        elif valTipo == "UInt32": valTipo = ua.VariantType.UInt32
        elif valTipo == "UInt64": valTipo = ua.VariantType.UInt64
        elif valTipo == "Boolean": valTipo = ua.VariantType.Boolean
        elif valTipo == "Double": valTipo = ua.VariantType.Double
        elif valTipo == "Float": valTipo = ua.VariantType.Float
        elif valTipo == 'String': valTipo = ua.VariantType.String
        else: valTipo = ua.VariantType.DateTime            
        var = objeto.add_variable(self.idx, nombreTag, descripcion, ua.Variant(val, valTipo))
        idTag = str(var)
        idTag = idTag[idTag.find('i=')+2 : idTag.find(')')]
        idPlc = str(objeto)
        idPlc = idPlc[idPlc.find('i=')+2 : idPlc.find(')')]
        database.Crear_Tag(nombreTag, tagPLC, descripcion, valTipo, idPlc, idTag)
        var.set_writable()  
    
    def EliminarNodo(self, nodo):
        for x in range(0, len(self.IPs_PLC)):            
            if nodo in self.IPs_PLC[x]:
                n = self.IPs_PLC.pop(x)
        idObjeto = str(nodo)
        idObjeto= idObjeto[idObjeto.find('i=')+2 : idObjeto.find(')')]
        database.eliminarNodo(idObjeto)
        self.server.delete_nodes([nodo])
        
    def obtener_valorPLC(self, plc, tagPLC):
        temp =  plc.getMem(tagPLC)
        if tagPLC[1] == 'x': 
            if (temp == True):temp = "ON"
            else: temp = "OFF"
        elif tagPLC[1] == 'b': None
        else: None
        return temp
        
    def CrearObj(self, NomObj, ip = None, latencia = None, objeto = True, window = None):
        if objeto:
            plc = self.ConexionPLC(ip)
            obj = self.objects.add_object(self.idx, NomObj)
            self.IPs_PLC.append([obj, ip])
            idPlc = str(obj)
            idPlc = idPlc[idPlc.find('i=')+2 : idPlc.find(')')]
            database.Crear_Objeto(NomObj, ip, idPlc)
            _latencia = int(latencia)
            _latencia = _latencia/1000
        else: 
            plc = obj = None    
            folder = self.objects.add_folder(self.idx, NomObj)
        if [obj, plc] not in self.conexionesPLC and objeto:
            self.conexionesPLC.append([obj, plc])
            d = threading.Thread(target = self.actualizarVar_Obj, args=(obj, plc, ip, _latencia, window))
            d.setDaemon(True)
            d.start()

    def actualizarVar_Obj(self, Obj, plc, ip, latencia, window): 
        continuar = True        
        while continuar:
            try:
                valoresTag = []
                idPlc = str(Obj)
                idPlc = idPlc[idPlc.find('i=')+2 : idPlc.find(')')]
                for node, attrs in self.get_children(Obj):
                    des = str(self.desc_nodo(node))
                    tagPLC = des[des.find('Tag:')+5 : des.find('-')]
                    nombreTag = des[des.find('->')+3 : des.find(':)')-2]
                    val = self.obtener_valorPLC(plc, tagPLC)
                    database.Actualizar(idPlc, nombreTag, val)
                    node.set_value(val)
                    valoresTag.append(val)
                    
                time.sleep(latencia)
                i = 0
                   
                for node, attrs in self.get_children(Obj):
                    temp = node.get_value()
                    if valoresTag[i] != temp:
                        des = str(self.desc_nodo(node))
                        tagPLC = des[des.find('Tag:')+5 : des.find('-')]
                        if (temp.lower() == 'on'): temp = True
                        else: temp = False
                        plc.writeMem(tagPLC, temp)
                    i = i+1
                    
            except Exception as ex:
                if str(ex) == 'Objeto':
                    continuar = False                    
                    raise
                if 'Connection timed out' in str(ex):
                    window.senalPLC()
                    time.sleep(5)
        
    def setValorVar(self, node, val):
        node.set_value(val)
        
    def Objetos_id(self):        
        for name, val in ua.ObjectIds.__dict__.items():
            if not name.startswith("_"):
                self.obj_id.append([name, val]) 
    
    def Id_a_Nombre(self, id):
        for x in range(0, len(self.obj_id)):            
            if id in self.obj_id[x]:  
                Dato = self.obj_id[x][0]
                return Dato
            
    def subscribe_datachange(self, node, handler):
        if not self._datachange_sub:
            self._datachange_sub = self.server.create_subscription(500, handler)
        handle = self._datachange_sub.subscribe_data_change(node)
        self._subs_dc[node.nodeid] = handle
        return handle

    def unsubscribe_datachange(self, node):
        self._datachange_sub.unsubscribe(self._subs_dc[node.nodeid])
    
    def get_all_refs(self, node):
        return node.get_children_descriptions(refs=ua.ObjectIds.References)

    def func(self, parent, variant):
        ret = False
        if variant.Value % 2 == 0:
            ret = True
        return [ua.Variant(ret, ua.VariantType.Boolean)]

    def Multiplicacion(self, parent, x, y):
        print("Multiplicacion method call with parameters: ", x, y)
        return x * y
    
        

        
