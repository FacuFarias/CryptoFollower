import sys
import time
from tokens import *
from TokenFav import *
from notificacion import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
import requests
import webbrowser
import sqlite3
import numpy as np

vRef=np.zeros(20)
vAct=np.zeros(20)
timers=np.zeros(20)

tokens= []


token = '0x31471e0791fcdbe82fbf4c44943255e923f1b794'
j=-1


class DialogNotif(QWidget):
	def __init__(self):
		super().__init__()
		
		self.notificaciones = QtWidgets.QDialog()
		self.uinotif = Ui_Notificacion()
		self.uinotif.setupUi(self.notificaciones)
		self.notificaciones.show()
		self.row= mi_app.ui.L_CellChanged.text()
		name = mi_app.ui.T_Tokens.item(int(self.row),0).text()
		vari = mi_app.ui.T_Tokens.item(int(self.row),4).text()
		print(name)
		self.uinotif.l_texto.setText(name + " ha variado su precio un "+vari+"%")
		
		self.uinotif.b_detener.clicked.connect(self.detener)
		self.uinotif.b_analizar.clicked.connect(self.analizar)

	def detener(self):
		pass

	def analizar(self):
		global tokens
		row=mi_app.ui.L_CellSelected.text()
		print("la columna seleccionada es: "+ str(row))
		token = tokens[int(row)]
		url = 'https://poocoin.app/tokens/'+token
		webbrowser.open(url)
		print(url)



