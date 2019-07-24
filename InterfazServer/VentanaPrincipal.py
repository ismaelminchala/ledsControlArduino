#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#_________________-librerias para Pyinstaller--_________________
#from concurrent.futures import Future
#import trollius as asyncio
#import uuid
#import xml.etree.ElementTree as ET

from PyQt4 import uic
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, re
sys.path.insert(0, "/home/pi/FreeOpcUa/python-opcua")
import socket
import threading
import time
import datetime
import nmap
import sqlite3

import database 
from enum import Enum
from opcua import ua
from server import *


class V_principal(QMainWindow):
    def __init__(self):
        super(V_principal, self).__init__()
        uic.loadUi('./ArchivosUI/V_principal.ui',self)
        self.setWindowTitle("UNIVERSIDAD DE CUENCA - SERVIDOR")        
        #Fijar el tamano de la ventana
        #Tamano minimo
        self.setMinimumSize(750,500)
        #Fijar el tamano maximo
        self.setMaximumSize(750,500)  
        self.ip = None
        self.puerto = None
        
        #Funcion para centrar la ventana
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

        #Logo Universidad
        myPixmap = QPixmap('./Iconos/logo.jpg')
        myScaledPixmap = myPixmap.scaled(self.label.size(), Qt.KeepAspectRatio)
        self.label.setPixmap(myScaledPixmap)
        self.setWindowIcon(QIcon("./Iconos/network.svg"))

        #LLamados a funciones de edicion de texto
        self.lineEdit.textChanged.connect(self.validar_IP_servidor)
        self.timer = QBasicTimer()
        self.step = 0

        #Uso de Botones
        self.pushButton.clicked.connect(self.validar_IPs)
    
        #Instancia de las clases
        self._detIp = detIp()
    
        #Rellena Campos Vacios
        self.lineEdit.setText(self._detIp.ip())
        self.lineEdit_2.setText('4841')
                
    #Funciones validacion ingreso de datos
    def validar_IP_servidor(self):
        lineEdit = self.lineEdit.text()
        validar = re.match('^[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}$', lineEdit, re.I)
        if lineEdit == "":
            self.lineEdit.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.lineEdit.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.lineEdit.setStyleSheet("border: 1px solid green;")
            return True
    
    def timerEvent(self, event):
        #funcion asociada al timer.
        #Si el contador llega a 100
        #Se detiene el timer, se cambia el titulo
        #del boton, se coloca el contador en cero
        #y se sale de la funcion.
        #Si no llega a 100, se incrementa en 1 el contador y
        #se le asigna un nuevo valor a la barra de progreso.
        qfont = QFont("Arial",11, QFont.Bold)
        self.label_10.setFont(qfont)
        self.label_10.setText("Conectando...")
        self.step = self.step + 1
        self.progressBar.setValue(self.step)


        if EstadoServidor() == True:
            print 'Conectado'
            self.step = 100
            self.progressBar.setValue(self.step)
            self.label_10.setText("Conectado")
            self.step = 0
            self.timer.stop()            

        if self.step >= 99:            
            qfont = QFont("Arial",11, QFont.Bold)
            self.label_10.setFont(qfont)
            self.step=98

        if str(self.label_10.text()) == "Conectado":
            time.sleep(2)
            self.label_10.setText("Desconectado")
            windowP.setVisible(False)
            windowS.Actualizar(self.ip, self.puerto)
            windowS.setVisible(True)

    def Accion(self):
        d = threading.Thread(target = self.ActivarServidor)
        d.setDaemon(True)
        d.start()
        #Si el timer esta activo se detiene y se
        #le cambia el titulo al boton con Iniciar.
        if self.timer.isActive():
            self.timer.stop()
            self.step = 0
            #self.button.setText('Iniciar')
        else:
            #Si no esta activo el timer, se inicia con valor de 100
            #se coloca el titulo detener al boton.
            self.timer.start(50, self)
            #self.button.setText('Detener')
            
    #Evento de cierre de ventana
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir", "Seguro que desea salir del servidor", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:
            event.accept()
        else: event.ignore()


    #Validacion con Boton
    def validar_IPs(self):
        if self.validar_IP_servidor():
            self.Accion()
        else:
            qfont = QFont("Arial",11, QFont.Bold)
            self.label_10.setFont(qfont)
            self.label_10.setText("Desconectado")
            
    def ActivarServidor(self):
        self.ip = str(self.lineEdit.text())
        self.puerto = str(self.lineEdit_2.text())
        uaserver.Conectar(self.ip, self.puerto)
               

class detIp():
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
        self.local_ip_address = s.getsockname()[0]
        
    def ip(self):
        return self.local_ip_address

class IP_PLC():
    def __init__(self):
        self.nm = nmap
        
    def list_ipPLC(self, ip):
        a = nm.scan(hosts=ip, arguments='-sP')
        identificador = []
        i=0
        for k,v in a['scan'].iteritems():
            i=i+1
            try:
                ip=str(v['addresses']['ipv4'])
                mac=str(v['addresses']['mac'])
                if '01:BD' in mac:
                    identificador.append(ip)
            except:
                None
        return identificador
        
