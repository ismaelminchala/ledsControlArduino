# -*- coding: utf-8 -*-
import sqlite3, datetime
import random, time

#----------------------Creación de Objetos---------------------------------
def Crear_Objeto():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    nombre = raw_input("Introduzca el nombre del objeto (PLC): ")
    numvar = 0
    i=2011
    IpPLC = 123
    idPLC = "ns=2;i="+str(i)
    #Valor de los argumentos
    argumentos = (nombre, numvar, IpPLC, idPLC, datetime.date.today())
    #consulta SQL con argumentos ?, ?, ?, ?
    sql = """INSERT INTO PLC(nombre, numvar, IpPLC, idPLC, fecha_plc)VALUES (?, ?, ?, ?, ?)"""
    #Realizar la consulta
    if (consulta.execute(sql, argumentos)):
        print("Registro guardado con éxito")
    else:
        print("Ha ocurrido un error al guardar los datos")
    sql = "SELECT * FROM PLC WHERE idPLC = '%s' " % idPLC
    consulta.execute(sql)
    fila = consulta.fetchone()
    print fila
    
    consulta.execute("UPDATE PLC SET plc_id= %s WHERE idPLC = '%s' " %(i, idPLC))
    conexion.commit()

    sql = "SELECT * FROM PLC WHERE idPLC = '%s' " % idPLC
    consulta.execute(sql)
    fila = consulta.fetchone()
    print fila

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#------------------Creación de Tags-------------------------------

def Crear_Tag():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

#-------------------leer datos del objeto pedido---------------------------
    while True:
        id = raw_input("Ingrese el identificador del objeto (PLC) al cual desea ingresar el tag: ")
        #Sólo numeros enteros
        try:
            id = int(id)
            break
        except ValueError:
            print(id, "no es un numero entero")
    #Extrayendo una sola fila
    sql = "SELECT numvar FROM PLC WHERE plc_id = %s" % id
    consulta.execute(sql)
    fila = consulta.fetchone()
    numvar=int(fila[0])
    numvar=numvar+1

#-------------------Ingreso de datos en la Tag-------------------------------

    plc_ids = id
    nombre = raw_input("Introduzca el nombre de la variable: ")
    descripcion = raw_input("Introduzca la descripción de la variable: ")

    while True:
        tipo = raw_input("Introduzca el tipo de variable: ")
        if tipo == "integer":
            break
        elif tipo == "boolean":
            break
        elif tipo == "string":
            break
        else:
            print ("NO es ninguno de los tres tipos de datos")

    #Valor de los argumentos
    argumentos = (nombre, descripcion, tipo, plc_ids, datetime.datetime.now())
    #consulta SQL con argumentos ?, ?, ?, ?
    sql = """INSERT INTO Tags(nombre, descripcion, tipo,
    plc_ids, fecha_creacion)VALUES (?, ?, ?, ?, ?)"""

#-------------------actualiza el numero de variables a objeto---------------

    consulta.execute("UPDATE PLC SET numvar = '%s' WHERE plc_id = %s " %(numvar, id))
    conexion.commit()

    #Realizar la consulta
    if (consulta.execute(sql, argumentos)):
        print("Registro guardado con éxito")
    else:
        print("Ha ocurrido un error al guardar los datos")

#-----------------------Ingreso del registro de la tag------------------------

#----------------------------------
    sql = "SELECT tag_id FROM Tags Where nombre = '%s'" % nombre
    consulta.execute(sql)
    fila = consulta.fetchone()
    tag_id=int(fila[0])
#---------------------------------------
    valor = 1
    tag_ids = id
    #Valor de los argumentos
    argumentos = (valor, tag_ids, tag_id, datetime.datetime.now())
    #consulta SQL con argumentos ?, ?, ?, ?
    sql = """INSERT INTO Registro(valor, tag_ids, tag_id, hora)VALUES (?, ?, ?, ?)"""

    #Realizar la consulta
    if (consulta.execute(sql, argumentos)):
        print("Registro guardado con éxito")
    else:
        print("Ha ocurrido un error al guardar los datos")

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Leer Datos Objetos ----------------------------

def Leer_Objetos():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    #Extrayendo todas las filas
    sql = "SELECT * FROM PLC"
    if (consulta.execute(sql)):
        filas = consulta.fetchall()
        for fila in filas:
            print(fila[0], fila[1], fila[2], fila[3])

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Leer Datos Tags ------------------------------

def Leer_Tags():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    #Extrayendo todas las filas
    sql = "SELECT * FROM Tags"
    if (consulta.execute(sql)):
        filas = consulta.fetchall()
    for fila in filas:
        print(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7])

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Leer Registro-------------------------------------

def Leer_Registro():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    #Extrayendo todas las filas
    sql = "SELECT * FROM Registro"
    if (consulta.execute(sql)):
        filas = consulta.fetchall()
        for fila in filas:
            print(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6])

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Eliminar Objeto------------------------------------

def Eliminar_Objeto():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    id = raw_input("Ingrese el identificador del objeto (PLC) al cual desea eliminar: ")
    consulta.execute("DELETE from PLC where plc_id=%s"%id)
    conexion.commit()

    #Extrayendo una sola fila
    sql = "SELECT tag_id FROM Tags WHERE plc_ids = %s" % id
    consulta.execute(sql)
    filas = consulta.fetchall()
    for fila in filas:
        temp = int(fila[0])
        consulta.execute("DELETE from Tags where tag_id=%s"%temp)
        conexion.commit()
        #-----------------------elimina registros--------------------
        consulta.execute("DELETE from Registro where tag_id=%s"%temp)
        conexion.commit()
        #-----------------------por ver seria otro for eliminar todos registros de cada variable

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()


#---------------------Eliminar Tag--------------------------------------

