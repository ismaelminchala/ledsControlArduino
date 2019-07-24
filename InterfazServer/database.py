# -*- coding: utf-8 -*-
import sqlite3, datetime
import time


#----------------------Creación de Objetos---------------------------------
def Crear_Objeto(NomObj, ip, idPlc):
    idUlt=int(idPlc)
    IpPLC = ip
    nombrePLC = NomObj
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()
    idPLC = "ns=2;i="+str(idPlc)
    #Valor de los argumentos
    argumentos = (nombrePLC, IpPLC, idPLC, datetime.date.today(), idUlt)
    #consulta SQL con argumentos ?, ?, ?, ?
    sql = """INSERT INTO PLC(nombrePLC, IpPLC, idPLC, fecha_plc, idUlt)
    VALUES (?, ?, ?, ?, ?)"""
    #Realizar la consulta
    consulta.execute(sql, argumentos)
    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#------------------Creación de Tags-------------------------------

def Crear_Tag(NomVar, tagPLC, desc, valTipo, idPlc, idTag):
    idPlc=int(idPlc)
    idTag=int(idTag)
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

#-------------------Ingreso de datos en la Tag-------------------------------
    plc_ids = idPlc
    nombreTag = str(NomVar)
    descripcion = str(desc)
    tipo = str(valTipo)
    tagPLC =str(tagPLC)
    idServidor = idTag
    
    #Valor de los argumentos
    argumentos = (nombreTag, descripcion, tagPLC, tipo, plc_ids , idServidor, datetime.datetime.now())
    #consulta SQL con argumentos ?, ?, ?, ?
    sql = """INSERT INTO Tags(nombreTag, descripcion, tagPLC, tipo,
    plc_ids, idServidor, fecha_creacion)VALUES (?, ?, ?, ?, ?, ?, ?)"""
    #Realizar la consulta
    consulta.execute(sql, argumentos)

#-----------------------Ingreso del registro de la tag------------------------
    
    valor="OFF"
    tag_id = idTag
    tag_ids = idPlc
    #Valor de los argumentos
    argumentos = (valor, tag_ids, nombreTag, tag_id, datetime.datetime.now(), datetime.date.today())
    #consulta SQL con argumentos ?, ?, ?, ?
    sql = """INSERT INTO Registro(valor, tag_ids, nombreTag, tag_id, hora, fecha_Registro)VALUES (?, ?, ?, ?, ?, ?)"""

    #Realizar la consulta
    consulta.execute(sql, argumentos)

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Eliminar Objeto------------------------------------

def eliminarNodo(idObjeto):
    idUlt = 0
    idServidor = 0
    idObjeto = int(idObjeto)
    
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    sql = "SELECT idUlt FROM PLC" 
    consulta.execute(sql)
    filas = consulta.fetchall()
    for fila in filas:
        if  idObjeto == int(fila[0]):
            idUlt = idObjeto
            eliminarObjeto(idUlt)

    if idUlt == 0:
        sql = "SELECT idServidor FROM Tags"
        consulta.execute(sql)
        filas = consulta.fetchall()
        for fila in filas:
            if  idObjeto == int(fila[0]):
                idServidor = idObjeto
                eliminarTag(idServidor)

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Eliminar Objeto------------------------------------

def eliminarObjeto(idUlt):
    idUlt = idUlt
    
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    #-----------------------elimina registros--------------------
    consulta.execute("DELETE from PLC where idUlt=%s"%idUlt)
    conexion.commit()

    #-----------------------elimina registros--------------------
    consulta.execute("DELETE from Registro where tag_ids=%s"%idUlt)
    conexion.commit()
    
    #-----------------------elimina tags--------------------
    consulta.execute("DELETE from Tags where plc_ids=%s"%idUlt)
    conexion.commit()

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()


#---------------------Eliminar Tag--------------------------------------

def eliminarTag(idServidor):

    idServidor = idServidor

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

#-----------------------elimina tag---------------------------------------------
    consulta.execute("DELETE from Tags where idServidor=%s"%idServidor)
    conexion.commit()

#-----------------------elimina registros---------------------------------------------
    consulta.execute("DELETE from Registro where tag_id=%s"%idServidor)
    conexion.commit()

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#----------------------------Actualizar Registros-----------------------

def Actualizar(idPlc, nombreTag, val):
    valor=str(val)
    tag_ids = int(idPlc)
    nombreTag = nombreTag

    tam=len(valor)
    if tam >> 3:
        valor=valor[0:4]
   
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()
    
    #Extrayendo todas las filas
    sql = "SELECT nombreTag, idServidor FROM Tags WHERE plc_ids = %s " %tag_ids
    consulta.execute(sql)
    filas = consulta.fetchall()
    for fila in filas:
        if nombreTag == str(fila[0]):
            tag_id=fila[1]
    temp = []
    sql = "SELECT * FROM Registro WHERE tag_ids = %s " %tag_ids
    consulta.execute(sql)
    filas = consulta.fetchall()
    for fila in filas:
        if nombreTag == str(fila[2]) and tag_id == int(fila[5]):
            temporal = str(fila[1])
            temp.append(temporal)
    temporal = temp[-1]
    if temporal != valor:
        #Valor de los argumentos
        argumentos = (valor, nombreTag, datetime.datetime.now(), datetime.date.today(), tag_id, tag_ids)
        #consulta SQL con argumentos ?, ?, ?, ?
        sql = """INSERT INTO Registro(valor, nombreTag, hora, fecha_Registro, tag_id, tag_ids)
        VALUES (?, ?, ?, ?, ?, ?)"""
        #Realizar la consulta
        consulta.execute(sql, argumentos)
    
    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#---------------------------Borrar Base de Datos----------------------

def BorrarBase():
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    #-----------------------elimina registros--------------------
    consulta.execute("DELETE FROM PLC")
    #-----------------------elimina registros--------------------
    consulta.execute("DELETE FROM Registro")
    #-----------------------elimina tags--------------------
    consulta.execute("DELETE FROM Tags")

    #Cerrar la consulta
    consulta.close()
    conexion.commit()
    #Cerrar la conexión
    conexion.close()
    
    




    

