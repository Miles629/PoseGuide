# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RankList.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RankListP(object):
    def setupUi(self, RankListP):
        RankListP.setObjectName("RankListP")
        RankListP.resize(1920, 1080)
        self.imageL = QtWidgets.QLabel(RankListP)
        self.imageL.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.imageL.setText("")
        self.imageL.setPixmap(QtGui.QPixmap("../Image/patten2.png"))
        self.imageL.setObjectName("imageL")
        self.pushButton = QtWidgets.QPushButton(RankListP)
        self.pushButton.setGeometry(QtCore.QRect(1760, 20, 120, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(252, 204, 220);\n"
"background-color: rgb(7, 33, 58);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(RankListP)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1730, 160, 141, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(0, 201, 205);\n"
"color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setStyleSheet("background-color: rgb(254, 97, 148);\n"
"color: rgb(255, 255, 255);\n"
"font: 20pt \"Adobe Arabic\";")
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setStyleSheet("background-color: rgb(252, 204, 220);\n"
"color: rgb(255, 255, 255);\n"
"font: 20pt \"Adobe Arabic\";")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setStyleSheet("background-color: rgb(130, 156, 181);\n"
"color: rgb(255, 255, 255);\n"
"font: 20pt \"Adobe Arabic\";")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.listWidget_1 = QtWidgets.QListWidget(RankListP)
        self.listWidget_1.setGeometry(QtCore.QRect(250, 90, 280, 900))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.listWidget_1.setFont(font)
        self.listWidget_1.setStyleSheet("font: 20pt \"Adobe Arabic\";\n"
"background-color: rgb(7, 33, 58);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.listWidget_1.setObjectName("listWidget_1")
        self.listWidget_2 = QtWidgets.QListWidget(RankListP)
        self.listWidget_2.setGeometry(QtCore.QRect(670, 90, 681, 900))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setStyleSheet("font: 20pt \"Adobe Arabic\";\n"
"background-color: rgb(7, 33, 58);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.listWidget_2.setObjectName("listWidget_2")

        self.retranslateUi(RankListP)
        QtCore.QMetaObject.connectSlotsByName(RankListP)

    def retranslateUi(self, RankListP):
        _translate = QtCore.QCoreApplication.translate
        RankListP.setWindowTitle(_translate("RankListP", "Form"))
        self.pushButton.setText(_translate("RankListP", "返回上级"))
        self.label_5.setText(_translate("RankListP", "健身区"))
        self.label_4.setText(_translate("RankListP", "有氧区"))
        self.label_2.setText(_translate("RankListP", "舞蹈区"))
        self.label_3.setText(_translate("RankListP", "拉伸"))
