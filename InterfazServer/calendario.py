#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Se importa el modulo sys
import sys


#De PyQt4 importar QtGui y QtCore
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3




class App(QtGui.QWidget):


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #Se define el tamano de la ventana
        self.resize(600, 450) #Tamaño inicial
        self.setMaximumSize(800,600)
        #Se le coloca un titulo a la ventana y se asocia un icono.
        self.setWindowTitle('Calendario')
        self.layout = QGridLayout() #Crear un layout grid
        self.setLayout(self.layout) #Agregar el layout al cuadro de diálogo
        self.table = QTableWidget() #Crear la tabla
        #Define el calendario en una ventana
        self.cal = QtGui.QCalendarWidget(self)
        #Se define una cuadricula al calendario
        self.cal.setGridVisible(True)
        #Se define una etiqueta donde se mostrara la fecha seleccionada
        self.etiqueta = QtGui.QLabel(self)
        self.btnSalir = QtGui.QPushButton('Salir', self)
        self.btnSalir.setMaximumSize(400,300)
        self.connect(self.btnSalir, QtCore.SIGNAL('clicked()'),QtGui.qApp, QtCore.SLOT('quit()'))
        #Se captura la fecha y se muestra en la etiqueta
        self.fecha = self.cal.selectedDate()
        self.etiqueta.setText(str(self.fecha.toPyDate()))
        self.etiqueta.setAlignment(QtCore.Qt.AlignCenter)
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
        self.layout.addWidget(self.btnSalir, 3, 0) #Agregar el boton al layout
        self.table.setColumnCount(4)
        #Se captura la fecha y se muestra en la etiqueta
        self.fecha = self.cal.selectedDate()
        self.etiqueta.setText(str(self.fecha.toPyDate()))
        self.connect(self.cal, QtCore.SIGNAL('selectionChanged()'),
            self.mostrarFecha)

    def mostrarFecha(self):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['VALOR', 'NOMBRE', 'HORA', 'ID PLC'])
        self.fecha = self.cal.selectedDate()
        self.etiqueta.setText(str(self.fecha.toPyDate()))
        fecha = str(self.fecha.toPyDate())
        i=0
        #idx = self.window.treeView.currentIndex()
        #parent = self.window.tree_ui.model.history(idx)
        #idVar = str(parent.data().toPyObject())
        #idVar = idVar[idVar.find('i=')+2 : idVar.find(')')]
        idVar = raw_input("Introduzca el nombre del objeto (PLC): ")
        idVar = int(idVar)
        conexion = sqlite3.connect("database.db")
        consulta = conexion.cursor()
        #Extrayendo todas las filas
        print fecha
        print idVar
        sql = "SELECT * FROM PLC Where fecha_plc ='%s' and plc_id = %s" %(fecha, idVar)
        consulta.execute(sql)
        filas = consulta.fetchall()
        for fila in filas:
            print(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6])
            self.table.insertRow(i)
            valor = QTableWidgetItem(str(fila[1]))
            nombre = QTableWidgetItem(str(fila[2]))
            hora = QTableWidgetItem(str(fila[3]))
            #id_tags = QTableWidgetItem(str(fila[4]))
            self.table.setItem(i, 0, valor)
            self.table.setItem(i, 1, nombre)
            self.table.setItem(i, 2, hora)
            #self.table.setItem(i, 3, id_tags)
            i=i+1




#Se ejecuta el programa principal
if __name__ == "__main__":
   #Se instancia la clase QApplication
   app = QtGui.QApplication(sys.argv)
   #Se instancia el objeto QuitButton
   qb = App()
   #Se muestra la aplicacion
   qb.show()
   #Se sale de la aplicacion
   sys.exit(app.exec_())
