# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'translation.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QApplication


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)
        font = QtGui.QFont()
        font.setKerning(False)
        Dialog.setFont(font)
        Dialog.setStyleSheet("background-color:rgb(220, 220, 220);")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(402, 50, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgb(159, 159, 159);")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 371, 21))
        self.lineEdit.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border: 2px solid rgb(0, 200, 240);\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 30, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(402, 100, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color:rgb(159, 159, 159);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 100, 371, 21))
        self.lineEdit_2.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border: 2px solid rgb(0, 200, 240);\n"
"")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(20, 230, 121, 511))
        self.listView.setStyleSheet("background-color:rgb(206, 206, 206);\n"
"border: 2px solid rgb(159,159,159);")
        self.listView.setObjectName("listView")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(780, 110, 211, 631))
        self.tableView.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.tableView.setObjectName("tableView")
        self.tableView_2 = QtWidgets.QTableView(Dialog)
        self.tableView_2.setGeometry(QtCore.QRect(530, 110, 211, 631))
        self.tableView_2.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.tableView_2.setObjectName("tableView_2")
        self.tableView_3 = QtWidgets.QTableView(Dialog)
        self.tableView_3.setGeometry(QtCore.QRect(170, 230, 321, 511))
        self.tableView_3.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.tableView_3.setObjectName("tableView_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(790, 80, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(540, 80, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(180, 190, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 200, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(False)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border: 2px solid rgb(159,159,159);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(900, 80, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color:rgb(159, 159, 159);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 140, 471, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color:rgb(255, 255, 69);\n"
"border: 2px solid rgb(159,159,159);\n"
"")
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Search"))
        self.label.setText(_translate("Dialog", "Dictionary File"))
        self.label_2.setText(_translate("Dialog", "Dictionary File"))
        self.pushButton_2.setText(_translate("Dialog", "Search"))
        self.label_3.setText(_translate("Dialog", "Not Found"))
        self.label_4.setText(_translate("Dialog", "Matched word"))
        self.label_5.setText(_translate("Dialog", "Need Checking"))
        self.label_6.setText(_translate("Dialog", "Target Language"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_4.setText(_translate("Dialog", "Translation"))
