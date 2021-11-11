# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TokenFav.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Fav(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(468, 436)
        Form.setStyleSheet("*{\n"
"font-family:century gothic;\n"
"}\n"
"\n"
"QWidget#Form{\n"
"background: qlineargradient(spread:pad, x1:1, y1:0.739, x2:1, y2:0.25, stop:0 rgba(37, 83, 134, 255), stop:1 rgba(29, 29, 29, 255))\n"
"\n"
"}\n"
"\n"
"QFrame\n"
"{\n"
"background: #1d1d1d;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"QToolButton\n"
"{\n"
"background: #2d89ef;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"QToolButton:hover\n"
"{\n"
"background:  #2b5797;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"QLabel{\n"
"color:white;\n"
"font-weight:bold;\n"
"\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"background:#1d1d1d;\n"
"border:none;\n"
"border-bottom: 1px solid white;\n"
"color:white;\n"
"}\n"
"\n"
"QPushButton{\n"
"background: #2d89ef;\n"
"color: white;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: #2b5797;\n"
"color: white;\n"
"border-radius: 5px;\n"
"font-weight:bold;\n"
"}\n"
"\n"
"QGroupBox{\n"
"color:white;\n"
"\n"
"}\n"
"\n"
"QGroupBox#ref{\n"
"color:white;\n"
"}\n"
"\n"
"QTableWidget\n"
"{\n"
"color:white;\n"
"}\n"
"\n"
"QLabel#Titulo\n"
"{\n"
"font-size:20px;\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"border-radius:20px;\n"
"}")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(30, 20, 421, 401))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.B_seleccionar = QtWidgets.QPushButton(self.frame)
        self.B_seleccionar.setGeometry(QtCore.QRect(120, 260, 75, 23))
        self.B_seleccionar.setObjectName("B_seleccionar")
        self.B_quitar = QtWidgets.QPushButton(self.frame)
        self.B_quitar.setGeometry(QtCore.QRect(240, 260, 75, 23))
        self.B_quitar.setObjectName("B_quitar")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(28, 300, 371, 71))
        self.groupBox.setObjectName("groupBox")
        self.B_agregar = QtWidgets.QPushButton(self.groupBox)
        self.B_agregar.setGeometry(QtCore.QRect(260, 30, 75, 23))
        self.B_agregar.setObjectName("B_agregar")
        self.LE_nuevo = QtWidgets.QLineEdit(self.groupBox)
        self.LE_nuevo.setGeometry(QtCore.QRect(30, 30, 211, 31))
        self.LE_nuevo.setObjectName("LE_nuevo")
        self.Titulo = QtWidgets.QLabel(self.frame)
        self.Titulo.setGeometry(QtCore.QRect(100, 10, 161, 31))
        self.Titulo.setObjectName("Titulo")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(50, 60, 311, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.L_row = QtWidgets.QLabel(self.frame)
        self.L_row.setGeometry(QtCore.QRect(220, 380, 47, 13))
        self.L_row.setObjectName("L_row")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.B_seleccionar.setText(_translate("Form", "Scrapear"))
        self.B_quitar.setText(_translate("Form", "Quitar"))
        self.groupBox.setTitle(_translate("Form", "Nuevo token"))
        self.B_agregar.setText(_translate("Form", "Agregar"))
        self.Titulo.setText(_translate("Form", "Tokens Favoritos"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Token"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Simbolo"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Referencia"))
        self.L_row.setText(_translate("Form", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Fav()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