class V_secundaria(QMainWindow):
    def __init__(self):
        super(V_secundaria, self).__init__()
        uic.loadUi('./ArchivosUI/V_secundaria.ui',self)
        self.setWindowTitle("UNIVERSIDAD DE CUENCA - SERVIDOR OPCUA")
        #Fijar el tamano de la ventana
        self.setMinimumSize(750,500)
        self.setMaximumSize(900,550)
        self.setWindowIcon(QIcon("./Iconos/network.svg"))
        
        self.ipServer = None
        self._IpPLC = IP_PLC()
        
        #Funcion para centrar la ventana
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

        self.tree_ui = TreeUI(self, uaserver)
        self.attrs_ui = AttrsUI(self, uaserver)          
        self.refs_ui = RefsUI(self, uaserver)
        self.datachange_ui = DataChangeUI(self, uaserver)
        self.conexion_ui = conexionUI(self, uaserver)
        
        self.windowCrearTag = V_crearTag(self, uaserver)
        self.windowObj = V_crearObj(self, uaserver)        
        self.windowEliminarTag = V_eliminarTag(self, uaserver)
        self.windowHistorial = V_historial(self, uaserver)
        self.CrearTablas()
        
        # populate contextual menu
        self.crearTag = QAction("&Crear Etiqueta/Variable", self.tree_ui.model)
        self.crearTag.triggered.connect(self._crearTag)
        self.historial = QAction("&Mostrar Historial", self.tree_ui.model)
        self.historial.triggered.connect(self._historial)
        self.valorTag = QAction("&Cambiar valor de la Etiqueta/Variable", self.tree_ui.model)
        self.valorTag.triggered.connect(self._valorTag)
        self.eliminarTag = QAction("&Eliminar Etiqueta/Variable", self.tree_ui.model)
        self.eliminarTag.triggered.connect(self.EliminarNodo)
        self.crearCarp = QAction("&Crear Nueva Carpeta", self.tree_ui.model)
        self.crearCarp.triggered.connect(self.V_crearCarp)
        self.crearObj = QAction("&Crear Nuevo Objeto", self.tree_ui.model)
        self.crearObj.triggered.connect(self.V_crearObj)
        self.EliminarObj = QAction("&Eliminar Objeto/Carpeta", self.tree_ui.model)
        self.EliminarObj.triggered.connect(self.EliminarNodo)
        self.suscNodo = QAction("&Suscribirse a Cambios", self.tree_ui.model)
        self.suscNodo.triggered.connect(self.suscripcionNodo)
        self.eliminarSuscNodo = QAction("&Quitar Suscripcion a Cambios", self.tree_ui.model)
        self.eliminarSuscNodo.triggered.connect(self.quitar_suscripcion)
        
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        
        self.timer = QBasicTimer()
        self.step = 0
        self._list_ip = False
    
    def showContextMenu(self, position):        
        idx = self.treeView.currentIndex()              
        nodoSeleccionado = self.tree_ui.model.itemFromIndex(idx)
        nodo = uaserver.desc_nodo(nodoSeleccionado.data().toPyObject())
        contextMenu = QMenu()
                     
        if nodoSeleccionado.text() == 'Root': None
        elif nodoSeleccionado.text() == 'Types': None 
        elif nodoSeleccionado.text() == 'Views': None 
        elif nodoSeleccionado.text() == 'Server': None
        elif nodoSeleccionado.text() == 'Objects': 
            contextMenu.addAction(self.crearObj)
            contextMenu.addAction(self.crearCarp)
            contextMenu.addAction(self.EliminarObj)
        else:    
            if 'Objeto' in str(nodo):        
                contextMenu.addAction(self.crearTag) 
                contextMenu.addAction(self.eliminarTag)
            elif 'Carpeta' in str(nodo):
                contextMenu.addAction(self.crearTag)
                contextMenu.addAction(self.eliminarTag)  
            else: 
                contextMenu.addAction(self.valorTag)
                contextMenu.addAction(self.suscNodo)  
                contextMenu.addAction(self.eliminarSuscNodo)
                contextMenu.addAction(self.historial) 
        contextMenu.exec_(self.treeView.mapToGlobal(position))
        
    def show_error(self, msg, level=1):
        self.statusBar.show()
        self.statusBar.setStyleSheet("QStatusBar { background-color : orange; color : black; }")
        self.statusBar.showMessage(str(msg))
        QTimer.singleShot(2500, self.statusBar.hide)
        
    def Actualizar(self, ip, puerto):
        self.ipServer = ip
        self.tree_ui.start()
        self.conexion_ui.start()
        endpoint = 'opc.tcp://'+ip+':'+puerto+'/freeopcua/server/'
        self.txtIpServidor.setText(endpoint)
        
        
    def get_current_node(self, idx=None):
        if idx is None:
            idx = self.treeView.currentIndex()
        return self.tree_ui.get_current_node(idx)
    
    def _crearTag(self):
        self.windowCrearTag._crearT = True        
        self.windowCrearTag.setWindowTitle("SERVIDOR OPCUA - CREAR ETIQUETA")
        self.windowCrearTag.txtNombre.setEnabled(True)
        self.windowCrearTag.txtDireccion.setEnabled(True)
        self.windowCrearTag.btComboBox.setEnabled(True)
        self.windowCrearTag.txtDescripcion.setEnabled(True)
        self.windowCrearTag.exec_()

    def _historial(self):       
        self.windowHistorial.Seleccionar()
        self.windowHistorial.exec_()

    def _valorTag(self):
        self.windowCrearTag._crearT = False
        self.windowCrearTag.setWindowTitle("SERVIDOR OPCUA - CAMBIAR VALOR DE LA ETIQUETA")
        self.windowCrearTag.txtNombre.setEnabled(False)
        self.windowCrearTag.txtDireccion.setEnabled(False)
        self.windowCrearTag.btComboBox.setEnabled(False)
        self.windowCrearTag.txtDescripcion.setEnabled(False)
        self.windowCrearTag.exec_()
        
    def V_crearObj(self): 
        d = threading.Thread(target = self.cargarPLC_Red)
        d.setDaemon(True)
        d.start()
        if self.timer.isActive():
            self.timer.stop()
            self.step = 0
        else:
            self.timer.start(50, self)        
        self.windowObj.setWindowTitle("SERVIDOR OPCUA - CREAR NUEVO OBJETO")
        self.windowObj.obj = True
        self.windowObj.txtlatencia.setEnabled(True)
        self.windowObj.setEnabled(False)
        self.windowObj.exec_()  
        
    def cargarPLC_Red(self):
        i = self.ipServer.split('.')
        rangoIp = i[0]+'.'+i[1]+'.'+i[2]+'.1/24'
        list_ip = self._IpPLC.list_ipPLC(rangoIp)
        self._list_ip = True
        self.windowObj.llenarComboBox(list_ip)        
        self.windowObj.btComboBox.setEnabled(True)        
        
    def timerEvent(self, event):
        self.step = self.step + 1
        self.windowObj.progressBar.setValue(self.step)

        if self._list_ip:
            self.step=100
            self.windowObj.progressBar.setValue(self.step)
            self.timer.stop()
            self.step = 0
            self._list_ip = False
            self.windowObj.setEnabled(True)

        if self.step >= 99:
            self.step=98
        
    def V_crearCarp(self):
        self.windowObj.setWindowTitle("SERVIDOR OPCUA - CREAR NUEVA CARPETA")
        self.windowObj.obj = False
        self.windowObj.btComboBox.setEnabled(False)
        self.windowObj.txtlatencia.setEnabled(False)
        self.windowObj.exec_()
                
    def EliminarNodo(self):        
        self.windowEliminarTag.Actualizar()
        self.windowEliminarTag.exec_()
    
    def suscripcionNodo(self):
        self.datachange_ui._subscribe()
        self.tabWidget.setCurrentIndex(1)
      
    def quitar_suscripcion(self):
        self.datachange_ui._unsubscribe()  
        
    def Desconectar(self):
        resultado = QMessageBox.question(self, "Salir", "Seguro que desea salir del servidor", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: 
            try:
                uaserver.disconnect()
                self.tree_ui.clear()
                self.refs_ui.clear()
                self.attrs_ui.clear()
                self.datachange_ui.clear()
                #self.event_ui.clear()
                windowS.setVisible(False)
                windowP.setVisible(True)
            except Exception as ex:
                self.show_error(ex)
                raise
        else: None
        
    def senalPLC(self):
        signal = SIGNAL("signal")
        self.connect(self, signal, self.show_error)
        self.emit(signal, "Plc deconectado")       
                   
    def closeEvent(self, event):
        resultado = QMessageBox.question(self, "Salir", "Seguro que desea salir del servidor", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes:
            #database.BorrarBase()
            event.accept()
        else: event.ignore()

    def CrearTablas(self):
        #Conectar a la base de datos
        conexion = sqlite3.connect("database.db")
        #Seleccionar el cursor para realizar la consulta
        consulta = conexion.cursor()

        #Una vez que tenemos los modelos, podemos pasar a crear las tablas:
        #String con la consulta para crear la tabla
        sql = """CREATE TABLE IF NOT EXISTS PLC(
        plc_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombrePLC VARCHAR(10) NOT NULL,
        idPLC VARCHAR(20) NOT NULL,
        IpPLC VARCHAR(20) NOT NULL,
        idUlt INT(100000) NOT NULL,
        fecha_plc DATE NOT NULL)"""
        #Ejecutamos la consulta
        consulta.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Tags(
        tag_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombreTag VARCHAR(10) NOT NULL,
        tagPLC VARCHAR (10) NOT NULL,
        descripcion BLOB,
        tipo VARCHAR(10) NOT NULL,
        fecha_creacion TIME NOT NULL,
        idServidor INT(100000) NOT NULL,
        plc_ids INTEGER NOT NULL, FOREIGN KEY (plc_ids) REFERENCES PLC(plc_id))"""
        #Ejecutamos la consulta
        consulta.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS Registro(
        registro_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        valor VARCHAR(5) NOT NULL,
        nombreTag VARCHAR (10) NOT NULL,
        fecha_Registro DATE NOT NULL,
        hora TIME NOT NULL,
        tag_id VARCHAR(10) NOT NULL,
        tag_ids INTEGER NOT NULL, FOREIGN KEY (tag_ids) REFERENCES Tags(tag_id))"""
        #Ejecutamos la consulta
        consulta.execute(sql)

        #Cerramos la consulta
        consulta.close()
        #Guardamos los cambio
        conexion.commit()
        #Cerramos la conexión
        conexion.close()

class TreeUI(object):

    def __init__(self, window, uaserver):
        self.window = window
        self.uaserver = uaserver
        self.model = TreeViewModel(self.uaserver)
        self.model.clear()  # FIXME: do we need this?
        self.model.error.connect(self.window.show_error)
        self.window.treeView.setModel(self.model)
        self.window.treeView.setUniformRowHeights(True)
        self.window.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.window.treeView.header().setDefaultSectionSize(180)
                     
    def clear(self):
        self.model.clear()

    def start(self):
        self.model.clear()
        self.model.add_item(*self.uaserver.get_root_node_and_desc())

    def get_current_node(self, idx):
        idx = idx.sibling(idx.row(), 0)
        it = self.model.itemFromIndex(idx)
        if not it:
            return None
        node = it.data()
        if not node:
            print("No node for item:", it, it.text())
            return None
        node.display_name = it.text()  # FIXME: hack
        return node 
    
class TreeViewModel(QStandardItemModel):
    error = pyqtSignal(str)

    def __init__(self, uaserver):
        super(TreeViewModel, self).__init__()
        self.uaserver = uaserver
        self._fetched = []

    def clear(self):
        QStandardItemModel.clear(self)
        self._fetched = []
        self.setHorizontalHeaderLabels(['DisplayName', 'BrowseName', 'NodeId'])

    def add_item(self, node, desc, parent=None):
        data = [QStandardItem(desc.DisplayName.to_string()), QStandardItem(desc.BrowseName.to_string()), QStandardItem(desc.NodeId.to_string())]
        if desc.NodeClass == ua.NodeClass.Object:
            if desc.TypeDefinition == ua.TwoByteNodeId(ua.ObjectIds.FolderType):
                data[0].setIcon(QIcon(QPixmap('./Iconos/folder.png')))
            else:
                data[0].setIcon(QIcon("./Iconos/object.png"))
        elif desc.NodeClass == ua.NodeClass.Variable:
            if desc.TypeDefinition == ua.TwoByteNodeId(ua.ObjectIds.PropertyType):
                data[0].setIcon(QIcon("./Iconos/property.png"))
            else:
                data[0].setIcon(QIcon("./Iconos/variable.jpg"))
        elif desc.NodeClass == ua.NodeClass.Method:
                data[0].setIcon(QIcon("./Iconos/method.png"))        
        data[0].setData(node)        
        if parent:
            parent.appendRow(data)
        else:
            self.appendRow(data)
       
    def canFetchMore(self, idx):
        item = self.itemFromIndex(idx)
        if not item:
            return True
        node = item.data()       
        if node not in self._fetched:
            self._fetched.append(node)
            return True
        return False

    def hasChildren(self, idx):
        item = self.itemFromIndex(idx)
        if not item:
            return True
        node = item.data()
        if node in self._fetched:
            return QStandardItemModel.hasChildren(self, idx)
        return True

    def fetchMore(self, idx):
        parent = self.itemFromIndex(idx)
        if parent:
            self._fetchMore(parent)

    def _fetchMore(self, parent): 
        try:
            for node, attrs in self.uaserver.get_children(parent.data().toPyObject()):
                self.add_item(node, attrs, parent)
        except Exception as ex:
            self.error.emit(ex)
            raise
        
    def borrarTreeModel(self, idx, parent):
        self.canFetchMore(idx)
        for x in range(0, parent.rowCount()):
            parent.removeRow(0)   
        
    def crearVar(self,idx, NomVar, tagPLC, desc, val, valTipo):
        parent = self.itemFromIndex(idx)
        list1, list2 = self.uaserver.listaTagObj(parent.data().toPyObject())
        if tagPLC[1].isdigit():
            tagPLC   =  tagPLC[:1] + 'x' + tagPLC[1:]
        if tagPLC in list1 or NomVar in list2:
            return False                
        try:
            if val == '': val = 1
            self.uaserver.CrearTag(parent.data().toPyObject(), NomVar, tagPLC, desc, val, valTipo)
            self.borrarTreeModel(idx, parent)
            self._fetchMore(parent)
            return True
        except Exception as ex:
            return False         
        
    def eliminarVar(self, idx, var):
        parent = self.itemFromIndex(idx)
        try:
            self.uaserver.EliminarNodo(var)
            self.borrarTreeModel(idx, parent) 
            self._fetchMore(parent)
            return True
        except Exception as ex:
            return False   

    def crearObj(self, idx, NomObj, IpPLC, latencia, obj, window):
        parent = self.itemFromIndex(idx)
        if IpPLC in self.uaserver.listaIpPLC():
            return False 
        try:            
            self.uaserver.CrearObj(NomObj, IpPLC, latencia, obj, window) 
            self.borrarTreeModel(idx, parent)
            self._fetchMore(parent)
            return True
        except Exception as ex:
            return False

    def history(self, idx):
        parent = self.itemFromIndex(idx)
        return parent
        
        
class AttrsUI(object):
    def __init__(self, window, uaserver):
        self.window = window
        self.uaserver = uaserver
        self.model = QStandardItemModel()
        self.window.attrView.setModel(self.model)
        self.window.attrView.header().setDefaultSectionSize(150)        
       
        self.window.treeView.clicked.connect(self.show_attrs)
                
        # Context menu
        copyaction = QAction("&Copy Value", self.model)
        copyaction.triggered.connect(self._copy_value)
        self.window.attrView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.attrView.customContextMenuRequested.connect(self.showContextMenu)
        self._contextMenu = QMenu()
        self._contextMenu.addAction(copyaction)   
   
    def showContextMenu(self, position):
        item = self.get_current_item()
        if item:
            self._contextMenu.exec_(self.window.attrView.mapToGlobal(position))

    def get_current_item(self, col_idx=0):
        idx = self.window.attrView.currentIndex()
        return self.model.item(idx.row(), col_idx)

    def _copy_value(self, position):
        it = self.get_current_item(1)
        if it:
            QApplication.clipboard().setText(it.text())

    def clear(self):
        self.model.clear()

    def show_attrs(self, idx):
        if not isinstance(idx, QModelIndex):
            idx = None
        node = self.window.get_current_node(idx).toPyObject()        
        if node:  
            self._show_attrs(node) 

    def _show_attrs(self, node):
        try:
            attrs = self.uaserver.get_all_attrs(node) 
        except Exception as ex:
            self.window.show_error(ex)
            raise
            
        self.model.clear()    
        self.model.setHorizontalHeaderLabels(['Attribute', 'Value'])
        for k, v in attrs.items():
            if isinstance(v, (ua.NodeId)):
                v = str(v)
            elif isinstance(v, (ua.QualifiedName, ua.LocalizedText)):
                v = v.to_string()
            elif isinstance(v, Enum):
                v = repr(v)
            elif isinstance(v, ua.DataValue):
                v = repr(v)
            else:
                v = str(v)    
            self.model.appendRow([QStandardItem(k), QStandardItem(v)]) 
            
    def ActualizarVarTag(self,idx, val):
        try:
            node = self.window.get_current_node(idx).toPyObject()
            self.uaserver.setValorVar(node, val)
            self.clear()
            self._show_attrs(node)
            return True
        except Exception as ex:
            return False

class RefsUI(object):
    def __init__(self, window, uaserver):
        self.window = window
        self.uaserver = uaserver
        self.model = QStandardItemModel()
        self.window.refView.setModel(self.model)

        self.window.treeView.activated.connect(self.show_refs)
        self.window.treeView.clicked.connect(self.show_refs)

    def clear(self):
        self.model.clear()

    def show_refs(self, idx):
        node = self.window.get_current_node(idx)
        self.model.clear()
        if node:
            self._show_refs(node)

    def _show_refs(self, node):
        self.model.setHorizontalHeaderLabels(['ReferenceType', 'NodeId', "BrowseName", "TypeDefinition"])
        try:
            refs = self.uaserver.get_all_refs(node.toPyObject())
        except Exception as ex:
            self.window.show_error(ex)
            raise
        for ref in refs:
            self.model.appendRow([QStandardItem(str(ref.ReferenceTypeId)),
                                  QStandardItem(str(ref.NodeId)),
                                  QStandardItem(str(ref.BrowseName)),
                                  QStandardItem(str(ref.TypeDefinition))])
        
class DataChangeHandler(QObject):
    data_change_fired = pyqtSignal(object, str, str)

    def datachange_notification(self, node, val, data):
        dato = datetime.datetime.now().isoformat()
        self.data_change_fired.emit(node, str(val), dato)

class DataChangeUI(object):

    def __init__(self, window, uaserver):
        self.window = window
        self.uaserver = uaserver
        self._subhandler = DataChangeHandler()
        self._subscribed_nodes = []
        self.model = QStandardItemModel()
        self.window.subView.setModel(self.model)
        self._subhandler.data_change_fired.connect(self._update_subscription_model)

    def clear(self):
        self._subscribed_nodes = []
        self.model.clear()

    def _subscribe(self):
        node = self.window.get_current_node()
        if node is None: return
        if node.toPyObject() in self._subscribed_nodes:
            self.window.show_error("Suscripcion ya realizada: ", node.toPyObject())
            return
        self.model.setHorizontalHeaderLabels(["DisplayName", "Valor", "Horalocal"])
        try:
            row = [QStandardItem(node.display_name), QStandardItem("Sin Datos Todavia"), QStandardItem("")]
            row[0].setData(node)
            self.model.appendRow(row)
            self._subscribed_nodes.append(node.toPyObject())        
            self.uaserver.subscribe_datachange(node.toPyObject(), self._subhandler)
        except Exception as ex:
            self.window.show_error("No se puede Crear la Suscripcion")
            
    def _unsubscribe(self, node = None):
        if node == None:
            node = self.window.get_current_node().toPyObject()
        if node is None: return
        if node in self._subscribed_nodes:
            self.uaserver.unsubscribe_datachange(node)
            self._subscribed_nodes.remove(node)
            i = 0
            while self.model.item(i):
                item = self.model.item(i)
                if item.data().toPyObject() == node:
                    self.model.removeRow(i)
                i += 1
        else: self.window.show_error("El %s no esta suscrito " % node)

    def _update_subscription_model(self, node, value, timestamp):
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            if item.data().toPyObject() == node:
                it = self.model.item(i, 1)
                it.setText(value)
                it_ts = self.model.item(i, 2)
                it_ts.setText(timestamp)
            i += 1

class conexionHandler(QObject):
    data = pyqtSignal(str)
    
    def data_notification(self, conexion):
        self.data.emit(conexion)

class conexionUI(object):
    def __init__(self, window, uaserver):
        self.window = window
        self.uaserver = uaserver
        self._subhandler = conexionHandler()
        self.model = QStandardItemModel()
        self.window.conView.setModel(self.model)
        self._subhandler.data.connect(self.Conexiones)        
    
    def start(self):
        self.uaserver.registroConexiones(self._subhandler)
        self.model.setHorizontalHeaderLabels(["Sesion", "Cliente", 'Puerto', "Estatus"])
        
    def Conexiones(self, conexion):
        c = str(conexion)
        self.model.setHorizontalHeaderLabels(["Sesion", "Cliente", 'Puerto', "Estatus"])
        try:
            ip = c[c.find("(")+2 : c.find(",")-1]
            puerto = c[c.find(", ")+1 : c.find(")")]
            user = c[c.find("User")+5 :]
            puerto = c[c.find(",")+1 : c.find(")")]
            row = [ QStandardItem(user), QStandardItem(ip), QStandardItem(puerto), QStandardItem("Estatus")]
            self.model.appendRow(row)
        except Exception as ex:
            self.window.show_error("Error en el registro de Conexiones")

class V_crearTag(QDialog):
    def __init__(self, window, uaserver):
        super(V_crearTag,  self).__init__(window)
        uic.loadUi('./ArchivosUI/V_AgregarTag.ui',self)
        self.window = window
        self.uaserver = uaserver
        self._crearT = None
        self.validarTag = None
        
        self.txtNombre.textChanged.connect(self.validar_PLC_Nombre)
        self.txtDireccion.textChanged.connect(self.validar_Tag_PLC)
        self.txtDescripcion.textChanged.connect(self.validar_Descripcion_PLC)
        
        self.tipoDatos1 = ["Boolean"]
        self.tipoDatos2 = ['Byte', 'Char','UInt8', 'SByte']
        self.tipoDatos3 = ['Int16', 'Int32', 'Int64', "UInt16", "UInt32", "UInt64"]
        self.tipoDatos4 = ['DateTime', "Double", "Float", 'String']
         
    def llenarComboBox(self, lista):
        for x in range(0, self.btComboBox.count()):
            self.btComboBox.removeItem(0) 
        self.btComboBox.insertItems(0, lista)
        
    def validar_PLC_Nombre(self):
        txtNombre = self.txtNombre.text()
        validar = re.match('^[a-zA-Z0-9]{1,10}$', txtNombre, re.I)
        if txtNombre == "":
            self.txtNombre.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.txtNombre.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.txtNombre.setStyleSheet("border: 1px solid green;")
            return True

    def validar_Descripcion_PLC(self):
        txtDescripcion = self.txtDescripcion.text()
        validar = re.match('^[a-zA-Z0-9]{0,50}$', txtDescripcion, re.I)
        if txtDescripcion == "":
            self.txtDescripcion.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.txtDescripcion.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.txtDescripcion.setStyleSheet("border: 1px solid green;")
            return True

    def validar_Tag_PLC(self):
        txtDireccion = self.txtDireccion.text()
        validar1 = re.match('^[M,Q,I]{1}[0-9]{1,4}[.][0-7]{1}$', txtDireccion, re.I)
        validar2 = re.match('^[F]{1}[R]{1}[E]{1}[A]{1}[L]{1}[0-9]{1,3}$', txtDireccion, re.I)
        validar3 = re.match('^[M,Q,I]{1}[D,W,B]{1}[0-9]{1,4}$', txtDireccion, re.I)
        if txtDireccion == "":
            self.txtDireccion.setStyleSheet("border: 1px solid yellow;")
            self.validarTag = False
        elif validar1 or validar2 or validar3:
            self.txtDireccion.setStyleSheet("border: 1px solid green;")
            temp = str(txtDireccion)[1]
            if temp.lower() == 'b': self.llenarComboBox(self.tipoDatos2)
            elif temp.lower() == 'w':self.llenarComboBox(self.tipoDatos3)
            elif temp.lower() == 'd':self.llenarComboBox(self.tipoDatos4)
            elif temp.lower() == 'r':self.llenarComboBox(self.tipoDatos4)
            else:self.llenarComboBox(self.tipoDatos1)
            self.validarTag = True        
        else:
            self.txtDireccion.setStyleSheet("border: 1px solid red;")            
            self.validarTag = False   
    
    def Aceptar(self):
        if self._crearT:
            if self.validarTag and self.validar_PLC_Nombre() :
                NomVar = str(self.txtNombre.text())
                desc = str(self.txtDescripcion.text())
                tagPLC = str(self.txtDireccion.text())
                val = str(self.txtValor.text())
                valTipo = str(self.btComboBox.currentText())
                idx = self.window.treeView.currentIndex()
                if self.window.tree_ui.model.crearVar(idx, NomVar, tagPLC, desc, val, valTipo):
                    self.txtNombre.setText("")
                    self.txtDireccion.setText("")
                    self.txtDescripcion.setText("")
                    self.txtValor.setText('')
                    self.close()
                else:
                    QMessageBox.warning(self, "Ingreso Incorrecto", "Tag ya existente o no se puede crear la Tag", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Ingreso Incorrecto", "Ingreso incorrecto de datos", QMessageBox.Ok)
        else:
            val = str(self.txtValor.text())
            idx = self.window.treeView.currentIndex()
            if self.window.attrs_ui.ActualizarVarTag(idx, val):
                self.txtValor.setText('')
                self.close()
            else:
                QMessageBox.warning(self, "Ingreso Incorrecto", "No se puede cambiar el valor de la Tag", QMessageBox.Ok)
                        
    def cerrar(self):
        self.txtNombre.setText("")
        self.txtDireccion.setText("")
        self.txtDescripcion.setText("")
        self.txtValor.setText('')
        self.close()
        
class V_eliminarTag(QDialog):    
    def __init__(self, window, uaserver):
        super(V_eliminarTag,  self).__init__(window)
        uic.loadUi('./ArchivosUI/V_EliminarTag.ui',self) 
        self.window = window
        self.uaserver = uaserver
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model) 
        self.treeView.header().setDefaultSectionSize(120) 
        self.parent = None
        
    def Actualizar(self):
        idx = self.window.treeView.currentIndex()
        self.parent = self.window.tree_ui.model.itemFromIndex(idx)
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['DisplayName', 'BrowseName', 'NodeId'])
        try:
            for node, attrs in self.uaserver.get_children(self.parent.data().toPyObject()):
                if attrs.DisplayName.to_string() != 'Server':
                    self.add_item(node, attrs, self.parent)
        except Exception as ex:
            self.window.show_error(ex)
            raise 
    
    def add_item(self, node, desc, parent=None):
        data = [QStandardItem(desc.DisplayName.to_string()), QStandardItem(desc.BrowseName.to_string()), QStandardItem(desc.NodeId.to_string())]        
        data[0].setData(node)
        data[0].setIcon(QIcon("./Iconos/variable.jpg"))
        self.model.appendRow(data)
        
    def Eliminar(self):
        idx = self.treeView.currentIndex()
        idx_parent = self.window.treeView.currentIndex()
        variable = self.model.itemFromIndex(idx) 
        if variable == None:
            return
        resultado = QMessageBox.question(self, "Eliminar", "Seguro que desea eliminar nodo seleccionado?", QMessageBox.Yes | QMessageBox.No)
        try:
            if resultado == QMessageBox.Yes:
                variable = variable.data().toPyObject()
                nodo = str(self.uaserver.desc_nodo(variable))
                if 'Objeto' or 'Carpeta' in nodo:
                    for node, attrs in self.uaserver.get_children(variable):
                        if node in self.window.datachange_ui._subscribed_nodes:
                            self.window.datachange_ui._unsubscribe(node)
                if variable in self.window.datachange_ui._subscribed_nodes:
                    self.window.datachange_ui._unsubscribe(variable)                   
                if not self.window.tree_ui.model.eliminarVar(idx_parent, variable):
                    QMessageBox.warning(self, "Ingreso Incorrecto", "No se puede borrar la varible", QMessageBox.Ok)
                self.Actualizar()
        except Exception as ex:
            QMessageBox.warning(self, "Error", "No se puede borrar la varible", QMessageBox.Ok)
        
    def Cerrar(self):
        self.close()
        
class V_crearObj(QDialog):
    def __init__(self, window, uaserver):
        super(V_crearObj,  self).__init__(window)
        uic.loadUi('./ArchivosUI/V_AgregarObj.ui',self)
        self.window = window
        self.uaserver = uaserver
        self.obj = None
        self.txtlatencia.textChanged.connect(self.validar_IntLatencia)
        
    def validar_IntLatencia(self):
        latencia = self.txtlatencia.text()
        validar = re.match('^[0-9]{1,10}$', latencia, re.I)
        if latencia == "":
            self.txtlatencia.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.txtlatencia.setStyleSheet("border: 1px solid red;")
            return False
        else:
            val = int(latencia)
            if val >= 500:
                self.txtlatencia.setStyleSheet("border: 1px solid green;")
                return True
            else:
                return False
    
    def llenarComboBox(self, lista):
        for x in range(0, self.btComboBox.count()):
            self.btComboBox.removeItem(0) 
        self.btComboBox.insertItems(0, lista)
        
    def Aceptar(self):
        NomObj = str(self.txtObjeto.text())
        IpPLC = str(self.btComboBox.currentText())
        latencia = str(self.txtlatencia.text())
        idx = self.window.treeView.currentIndex()
        if self.obj:
            if self.validar_IntLatencia():
                if self.window.tree_ui.model.crearObj(idx, NomObj, IpPLC, latencia, self.obj, self.window):
                    self.txtObjeto.setText("")
                    self.txtlatencia.setText("")
                    self.close()
                else:
                    QMessageBox.warning(self, "Ingreso Incorrecto", "No Se Puede Crear el Objeto, revise los datos Ingresados", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Ingreso Incorrecto", "Revise los datos Ingresados", QMessageBox.Ok)
        else:
            if self.window.tree_ui.model.crearObj(idx, NomObj, IpPLC, latencia, self.obj, self.window):
                self.txtObjeto.setText("")
                self.close()
            else:
                QMessageBox.warning(self, "Ingreso Incorrecto", "No Se Puede Crear la Carpeta", QMessageBox.Ok)
                  
    def cerrar(self):
        self.close()

class V_historial(QDialog):
    def __init__(self, window, uaserver, parent=None):
        super(V_historial,  self).__init__(window)
        self.window = window
        self.uaserver = uaserver
        self.model = QStandardItemModel()
        self.setWindowTitle("SERVIDOR OPCUA - HISTORIAL")
        self.resize(600, 450) #Tamaño inicial
        self.setMaximumSize(800,600)
        self.layout = QGridLayout() #Crear un layout grid
        self.setLayout(self.layout) #Agregar el layout al cuadro de diálogo
        self.table = QTableWidget() #Crear la tabla
        #Define el calendario en una ventana
        self.cal = QtGui.QCalendarWidget(self)
        #Se define una cuadricula al calendario
        self.cal.setGridVisible(True)
        #Se define una etiqueta donde se mostrara la fecha seleccionada
        self.etiqueta = QtGui.QLabel(self)
        #Se define como empaquetar los widgets.
        #En este caso se usa grilla.
        #Se crea la instancia
        self.layout.setSpacing(25)
        self.layout.setColumnStretch(1, 500)
        self.layout.setColumnMinimumWidth(1, 400)
        self.table.clear()
        self.layout.addWidget(self.table, 1, 1) #Agregar la tabla al layout
        self.layout.addWidget(self.cal, 1, 0) #Agregar el calendario al layout
        self.layout.addWidget(self.etiqueta, 2, 0) #Agregar la etiqueta al layout
        self.table.setColumnCount(4)
        
    def Seleccionar(self):
        self.table.clear()
        #Se captura la fecha y se muestra en la etiqueta
        self.fecha = self.cal.selectedDate()
        self.etiqueta.setText(str(self.fecha.toPyDate()))
        self.etiqueta.setAlignment(QtCore.Qt.AlignCenter)
        self.connect(self.cal, QtCore.SIGNAL('selectionChanged()'),
            self.mostrarFecha)

    def mostrarFecha(self):
        self.table.clear()
        self.fecha = self.cal.selectedDate()
        self.etiqueta.setText(str(self.fecha.toPyDate()))    
        self.table.setHorizontalHeaderLabels(['VALOR', 'NOMBRE', 'HORA', 'ID PLC'])
        self.fecha = self.cal.selectedDate()
        self.etiqueta.setText(str(self.fecha.toPyDate()))
        fecha = str(self.fecha.toPyDate())
        i=0
        idx = self.window.treeView.currentIndex()
        parent = self.window.tree_ui.model.history(idx)
        idVar = str(parent.data().toPyObject())
        idVar = idVar[idVar.find('i=')+2 : idVar.find(')')]
        idVar = int(idVar)
        conexion = sqlite3.connect("database.db")
        consulta = conexion.cursor()
        #Extrayendo todas las filas
        sql = "SELECT * FROM Registro WHERE fecha_Registro ='%s' and  tag_id = %s" %(fecha, idVar)
        consulta.execute(sql)
        filas = consulta.fetchall()
        for fila in filas:
            self.table.insertRow(i)
            valor = QTableWidgetItem(str(fila[1]))
            nombre = QTableWidgetItem(str(fila[2]))
            hora = QTableWidgetItem(str(fila[4]))
            id_tags = QTableWidgetItem(str(fila[6]))
            self.table.setItem(i, 0, valor)
            self.table.setItem(i, 1, nombre)
            self.table.setItem(i, 2, hora)
            self.table.setItem(i, 3, id_tags)
            i=i+1
        consulta.close()
        conexion.commit()
        conexion.close()
        
    
if __name__ == '__main__':    
    app = QApplication(sys.argv)    
    uaserver = UaServer()
    nm = nmap.PortScanner()
    windowP = V_principal()
    windowP.setVisible(True)
    windowS = V_secundaria() 
    sys.exit(app.exec_())
