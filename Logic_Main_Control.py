import sys
import socket
from Page import Login,Register,Main_Window,ChooseTrain,StartTrain,Score,History
<<<<<<< Updated upstream:Logic_Main_Control.py
#from Image import
from PyQt5 import QtGui,QtCore
=======
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget


>>>>>>> Stashed changes:Page/Logic_Main_Control.py
target_host = "39.106.96.98"
target_port = 9998
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
userAccount = "user"

class Login(QWidget,Login.Ui_LoginP):
    def __init__(self):
        super(Login,self).__init__()
        self.setupUi(self)
        self.imageL.setPixmap(QtGui.QPixmap("Image/15562886683298.png"))
        self.jumpToRegisterP.clicked.connect(self.jumpToRegisterP_clicked)
        self.loginB_2.clicked.connect(self.loginB_clicked)

    def jumpToRegisterP_clicked(self):
        self.close()
        self.ui = Register()
        self.ui.show()

    def loginB_clicked(self):
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
<<<<<<< Updated upstream:Logic_Main_Control.py
            result = response.decode()
            print(result)
            if result == 'True':
=======
            if response:
>>>>>>> Stashed changes:Page/Logic_Main_Control.py
                userAccount = user
                self.close()
                self.ui = MainWindow()
                self.ui.show()
            else:
                QMessageBox.warning(self,'错误','您输入的密码有误',QMessageBox.Cancel)
        except Exception as e:
            QMessageBox.warning(self,"错误",e,QMessageBox.Cancel)




class Register(QWidget,Register.Ui_RegitserP):
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        self.imageL.setPixmap(QtGui.QPixmap("Image/15562886683298.png"))
        self.jumpToLoginP.clicked.connect(self.jumpToLoginP_clicked)
        self.registerB.clicked.connect(self.registerB_clicked)

    def jumpToLoginP_clicked(self):
        self.close()
        self.ui = Login()
        self.ui.show()

    def registerB_clicked(self):
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
<<<<<<< Updated upstream:Logic_Main_Control.py
                result = response.decode()
                print(result)
                if result == 'True':
=======
                if response:
>>>>>>> Stashed changes:Page/Logic_Main_Control.py
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
        try:
            msg = "askhistory %s" %('wx')
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("askHistoryReturn:%s" % (response))
            alist = response.decode().split('\'')
            num = alist[0].split('"')
            num = num[0].split('(')
            num = num[0]
            print(num)
            if num != 0:
                self.close()
                self.ui = History(alist)
                self.ui.show()
            else:
                QMessageBox.warning(self,"提示",'暂无个人历史记录',QMessageBox.Ok)
        except Exception as e:
            QMessageBox.warning(self,"错误",e,QMessageBox.Cancel)
            print(e)

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
        self.ui = StartTrain()
        self.ui.show()


class StartTrain(QWidget,StartTrain.Ui_StartTrainP):
    def __init__(self):
        super(StartTrain, self).__init__()
        self.setupUi(self)
        self.jumpToChooseP.clicked.connect(self.jumpToChooseP_clicked)
        self.startB.clicked.connect(self.startB_clicked)
        self.jumpToScoreP.clicked.connect(self.jumpToScore_clicked)
        #self.startB.clicked.connect()
        #self.btn_play.clicked.connect(self.player.play)

    def jumpToChooseP_clicked(self):
        self.close()
        self.ui = ChooseTrain()
        self.ui.show()

    def jumpToScore_clicked(self):
        try:
            # 上传训练历史记录的格式如下，u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
            #msg = "uphistory u item s dp dur date"
            msg = "uphistory %s %s %s %s %s %s" % ("wx","项目2","90","E://Video","16:00","2020/7/11")
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("upHistoryReturn:%s" % (response))
<<<<<<< Updated upstream:Logic_Main_Control.py
            result = response.decode()
            print(result)
            if result == 'True':
                QMessageBox.warning(self,'提示','上传成功',QMessageBox.Cancel)
=======
            if response:
                QMessageBox.warning(self,'提示',"分数上传成功",msg,QMessageBox.Ok)
>>>>>>> Stashed changes:Page/Logic_Main_Control.py
                self.close()
                self.ui = Score()
                self.ui.show()
            else:
                QMessageBox.warning(self,'提示','上传失败',QMessageBox.Cancel)
        except Exception as e:
            QMessageBox.warning(self, '提示',"错误", e, QMessageBox.Cancel)
            print(e)


    def startB_clicked(self):
        do = "nothing"


class Score(QWidget,Score.Ui_Score):
    def __init__(self):
        super(Score, self).__init__()
        self.setupUi(self)
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)
        self.scoreL.setText('90')
        self.suggestionL.setText('待改进')

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


class History(QWidget,History.Ui_HistoryP):
    def __init__(self,alist):
        super(History, self).__init__()
        self.setupUi(self)
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)

        num = alist[0].split('"')
        num = num[0].split('(')
        num = num[0]
        print(num)
        index = 0
        result = []
        for a in range(1, int(num) + 1):
            for b in range(1, 7):
                i = 14 * a - 11
                #result[index] =
                result.append(alist[i+2*b-2])
                #label = "iL%s" %(str(index))
<<<<<<< Updated upstream:Logic_Main_Control.py
        self.iL1.setText(result[0])
        self.iL2.setText(result[1])
        self.iL3.setText(result[2])
        self.iL4.setText(result[3])
        self.iL5.setText(result[4])
        self.iL6.setText(result[5])

=======
        self.iL1 =result[0]
        self.iL2 = result[1]
        self.iL3 = result[2]
        self.iL4 = result[3]
        self.iL5 = result[4]
        self.iL6 = result[5]
>>>>>>> Stashed changes:Page/Logic_Main_Control.py

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = QMediaPlayer()
    ui = Login()
    ui.show()
    sys.exit(app.exec_())

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = QMediaPlayer()
    vw=  QVideoWidget()                       # 定义视频显示的widget
    vw.show()
    player.setVideoOutput(vw)                 # 视频播放输出的widget，就是上面定义的
    player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
    player.play()                               # 播放视频
    sys.exit(app.exec_())
'''
