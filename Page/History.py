# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'History.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HistoryP(object):
    def setupUi(self, HistoryP):
        HistoryP.setObjectName("HistoryP")
        HistoryP.resize(1920, 1080)
        self.jumpToMainWindowP = QtWidgets.QPushButton(HistoryP)
        self.jumpToMainWindowP.setGeometry(QtCore.QRect(1730, 30, 120, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.jumpToMainWindowP.setFont(font)
        self.jumpToMainWindowP.setStyleSheet("background-color: rgb(7, 33, 58);\n"
"color: rgb(252, 204, 220);")
        self.jumpToMainWindowP.setObjectName("jumpToMainWindowP")
        self.imageL = QtWidgets.QLabel(HistoryP)
        self.imageL.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.imageL.setText("")
        self.imageL.setPixmap(QtGui.QPixmap("../Image/patten3.png"))
        self.imageL.setObjectName("imageL")
        self.horizontalLayoutWidget = QtWidgets.QWidget(HistoryP)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(680, 130, 1141, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(20)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(22)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.listWidget = QtWidgets.QListWidget(HistoryP)
        self.listWidget.setGeometry(QtCore.QRect(680, 210, 1140, 620))
        self.listWidget.setObjectName("listWidget")
        self.imageL.raise_()
        self.jumpToMainWindowP.raise_()
        self.horizontalLayoutWidget.raise_()
        self.listWidget.raise_()

        self.retranslateUi(HistoryP)
        QtCore.QMetaObject.connectSlotsByName(HistoryP)

    def retranslateUi(self, HistoryP):
        _translate = QtCore.QCoreApplication.translate
        HistoryP.setWindowTitle(_translate("HistoryP", "Form"))
        self.jumpToMainWindowP.setText(_translate("HistoryP", "返回首页"))
        self.label.setText(_translate("HistoryP", "用户"))
        self.label_2.setText(_translate("HistoryP", "项目名"))
        self.label_3.setText(_translate("HistoryP", "得分（总）"))
        self.label_8.setText(_translate("HistoryP", "头部"))
        self.label_7.setText(_translate("HistoryP", "左臂"))
        self.label_6.setText(_translate("HistoryP", "右臂"))
        self.label_9.setText(_translate("HistoryP", "左腿"))
        self.label_10.setText(_translate("HistoryP", "右腿"))
        self.label_5.setText(_translate("HistoryP", "时长"))
        self.label_4.setText(_translate("HistoryP", "训练日期"))
