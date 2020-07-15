'''
Auth://作者 吴茜
Create date:///创建时间 2020.7.9
Update date://签入时间 2020.7.12
Discrip://此处须注明更新的详细内容
    完成了label的图片正确显示
    更改了路径
    完成了数据显示
'''

import socket
import sys
# from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
from PyQt5.QtWidgets import *
from Page import Login,Register,Main_Window,ChooseTrain,StartTrain,Score,History
# from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
import cv2
import globalvar
import modelload
import threading
# import video
target_host = "39.106.96.98"
target_port = 9998

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
userAccount = "user"

class Login(QWidget,Login.Ui_LoginP):
    def __init__(self):
        super(Login,self).__init__()
        self.setupUi(self)
        # self.imageL.setPixmap(QtGui.QPixmap("Image/15562886683298.png"))
        self.imageL.setPixmap(QPixmap("Image/15562886683298.png"))
        self.jumpToRegisterP.clicked.connect(self.jumpToRegisterP_clicked)
        self.loginB_2.clicked.connect(self.loginB_clicked)

    def jumpToRegisterP_clicked(self):
        self.close()
        self.ui = Register()
        self.ui.show()

    def loginB_clicked(self):
        try:
            user = self.userT.toPlainText()
            # userAccount=user
            pwd = self.pwdT.toPlainText()
            print(user)
            print(pwd)
            msg = "login %s %s" %(user, pwd)
            print(msg)
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("loginReturn:%s" %(response))
            result = response.decode()
            if result == 'True':
                global userAccount
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
                result = response.decode()
                print(result)
                if result == 'True':
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
        # self.jumpToScoreP.clicked.connect(self.close)
        self.startB.setEnabled(True)
        self.jumpToScoreP.setEnabled(False)
        self.libNamePath = "/system/3559v100_AI_libs/libNL_ACTIONENC.so"
        self.configPath = b"/system/3559v100_AI_model"
        # 线程变量初始化
        self.threadCap = None
        self.nlPose = None
        self.videoth = None
        self.capWidth = 640
        self.capHeight = 480
