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

from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import *
from Page import Login,Register,Main_Window,ChooseTrain,StartTrain,Score,History,Tabel
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

        self.imageL.setPixmap(QtGui.QPixmap("Image/patten.png"))

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
        self.imageL.setPixmap(QtGui.QPixmap("Image/patten.png"))
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
        self.imageL.setPixmap(QtGui.QPixmap("Image/patten.png"))
        self.jumpToLoginP.setIcon(QtGui.QIcon("Image/loginB.png"))
        self.jumpToChooseP.setIcon(QtGui.QIcon("Image/button1.png"))
        self.jumpToLikeP.setIcon(QtGui.QIcon("Image/button2.png"))
        self.jumpToHistoryP.setIcon(QtGui.QIcon("Image/button3.png"))

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
        '''
            try:
            msg = "askhistory %s" %(userAccount)
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

            else:
                QMessageBox.warning(self,"提示",'暂无个人历史记录',QMessageBox.Ok)
        except Exception as e:
            QMessageBox.warning(self,"错误",e,QMessageBox.Cancel)
            print(e)
        '''
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
        self.label_2.setPixmap(QtGui.QPixmap("Image/patten2.png"))
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)

        self.listWidget_1.itemClicked.connect(self.jump1)
        self.listWidget_2.itemClicked.connect(self.jump2)
        self.listWidget_3.itemClicked.connect(self.jump3)
        self.listWidget_4.itemClicked.connect(self.jump4)
        self.listWidget_5.itemClicked.connect(self.jump5)
        self.getData()

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()

    def getData(self):
        '''
        1.从数据库获取数据，然后分解
        2.将每个单元的内容改成：视频名，视频封面，视频类型，视频难度，视频介绍
        3.将‘视频封面路径，视频名，视频类型，视频难度，视频介绍’传入add中
        '''
        try:
            f = open('sposes/chooseTrain.txt', 'r', encoding='utf8', errors='ignore')
            for eachline in f.readlines():
                eachl = eachline.split('+')
                imagelt = eachl[0].strip('.mp4')
                if eachl[1] =='健身':
                    print(eachl[4])
                    self.itemAdd1(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                    self.itemAdd2(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                elif eachl[1] =='有氧操':
                    self.itemAdd1(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                    self.itemAdd3(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                elif eachl[1] =='舞蹈':
                    self.itemAdd1(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                    self.itemAdd4(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                elif eachl[1] =='拉伸':
                    self.itemAdd1(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
                    self.itemAdd5(self.add(eachl[4],eachl[1],eachl[2],eachl[3],imagelt))
        finally:
            if f:
                f.close()

    def add(self,image,l1, l2, l3,l4):
        self.imagel = QLabel()
        self.lb1 = QLabel()
        self.lb2 = QLabel()
        self.lb3 = QLabel()
        self.lb4 = QLabel()
        self.lb5 = QLabel()
        self.bt = QPushButton()
        wight = QWidget()
        # 设置属性
        image=image.rstrip()
        self.imagel.setPixmap(QtGui.QPixmap('simages/%s.png'%(image)).scaled(421,316))
        self.imagel.setFixedSize(421, 316)
        self.imagel.setObjectName('imagel')
        # self.imagel.setScaledContents(True)  # 让图片自适应label大小

        imageName = l4.split('-')
        self.lb1.setStyleSheet("background-color:#ffffff")
        self.lb1.setStyleSheet("color:#07213a")
        self.lb1.setObjectName('lb1')
        self.lb1.setText(imageName[0])
        self.lb1.setFont(QtGui.QFont("Adobe Arabic", 22, 80))

        self.lb2.setStyleSheet("background-color:#ffffff")
        self.lb2.setStyleSheet("color:#52968e")
        self.lb2.setText(l1)
        self.lb2.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        self.lb4.setStyleSheet("background-color:#ffffff")
        self.lb4.setStyleSheet("color:#52968e")
        self.lb4.setText(l2)
        self.lb4.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        self.lb3.setStyleSheet("background-color:#ffffff")
        self.lb3.setStyleSheet("color:#829cb5")
        self.lb3.setWordWrap(True)
        self.lb3.setText(l3)
        self.lb3.setFont(QtGui.QFont("Adobe Arabic", 18, 50))

        self.lb5.setObjectName('lb5')
        self.lb5.setText(image)
        self.lb5.setFont(QtGui.QFont("Adobe Arabic", 1, 50))
        self.lb5.setStyleSheet("color:#ffffff")

        self.bt.setFont(QtGui.QFont("Adobe Arabic", 20, 50))
        self.bt.setStyleSheet("color:#829cb5")
        self.bt.setObjectName('bt')
        self.bt.setText('详情')

        # 布局
        layout_main = QHBoxLayout()
        layout_middel = QVBoxLayout()
        layout_right = QVBoxLayout()

        # 添加控件
        layout_middel.addWidget(self.lb1)
        layout_middel.addWidget(self.lb2)
        layout_middel.addWidget(self.lb4)
        layout_main.addWidget(self.imagel)
        layout_main.addLayout(layout_middel)
        layout_main.addWidget(self.lb3)
        layout_right.addWidget(self.bt)
        layout_right.addWidget(self.lb5)
        layout_main.addLayout(layout_right)
        wight.setLayout(layout_main)
        self.programName=imageName[0]
        self.bt.clicked.connect(self.jumpToTabelP)
        #self.itemAdd(wight)
        return wight

    def itemAdd1(self, object):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(900, 230))
        self.listWidget_1.addItem(item)
        self.listWidget_1.setItemWidget(item, object)
        self.listWidget_1.setWrapping(True)
    def itemAdd2(self, object):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(900, 230))
        self.listWidget_2.addItem(item)
        self.listWidget_2.setItemWidget(item, object)
        self.listWidget_2.setWrapping(True)
    def itemAdd3(self, object):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(900, 230))
        self.listWidget_3.addItem(item)
        self.listWidget_3.setItemWidget(item, object)
        self.listWidget_3.setWrapping(True)
    def itemAdd4(self, object):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(900, 230))
        self.listWidget_4.addItem(item)
        self.listWidget_4.setItemWidget(item, object)
        self.listWidget_4.setWrapping(True)
    def itemAdd5(self, object):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(900, 230))
        self.listWidget_5.addItem(item)
        self.listWidget_5.setItemWidget(item, object)
        self.listWidget_5.setWrapping(True)

    def jump1(self):
        windows = self.listWidget_1.currentItem()
        print(type(windows))
        widget = self.listWidget_1.itemWidget(windows)
        print(type(widget))
        item = widget.findChild(QLabel, 'lb5')
        print(type(item))
        if item:
            # 这个地方负责传参数给startTrain界面，参数为（正面长.json,侧面长.json）
            temp = item.text()
            # print(temp)
            t = temp.split('-')
            prm1 = "%s.json" %(temp)
            #prm2 = "%s-%s-%s-%s.json" % (t[0], t[1], '侧', '长')
            print(prm1)
            #print(prm2)
            self.close()
            self.ui = StartTrain(prm1)
            self.ui.show()
        else:
            print('didnt find')
    def jump2(self):
        windows = self.listWidget_2.currentItem()
        print(type(windows))
        widget = self.listWidget_2.itemWidget(windows)
        print(type(widget))
        item = widget.findChild(QLabel, 'lb5')
        print(type(item))
        if item:
            # 这个地方负责传参数给startTrain界面，参数为（正面长.json,侧面长.json）
            temp = item.text()
            # print(temp)
            t = temp.split('-')
            prm1 = "%s.json" %(temp)
            prm2 = "%s-%s-%s-%s.json" % (t[0], t[1], '侧', '长')
            print(prm1)
            print(prm2)
            self.close()
            self.ui = StartTrain(prm1)
            self.ui.show()
        else:
            print('didnt find')
    def jump3(self):
        windows = self.listWidget_3.currentItem()
        print(type(windows))
        widget = self.listWidget_3.itemWidget(windows)
        print(type(widget))
        item = widget.findChild(QLabel, 'lb5')
        print(type(item))
        if item:
            # 这个地方负责传参数给startTrain界面，参数为（正面长.json,侧面长.json）
            temp = item.text()
            # print(temp)
            t = temp.split('-')
            prm1 = "%s.json" %(temp)
            prm2 = "%s-%s-%s-%s.json" % (t[0], t[1], '侧', '长')
            print(prm1)
            print(prm2)
            self.close()
            self.ui = StartTrain(prm1)
            self.ui.show()
        else:
            print('didnt find')
    def jump4(self):
        windows = self.listWidget_4.currentItem()
        print(type(windows))
        widget = self.listWidget_4.itemWidget(windows)
        print(type(widget))
        item = widget.findChild(QLabel, 'lb5')
        print(type(item))
        if item:
            # 这个地方负责传参数给startTrain界面，参数为（正面长.json,侧面长.json）
            temp = item.text()
            # print(temp)
            t = temp.split('-')
            prm1 = "%s.json" %(temp)
            prm2 = "%s-%s-%s-%s.json" % (t[0], t[1], '侧', '长')
            print(prm1)
            print(prm2)
            self.close()
            self.ui = StartTrain(prm1)
            self.ui.show()
        else:
            print('didnt find')
    def jump5(self):
        windows = self.listWidget_5.currentItem()
        print(type(windows))
        widget = self.listWidget_5.itemWidget(windows)
        print(type(widget))
        item = widget.findChild(QLabel, 'lb5')
        print(type(item))
        if item:
            # 这个地方负责传参数给startTrain界面，参数为（正面长.json,侧面长.json）
            temp = item.text()
            # print(temp)
            t = temp.split('-')
            prm1 = "%s.json" %(temp)
            prm2 = "%s-%s-%s-%s.json" % (t[0], t[1], '侧', '长')
            print(prm1)
            print(prm2)
            self.close()
            self.ui = StartTrain(prm1)
            self.ui.show()
        else:
            print('didnt find')

    def jumpToTabelP(self):
        self.close()
        self.ui = Tabel(self.projectName)
        self.ui.show()


class StartTrain(QWidget,StartTrain.Ui_StartTrainP):
    def __init__(self,json1):
        super(StartTrain, self).__init__()
        self.setupUi(self)
        self.json1 = json1
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

        #获取正面视频文件名
        tempVideo = self.json1.strip('.json')
        video ='%s.mp4'%(tempVideo)
        # 线程3播放视频
        self.showvedio=None
        self.showvedio=modelload.videoshow(self,video)
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
                self.threadAlgorithm.stop(self.json1)
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
            tempVideo = self.json1.strip('.json')
            video = '%s.mp4' % (tempVideo)
            temp = self.json1.split('-')
            projectName = temp[0]
            msg = "uphistory %s %s %s %s %s %s %s %s" % (userAccount,projectName,globalvar.get_value("score"),"sposes/%s.mp4"%(video),"16:00",date,globalvar.get_value("comment"),globalvar.get_value("part_scores"))

            # msg = "uphistory %s %s %s %s %s %s" % (userAccount,"项目1",globalvar.get_value("score"),"E://Video","16:00",date)
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            print("upHistoryReturn:%s" % (response))
            result = response.decode()
            print(result)
            if result == 'True':
                QMessageBox.warning(self,'提示','上传成功',QMessageBox.Cancel)
                self.close()
                self.ui = Score(globalvar.get_value("score"),globalvar.get_value("comment"),globalvar.get_value("part_scores"))
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
    def __init__(self,allscore,comment,partScore):
        super(Score, self).__init__()
        self.setupUi(self)
        #self.allscore = allscore
        #self.score1 =score1
        #self.score2 =score2
        #self.score3 =score3
        #self.score4 =score4
        #self.score5 =score5
        #self.comment = comment
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)
        self.imagL.setPixmap(QtGui.QPixmap("Image/patten4.png"))
        self.scoreL.setText(allscore)
        self.headl.setText(partScore['头部'])
        self.lefthandL.setText(partScore['左臂'])
        self.righthandL.setText(partScore['右臂'])
        self.leftlegL.setText(partScore['左腿'])
        self.rightlegL.setText(partScore['右腿'])
        self.commentL.setText(comment)

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()


class History(QWidget,History.Ui_HistoryP):
    def __init__(self,alist):
        super(History, self).__init__()
        self.setupUi(self)
        self.imageL.setPixmap(QtGui.QPixmap("Image/patten3.png"))
        self.jumpToMainWindowP.clicked.connect(self.jumpToMainWindowP_clicked)
        #目前的添加只考虑了添加1条的情况，多条数据分解，需要与数据库结合考虑
        self.getDate()
    # "uphistory u item s dp dur date"

    def divide(self,result):
        num =len(result)
        for i in range(0,num):
            self.record(result[i][0],result[i][1],result[i][2],result[i][7],result[i][4],result[i][5])

    def getDate(self):
        try:
            msg = "askhistory %s" % (userAccount)
            msg = msg.encode()
            client.send(msg)
            response = client.recv(4096)
            #转为元组
            result = eval(response)
            return result
        except Exception as e:
            print(e)

    def record(self,alist):
        #分解数据
        num = alist[0].split('"')
        num = num[0].split('(')
        num = num[0]
        result = []
        for a in range(1, int(num) + 1):
            for b in range(1, 7):
                i = 14 * a - 11
                result.append(alist[i + 2 * b - 2])
        for i in range(1,num):
            for j in range(0,6):
                '''
                获取数据库传来的数据，需要整理为（用户，项目名，总分，（部位得分），时长，日期）
                '''
                self.add()
        #显示再界面上

    def add(self,lb1,lb2,lb3,lb4,lb5,lb6):
        lb0 = QLabel(lb1)
        lb1 = QLabel(lb2)
        lb2 = QLabel(lb3)
        lb3 = QLabel(lb4)
        lb4 = QLabel(lb5)
        lb5 = QLabel(lb6)
        wight = QWidget()
        layoutH = QHBoxLayout()

        lb0.setStyleSheet("color:#07213a")
        lb0.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        lb1.setStyleSheet("color:#07213a")
        lb1.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        lb2.setStyleSheet("color:#07213a")
        lb2.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        lb3.setStyleSheet("color:#07213a")
        lb3.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        lb4.setStyleSheet("color:#07213a")
        lb4.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        lb5.setStyleSheet("color:#07213a")
        lb5.setFont(QtGui.QFont("Adobe Arabic", 20, 50))

        layoutH.addWidget(lb0)
        layoutH.addWidget(lb1)
        layoutH.addWidget(lb2)
        layoutH.addWidget(lb3)
        layoutH.addWidget(lb4)
        layoutH.addWidget(lb5)
        wight.setLayout(layoutH)

        #添加列表值
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(1140, 80))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, wight)
        #self.listWidget.setWrapping(True)

    def jumpToMainWindowP_clicked(self):
        self.close()
        self.ui = MainWindow()
        self.ui.show()

    def itemAdd(self, object):
        item = QListWidgetItem()
        item.setSizeHint(QtCore.QSize(620, 70))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, object)

class Tabel(QWidget,Tabel.Ui_TabelP):
    def __init__(self,projectName):
        super(Tabel, self).__init__()
        self.setupUi(self)
        self.imageL.setPixmap(QtGui.QPixmap("Image/patten2.png"))
        self.jumpToChooseP.clicked.connect(self.jumpToChooseP_clicked)

    def jumpToChooseP_clicked(self):
        self.close()
        self.ui = ChooseTrain()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Login()
    ui.show()
    sys.exit(app.exec_())