# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Register.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegitserP(object):
    def setupUi(self, RegitserP):
        RegitserP.setObjectName("RegitserP")
        RegitserP.resize(1920, 1080)
        self.registerB = QtWidgets.QPushButton(RegitserP)
        self.registerB.setGeometry(QtCore.QRect(1340, 860, 120, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.registerB.setFont(font)
        self.registerB.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(7, 33, 58);")
        self.registerB.setObjectName("registerB")
        self.jumpToLoginP = QtWidgets.QPushButton(RegitserP)
        self.jumpToLoginP.setGeometry(QtCore.QRect(1720, 60, 120, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.jumpToLoginP.setFont(font)
        self.jumpToLoginP.setStyleSheet("color: rgb(252, 204, 220);\n"
"background-color: rgb(7, 33, 58);")
        self.jumpToLoginP.setObjectName("jumpToLoginP")
        self.imageL = QtWidgets.QLabel(RegitserP)
        self.imageL.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.imageL.setText("")
        self.imageL.setPixmap(QtGui.QPixmap("../Image/patten.png"))
        self.imageL.setObjectName("imageL")
        self.btn_keyboard = QtWidgets.QPushButton(RegitserP)
        self.btn_keyboard.setGeometry(QtCore.QRect(810, 320, 120, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btn_keyboard.setFont(font)
        self.btn_keyboard.setStyleSheet("background-color: rgb(7, 33, 58);\n"
"color: rgb(252, 204, 220);")
        self.btn_keyboard.setObjectName("btn_keyboard")
        self.emailT = QtWidgets.QLineEdit(RegitserP)
        self.emailT.setGeometry(QtCore.QRect(990, 310, 789, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.emailT.setFont(font)
        self.emailT.setStyleSheet("color: rgb(0, 0, 0);")
        self.emailT.setClearButtonEnabled(True)
        self.emailT.setObjectName("emailT")
        self.usernameT = QtWidgets.QLineEdit(RegitserP)
        self.usernameT.setGeometry(QtCore.QRect(990, 430, 789, 80))
        self.usernameT.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 22pt \"Adobe Arabic\";")
        self.usernameT.setClearButtonEnabled(True)
        self.usernameT.setObjectName("usernameT")
        self.passwordT = QtWidgets.QLineEdit(RegitserP)
        self.passwordT.setGeometry(QtCore.QRect(990, 570, 789, 80))
        self.passwordT.setStyleSheet("font: 22pt \"Adobe Arabic\";\n"
"color: rgb(0, 0, 0);")
        self.passwordT.setClearButtonEnabled(True)
        self.passwordT.setObjectName("passwordT")
        self.VpasswordT = QtWidgets.QLineEdit(RegitserP)
        self.VpasswordT.setGeometry(QtCore.QRect(990, 700, 789, 80))
        self.VpasswordT.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 22pt \"Adobe Arabic\";")
        self.VpasswordT.setClearButtonEnabled(True)
        self.VpasswordT.setObjectName("VpasswordT")
        self.imageL.raise_()
        self.registerB.raise_()
        self.jumpToLoginP.raise_()
        self.btn_keyboard.raise_()
        self.emailT.raise_()
        self.usernameT.raise_()
        self.passwordT.raise_()
        self.VpasswordT.raise_()

        self.retranslateUi(RegitserP)
        QtCore.QMetaObject.connectSlotsByName(RegitserP)

    def retranslateUi(self, RegitserP):
        _translate = QtCore.QCoreApplication.translate
        RegitserP.setWindowTitle(_translate("RegitserP", "Form"))
        self.registerB.setText(_translate("RegitserP", "注册"))
        self.jumpToLoginP.setText(_translate("RegitserP", "返回登录"))
        self.btn_keyboard.setText(_translate("RegitserP", "键盘"))
        self.emailT.setText(_translate("RegitserP", "email"))
        self.usernameT.setText(_translate("RegitserP", "username"))
        self.passwordT.setText(_translate("RegitserP", "password"))
        self.VpasswordT.setText(_translate("RegitserP", "vertify password"))
