# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StartTrain.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StartTrainP(object):
    def setupUi(self, StartTrainP):
        StartTrainP.setObjectName("StartTrainP")
        StartTrainP.resize(1920, 1080)
        self.label = QtWidgets.QLabel(StartTrainP)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.jumpToScoreP = QtWidgets.QPushButton(StartTrainP)
        self.jumpToScoreP.setGeometry(QtCore.QRect(1700, 900, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.jumpToScoreP.setFont(font)
        self.jumpToScoreP.setObjectName("jumpToScoreP")
        self.startB = QtWidgets.QPushButton(StartTrainP)
        self.startB.setGeometry(QtCore.QRect(960, 50, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.startB.setFont(font)
        self.startB.setObjectName("startB")
        self.jumpToChooseP = QtWidgets.QPushButton(StartTrainP)
        self.jumpToChooseP.setGeometry(QtCore.QRect(30, 20, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        self.jumpToChooseP.setFont(font)
        self.jumpToChooseP.setObjectName("jumpToChooseP")

        self.retranslateUi(StartTrainP)
        QtCore.QMetaObject.connectSlotsByName(StartTrainP)

    def retranslateUi(self, StartTrainP):
        _translate = QtCore.QCoreApplication.translate
        StartTrainP.setWindowTitle(_translate("StartTrainP", "Form"))
        self.label.setText(_translate("StartTrainP", "整个画布大小用于显示摄像头的内容，由于还不能实现录制结束自动跳转，所以用完成录制按钮跳转到评分界面(现在只用了一个label，显示出摄影图片可能还需要改变该控件的内容)"))
        self.jumpToScoreP.setText(_translate("StartTrainP", "完成录制"))
        self.startB.setText(_translate("StartTrainP", "开始录制"))
        self.jumpToChooseP.setText(_translate("StartTrainP", "返回选择训练界面"))