def Eliminar_Tag():

    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    id = raw_input("Ingrese el identificador del plc al cual desea eliminar la tag: ")
    #Extrayendo una sola fila
    sql = "SELECT numvar FROM PLC WHERE plc_id = %s" % id
    consulta.execute(sql)
    fila = consulta.fetchone()
    numvar=int(fila[0])
    numvar=numvar-1

#-------------------actualiza el numero de variables a objeto---------------

    consulta.execute("UPDATE PLC SET numvar = '%s' WHERE plc_id = %s " %(numvar, id))
    conexion.commit()

#-----------------------elimina tag---------------------------------------------
    id = raw_input("Ingrese el identificador del tag al cual desea eliminar: ")
    consulta.execute("DELETE from Tags where tag_id=%s"%id)
    conexion.commit()

#-----------------------elimina registros---------------------------------------------
    consulta.execute("DELETE from Registro where tag_id=%s"%id)
    conexion.commit()
#-----------------------por ver
    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------------Historial----------------------------------

def Historial():
    #Establecer la conexión
    conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    consulta = conexion.cursor()

    id = raw_input("Ingrese el identificador de la tag: ")

    #Extrayendo todas las filas
    sql = "SELECT * FROM Registro WHERE tag_id = %s" % id
    if (consulta.execute(sql)):
        filas = consulta.fetchall()
        for fila in filas:
            print(fila[0], fila[1], fila[2], fila[3], fila[4])

    #Cerrar la consulta
    consulta.close()
    #Guardar los cambios en la base de datos
    conexion.commit()
    #Cerrar la conexión
    conexion.close()

#-------------------Numero Aleatorio-----------------------------------

#def numeroAleatorio():




    #Establecer la conexión
    #conexion = sqlite3.connect("database.db")
    #Seleccionar el cursor para iniciar una consulta
    #consulta = conexion.cursor()

    #sql = "SELECT * FROM Tags"
    #if (consulta.execute(sql)):
        #filas = consulta.fetchall()
    #sql = "SELECT * FROM Tags"
    #if (consulta.execute(sql)):
        #filas = consulta.fetchall()
        #
        #for fila in range(filas):
            #valor = random.randrange(100)
            #tag_ids = tags_ids +1
            #time.sleep( 1 )
            #Valor de los argumentos
            #argumentos = (valor, tag_ids, datetime.datetime.now())
            #consulta SQL con argumentos ?, ?, ?, ?
            #sql = """INSERT INTO Registro(valor, tag_ids, hora)VALUES (?, ?, ?)"""
            #Realizar la consulta
            #if (consulta.execute(sql, argumentos)):
                #print("Registro guardado con éxito")
            #else:
                #print("Ha ocurrido un error al guardar los datos")


 #while True:
        #id = raw_input("Ingrese el identificador del objeto (PLC) al cual desea ingresar el tag: ")
        #Sólo numeros enteros
        #try:
            #id = int(id)
            #break
        #except ValueError:
            #print(id, "no es un numero entero")
    #Extrayendo una sola fila
    #sql = "SELECT numvar FROM PLC WHERE plc_id = %s" % id
    #consulta.execute(sql)
    #fila = consulta.fetchone()
    #numvar=int(fila[0])
    #print(numvar)
    #numvar=numvar+1

#-------------------actualiza el numero de variables a objeto---------------

    #consulta.execute("UPDATE PLC SET numvar = '%s' WHERE plc_id = %s " %(numvar, id))
    #conexion.commit()

#-------------------Ingreso de datos en la Tag-------------------------------

    #plc_ids = id
    #nombre = raw_input("Introduzca el nombre de la variable: ")
    #descripcion = raw_input("Introduzca la descripción de la variable: ")




    #Cerrar la consulta
    #consulta.close()
    #Guardar los cambios en la base de datos
    #conexion.commit()
    #Cerrar la conexión
    #conexion.close()


#--------------------Menu-----------------------------------------
def menu():
    print "Selecciona una opción"
    print "\t1 - Ingresar Objeto"
    print "\t2 - Ingresar Tag"
    print "\t3 - Leer Datos de los Objetos"
    print "\t4 - Leer Datos Tags"
    print "\t5 - Leer Datos Registros"
    print "\t6 - Eliminar Objeto"
    print "\t7 - Eliminar Tag"
    print "\t8 - Leer Datos Historial"
    print "\t9 - Salir"

while True:
    # Mostramos el menu
    menu()

    # solicitamos una opción al usuario
    opcionMenu = raw_input("inserta un numero valor >> ")

    if opcionMenu=="1":
        Crear_Objeto()
        raw_input("Objeto Ingresado...\npulsa una tecla para continuar")

    elif opcionMenu=="2":
        Crear_Tag()
        #numeroAleatorio()
        raw_input("Tag Ingresado...\npulsa una tecla para continuar")

    elif opcionMenu=="3":
        Leer_Objetos()
        raw_input("Datos de Objetos...\npulsa una tecla para continuar")

    elif opcionMenu=="4":
        Leer_Tags()
        raw_input("Datos de Tags...\npulsa una tecla para continuar")

    elif opcionMenu=="5":
        Leer_Registro()
        raw_input("Datos de Registros...\npulsa una tecla para continuar")

    elif opcionMenu=="6":
        Eliminar_Objeto()
        raw_input("Objeto Eliminado...\npulsa una tecla para continuar")

    elif opcionMenu=="7":
        Eliminar_Tag()
        raw_input("Tag Eliminado...\npulsa una tecla para continuar")

    elif opcionMenu=="8":
        Historial()
        raw_input("Historial Leido...\npulsa una tecla para continuar")

    elif opcionMenu=="9":
        print "Salir"
        break
    else:
        print ""
        raw_input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