class DialogFav(QWidget):
	def __init__(self):
		super().__init__()
		
		self.Favoritos = QtWidgets.QDialog()
		self.uifav = Ui_Fav()
		self.uifav.setupUi(self.Favoritos)
		self.Favoritos.show()
		self.conexion=sqlite3.connect("list_fav.db")
		self.uifav.B_seleccionar.clicked.connect(self.seleccionar)
		
		self.uifav.B_agregar.clicked.connect(self.agregar)
		self.uifav.B_quitar.clicked.connect(self.quitar)
		self.uifav.tableWidget.cellClicked.connect(self.uifav.L_row.setNum)
		

		self.cursor = self.conexion.execute("select name,symbol,ref_price from favoritos")
		self.i=0
		for fila in self.cursor:
			self.uifav.tableWidget.insertRow(self.i)
			item=QtWidgets.QTableWidgetItem(fila[0])
			self.uifav.tableWidget.setItem(self.i,0,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			item=QtWidgets.QTableWidgetItem(fila[1])
			self.uifav.tableWidget.setItem(self.i,1,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			item=QtWidgets.QTableWidgetItem(str(fila[2]))
			self.uifav.tableWidget.setItem(self.i,2,item)
			self.i=self.i+1
		self.conexion.close()
		self.uifav.tableWidget.itemChanged.connect(self.cambiarRef)


	def cambiarRef(self,item):
		row= item.row()
		col = item.column()
		ref= self.uifav.tableWidget.item(row,col).text()
		self.conexion=sqlite3.connect("list_fav.db")
		try:
			ref=float(ref)
			print("Se pudo convertir")
			name=self.uifav.tableWidget.item(row,0).text()
			
			
			try:
				query="UPDATE favoritos SET ref_price=(?) where name=(?)"
				self.conexion.execute(query,(ref,name))
				self.conexion.commit()
				print("se insertó la ref")
				
			
			except:
				print("no se insertó ref")
		except:
			
			query="select ref_price from favoritos where symbol=?"
			symbol= self.uifav.tableWidget.item(row,1).text()
			print(symbol)
			cursor=self.conexion.execute(query,(symbol,))
			refp = cursor.fetchone()
			print(refp[0])
			#refp=''.join(refp)
			#item=QtWidgets.QTableWidgetItem(str(refp))
			#self.uifav.tableWidget.setItem(row,col,item)
			#self.uifav.tableWidget.item(row,col).setBackground(QtGui.QColor("red"))
			
		
		self.conexion.close()




	def seleccionar(self):

		row=self.uifav.L_row.text()
		symbol= self.uifav.tableWidget.item(int(row),1).text()
		#print(symbol)
		self.conexion=sqlite3.connect("list_fav.db")
		query= "select contract from favoritos where symbol = ?"
		cursor = self.conexion.execute(query,(symbol,))
		
		token = cursor.fetchone()
		token=''.join(token)
		self.conexion.close()
		mi_app.ui.lineEdit.setText(token)
		mi_app.scrapear()


	def agregar(self):
		self.uifav.tableWidget.blockSignals(True)
		self.conexion= sqlite3.connect("list_fav.db")
		token = self.uifav.LE_nuevo.text()
		try:
			response = requests.get('https://api.pancakeswap.info/api/v2/tokens/'+token) 
			data = response.json()
			print(data['data'])
			query="insert into favoritos(contract,name,symbol,price) values (?,?,?,?)"
			self.conexion.execute(query,(token,data['data']['name'],data['data']['symbol'],float(data['data']['price'])))
			self.conexion.commit()


			self.uifav.tableWidget.insertRow(self.i)
			item=QtWidgets.QTableWidgetItem(data['data']['name'])
			self.uifav.tableWidget.setItem(self.i,0,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			item=QtWidgets.QTableWidgetItem(data['data']['symbol'])
			self.uifav.tableWidget.setItem(self.i,1,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			self.i=self.i+1
		except:
			print("no se pudo agregar")
		self.uifav.tableWidget.blockSignals(False)
		self.conexion.close()

	def quitar(self):
		self.conexion= sqlite3.connect("list_fav.db")
		row=self.uifav.L_row.text()
		symbol= self.uifav.tableWidget.item(int(row),1).text()
		query = "DELETE from favoritos where symbol=?"
		self.conexion.execute(query,(symbol,))
		self.uifav.tableWidget.removeRow(int(row))
		
	
class WorkerThread(QThread):
	
	def run(self):

		global vRef
		global vAct
		
		global j
		global tokens
		global timers
		ft=False
		running=True
		vActAnt = 0
		token = mi_app.ui.lineEdit.text()
		
		#print(token[0:2])

		if token[0:2]!='0x':
			mi_app.ui.L_notif.setText("Inserte un token valido")
			running=False
		
		for contract in tokens:
			if token==contract:
				running=False
				print("este token ya está siendo scrapeado")

		if running==True:
			tokens.append(token)
			print(tokens)
			j=j+1
			i=j
			timers[i]=0
			mi_app.ui.T_Tokens.insertRow(j)
		
		while running==True:
			response = requests.get('https://api.pancakeswap.info/api/v2/tokens/'+tokens[i]) 
			data = response.json()
			vAct[i] = round(float(data['data']['price']),3)


			if vAct[i] != vActAnt:
				vActAnt=vAct[i]
				timers[i]=0
				#print("cambio el valor")
			else:
				timers[i]=timers[i]+1
			#print(vAct[j])
			item=QtWidgets.QTableWidgetItem(data['data']['name'])
			mi_app.ui.T_Tokens.setItem(i,0,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			item=QtWidgets.QTableWidgetItem(data['data']['symbol'])
			mi_app.ui.T_Tokens.setItem(i,1,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			item=QtWidgets.QTableWidgetItem(str(vAct[i]))
			mi_app.ui.T_Tokens.setItem(i,2,item)
			item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
			
			if ft==False:
				ft=True	
				self.conexion=sqlite3.connect("list_fav.db")
				self.query=("SELECT ref_price FROM favoritos WHERE symbol=(?)")
				cursor = self.conexion.execute(self.query,(data['data']['symbol'],))
				ref = cursor.fetchone()
				

				item=QtWidgets.QTableWidgetItem(str(ref[0]))
				mi_app.ui.T_Tokens.setItem(i,3,item)

				#print("El precio de ref es:"+str(ref))
				self.conexion.close()


			
			
			
			item=QtWidgets.QTableWidgetItem(str(int(timers[i])))
			mi_app.ui.T_Tokens.setItem(i,5,item)
			mi_app.ui.T_Tokens.hideRow(i)
			mi_app.ui.T_Tokens.showRow(i)
			

			time.sleep(1)			
			print(timers[i])
	

class Ventana(QWidget):


	def __init__(self,parent=None):

		QtWidgets.QWidget.__init__(self,parent)
		self.ui=Ui_Dialog()
		self.ui.setupUi(self)
		self.thread={}
		self.ui.B_scrap.clicked.connect(self.scrapear)
		self.ui.B_detener.clicked.connect(self.detener)
		self.ui.B_guardar.clicked.connect(self.guardar)
		self.ui.B_fav.clicked.connect(self.favoritos)
		self.ui.T_Tokens.cellClicked[int,int].connect(self.ui.L_CellSelected.setNum)

		self.ui.T_Tokens.itemChanged.connect(self.cambiarPrecio)
		self.ui.L_CellChanged.hide()
		self.ui.L_CellSelected.hide()
		
	def scrapear(self):
		self.worker=WorkerThread()
		self.worker.start()
		self.worker.finished.connect(self.finscrap)

	def finscrap(self):
		print("se termino el scrapeo")
  
	def guardar(self):
		global vRef
		global vAct
		row = int(self.ui.L_CellSelected.text())
		print("La fila seleccionada es:"+ str(row))
		vRef[row]=vAct[row]
		item=QtWidgets.QTableWidgetItem(str(vRef[row]))
		mi_app.ui.T_Tokens.setItem(row,3,item)
	
	
	def detener(self):
		global j
		global tokens
		global running
		running=False
		mi_app.ui.T_Tokens.clearContents()
		j=-1
		tokens =[]
		i=0
		rows=mi_app.ui.T_Tokens.rowCount()
		print("cantidad de filas = " + str(rows))
		while i<=rows:
			mi_app.ui.T_Tokens.removeRow(rows-1-i)
			i=i+1
			print("pase por aca "+str(i))
			
			
	

	def favoritos(self):

		self.diafav= DialogFav()
		
		

	def cambiarPrecio(self,item):
		global vRef
		row = item.row()
		col = item.column()
		mi_app.ui.L_CellChanged.setText(str(row))
		
		if col == 3:
			ref = mi_app.ui.T_Tokens.item(row,col).text()
			vRef[row]= float(ref)
			print("El precio de referencia es de:"+str(vRef[row]))

			variacion=((vAct[row]-vRef[row])/(vRef[row]))*100
			var=QtWidgets.QTableWidgetItem(str(round(variacion,5)))
			mi_app.ui.T_Tokens.setItem(row,4,var)
			var.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

			if abs(variacion)>10:
					mi_app.diaNotif = DialogNotif()

        


if __name__ == "__main__":
	mi_aplicacion=QApplication(sys.argv)
	mi_app = Ventana()
	mi_app.show()
	sys.exit(mi_aplicacion.exec_())