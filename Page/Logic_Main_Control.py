import socket
import sys
from PyQt5.QtWidgets import QApplication,QWidget
from Page import Login,Register,Main_Window,ChooseTrain,StartTrain,Score,History
from PyQt5 import QtGui,QtCore
target_host = "39.106.96.98"
target_port = 9998

'''
def login_clicked():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    txt1 = ui.usernameT.toPlainText()
    txt2 = ui.passwordT.toPlainText()
    print(txt1)
    print(txt2)
    msg = "login %s %s"%(txt1,txt2)
    print(msg)
    #msg = msg.encode()
    msg1 = "login 99 6"
    msg1 = msg.encode()
    client.send(msg1)
    response = client.recv(4096)
    print(response)
'''

class Login(QWidget,Login.Ui_LoginP):
    def __init__(self):
        super(Login,self).__init__()
        self.setupUi(self)
        self.jumpToRegisterP.clicked.connect(self.jumpToRegisterP_clicked)
        self.loginB_2.clicked.connect(self.loginB_clicked)


    def jumpToRegisterP_clicked(self):
        self.close()
        self.ui = Register()
        self.ui.show()

    def loginB_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


class Register(QWidget,Register.Ui_RegitserP):
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.jumpToLoginP.clicked.connect(self.jumpToLoginP_clicked)
        self.registerB.clicked.connect(self.registerB_clicked)

    def jumpToLoginP_clicked(self):
        self.close()
        self.ui = Login()
        self.ui.show()

    def registerB_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


class MainWindow(QWidget,Main_Window.Ui_MainWindowP):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.jumpToLoginP.clicked.connect(self.jumpToLoginP_clicked)
        self.jumpToChooseP.clicked.connect(self.jumpToChooseP_clicked)
        self.jumpToHistoryP.clicked.connect(self.jumpToHistoryP_clicked)
        self.jumpToLikeP.clicked.connect(self.jumpToLikeP_clicked)

    def jumpToLoginP_clicked(self):
        self.close()
        self.ui = Login()
        self.ui.show()
    def jumpToChooseP_clicked(self):
        self.close()
        self.ui = ChooseTrain()
        self.ui.show()
    def jumpToHistoryP_clicked(self):
        self.close()
        self.ui = History()
        self.ui.show()
    def jumpToLikeP_clicked(self):
        '''
        self.close()
        self.ui = Login()
        self.ui.show()
        '''



class ChooseTrain(QWidget,ChooseTrain.Ui_ChososeTrainP):
    def __init__(self):
        super(ChooseTrain, self).__init__()
        self.setupUi(self)
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)
        self.chooseCurrentVideoB.clicked.connect(self.chooseCurrentVideoB_clicked)

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()
    def chooseCurrentVideoB_clicked(self):
        self.close()
        self.ui = Score()
        self.ui.show()


class Score(QWidget,Score.Ui_Score):
    def __init__(self):
        super(Score, self).__init__()
        self.setupUi(self)
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


class History(QWidget,History.Ui_HistoryP):
    def __init__(self):
        super(History, self).__init__()
        self.setupUi(self)
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)


    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Login()
    ui.show()
    sys.exit(app.exec_())