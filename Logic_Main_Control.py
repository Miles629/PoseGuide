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
<<<<<<< Updated upstream:Page/Logic_Main_Control.py
        self.close()
        self.ui = MainWindow()
        self.ui.show()
=======
        try:
            user = self.userT.toPlainText()
            pwd = self.pwdT.toPlainText()
            print(user)
            print(pwd)
            msg = "login %s %s" %(user, pwd)
            print(msg)
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("LoginReturn:%s" %(response))
            if response:
                userAccount = user
                self.close()
                self.ui = MainWindow()
                self.ui.show()
            else:
                QMessageBox.warning(self,'错误','您输入的密码有误',QMessageBox.Cancel)
        except Exception as e:
            QMessageBox.warning(self,"错误",e,QMessageBox.Cancel)


>>>>>>> Stashed changes:Logic_Main_Control.py


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
<<<<<<< Updated upstream:Page/Logic_Main_Control.py
        self.close()
        self.ui = MainWindow()
        self.ui.show()
=======
        try:
            email =self.emailT.toPlainText()
            user = self.usernameT.toPlainText()
            pwd = self.passwordT.toPlainText()
            vpwd = self.VpasswordT.toPlainText()
            print(user)
            print(pwd)
            if pwd == vpwd:
                msg = "signin %s %s %s" %(user, pwd, email)
                print(msg)
                msg = msg.encode()
                client.send(msg)
                response = client.recv(4096)
                print("RegisterReturn:%s" %(response))
                if response:
                    userAccount = user
                    self.close()
                    self.ui = MainWindow()
                    self.ui.show()
                else:
                    QMessageBox.about(self,'有误','注册失败',QMessageBox.Cancel)
            else:
                QMessageBox.warning(self,"错误",'您输入的两次密码不同，请重新输入',QMessageBox.Ok)

        except Exception as e:
            QMessageBox.warning(self,"错误",e,QMessageBox.Cancel)

>>>>>>> Stashed changes:Logic_Main_Control.py


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

<<<<<<< Updated upstream:Page/Logic_Main_Control.py
=======
    def jumpToScore_clicked(self):
        try:
            # 上传训练历史记录的格式如下，u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
            #msg = "uphistory u item s dp dur date"
            msg = "uphistory %s %s %s %s %s %s" % (userAccount,"项目1","90","E://Video","16:00","2020/7/11")
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("upHistoryReturn:%s" % (response))
            if response:
                QMessageBox.warning(self,'提示',"分数上传成功",msg,QMessageBox.Ok)
                self.close()
                self.ui = Score()
                self.ui.show()
            else:
                QMessageBox.warning(self,'提示',"分数上传失败",msg,QMessageBox.Ok)
        except Exception as e:
            QMessageBox.warning(self, '提示',"错误", e, QMessageBox.Cancel)
            print(e)


    def startB_clicked(self):
        do = "nothing"

>>>>>>> Stashed changes:Logic_Main_Control.py

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