#       尝试播放视频
        # ui.Open.clicked.connect(self.Open)
        # ui.Close.clicked.connect(self.Close)


        # 创建一个关闭事件并设为未触发
        # self.stopEvent = threading.Event()
        # self.stopEvent.clear()
    # 尝试开始的时候用视频显示
    #     self.timer_camera = QTimer(self)
    #     self.cap = cv2.VideoCapture(0)  
    #     self.timer_camera.timeout.connect(self.show_pic)
    #     self.begin=False
    #     self.timer_camera.start(10)
    # def show_pic(self):
    #     print("kaishi")
    #     # image_resize = cv2.resize(image, (1280, 960), interpolation=cv2.INTER_CUBIC)
    #     if self.begin==False:
    #         print("begin=false")
    #         success, frame=self.cap.read()
    #         if success:
    #             show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
    #             self.label.setPixmap(QPixmap.fromImage(showImage))
    #             self.timer_camera.start(10)
    #     else:
    #         return





        # # 实现label读取视频的尝试
        # # self.timer_camera = QTimer(self)
        # # self.timer_camera.timeout.connect(self.showvedio)
        # # self.timer_camera.start(10)
        # self.cap = cv2.VideoCapture('test.mp4')
        # self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        # print("得到视频fps为："+str(self.frameRate))
        # th = threading.Thread(target=self.Display)
        # th.start()
        # # while(cap.isOpened()):
        # #     ret, frame = cap.read()
        # #     if ret:
        # #         show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # #         show=cv2.imshow('video', frame)
        # #         if cv2.waitKey(1) & 0xFF == ord('q'):
        # #             break
        # #         showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        # #         self.label.setPixmap(QPixmap.fromImage(showImage))
        # #         # self.timer_camera.start(10)
        # #         # if cv2.waitKey(1) & 0xFF == ord('q'):
        # #         #     break
        # #     else:
        # #         break
        # # cap.release()
    # def close(self):
    #     stopEvent.set()
    # def Display(self):
    #     # self.ui.Open.setEnabled(False)
    #     # self.ui.Close.setEnabled(True)

    #     while self.cap.isOpened():
    #         success, frame = self.cap.read()
    #         if success==True:
    #             # RGB转BGR
    #             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #             img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    #             self.label.setPixmap(QPixmap.fromImage(img))
    #             # if cv2.waitKey(1) & 0xFF == ord('q'):
    #             #     break
    #             # cv2.waitKey(int(1000 / self.frameRate))
    #             cv2.waitKey(100000)
    #             # 判断关闭事件是否已触发
    #             if True == self.stopEvent.is_set():
    #                 # 关闭事件置为未触发，清空显示label
    #                 self.stopEvent.clear()
    #                 self.ui.DispalyLabel.clear()
    #                 self.ui.Close.setEnabled(False)
    #                 self.ui.Open.setEnabled(True)
    #                 break

    def startB_clicked(self):
                # configPath = b"/system/3559v100_AI_model"
        # libNamePath = "/system/3559v100_AI_libs/libNL_ACTIONENC.so"  # 模型名字
        # box = VideoBox(libNamePath, configPath, 640, 480)
        # box.show()
    # def startButtonPressed(self):
        # self.info_label.setText('加载中......')
        print("clicked!")
        self.startB.setEnabled(False)
        self.jumpToScoreP.setEnabled(True)
        # self.showvedio()
        # 设置双线程
        self.frameID = 0
        self.CapIsbasy = False
        self.AlgIsbasy = False
        self.videoisbusy = False
        self.CapIsReady = False
        self.showImage = None
        self.limg = None
        # 线程1相机采集
        self.threadCap = None
        self.threadCap = modelload.ThreadCap(self)
        self.threadCap.start()

        # 线程2算法处理
        self.threadAlgorithm = None
        self.threadAlgorithm = modelload.ThreadPose(self)
        self.threadAlgorithm.updatedImage.connect(self.showframe)
        self.threadAlgorithm.start()

        # 线程3播放视频
        self.showvedio=None
        self.showvedio=modelload.videoshow(self)
        self.showvedio.start()

    def jumpToChooseP_clicked(self):
        self.close()
        self.ui = ChooseTrain()
        self.ui.show()

    def jumpToScore_clicked(self):
        try:
            self.jumpToChooseP.setEnabled(False)
            if self.threadCap:
                self.threadCap.stop()
                self.threadCap.wait()
                self.threadAlgorithm.stop()
                self.threadAlgorithm.wait()
                self.showvedio.stop()
                self.showvedio.wait()
            del self.threadCap
            del self.threadAlgorithm
            del self.showvedio

        # self.startB.setEnabled(True)
        # self.j.setEnabled(False)
            # 上传训练历史记录的格式如下，u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
            #msg = "uphistory u item s dp dur date"
            # date=datetime.date()
            date=datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            msg = "uphistory %s %s %s %s %s %s" % (userAccount,"项目1",globalvar.get_value("score"),"E://Video","16:00",date)
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("upHistoryReturn:%s" % (response))
            result = response.decode()
            print(result)
            if result == 'True':
                QMessageBox.warning(self,'提示','上传成功',QMessageBox.Cancel)
                self.close()
                self.ui = Score()
                self.ui.show()
            else:
                QMessageBox.warning(self,'提示','上传失败',QMessageBox.Cancel)
        except Exception as e:
            QMessageBox.warning(self, '提示',"错误", e, QMessageBox.Cancel)
            print(e)


    
    def showframe(self):
        # self.info_label.setText('已加载完成！')
        self.label.setPixmap(self.showImage)
        # if not self.jumpToScoreP.isEnabled():
            # self.info_label.setText('已停止！')
        

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
        self.iL1.setText(result[0])
        self.iL2.setText(result[1])
        self.iL3.setText(result[2])
        self.iL4.setText(result[3])
        self.iL5.setText(result[4])
        self.iL6.setText(result[5])


    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Login()
    ui.show()
    sys.exit(app.exec_())