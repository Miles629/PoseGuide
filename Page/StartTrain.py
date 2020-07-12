# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StartTrain.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Auth://作者 吴茜
Create date:///创建时间 2020.7.9
Update date://签入时间 2020.7.11
Discrip://此处须注明更新的详细内容
    CLass Ui_StartTrain()为前端代码部分
'''

import sys
import cv2
import os
import numpy as np
import datetime
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore, QtWidgets
import threading
from threading import Timer, Thread, Event
from ctypes import *
from coslike import *
from datetime import datetime
import globalvar as gl
so = cdll.LoadLibrary("/usr/lib/libopencv_core.so")
so = cdll.LoadLibrary("/system/3559v100_AI_libs/libNL_POSE.so")
json_result={}
# from PyQt5 import QtCore, QtGui, QtWidgets
score=10
gl._init()

# 结构体定义
class Struct_Handle(Structure):  # NLDJ_ACTION_Handle
    _fields_ = [("pvModel", c_void_p)]


class Struct_ACT_VarIn(Structure):  # NLDJ_ACTION_VarIn
    _fields_ = [("pubyIm", POINTER(c_ubyte)), ("dwWidth", c_int), ("dwHeight", c_int), ("dwChannel", c_int)]


class Struct_POS(Structure):  # NL_Pose_POS
    _fields_ = [("x", c_float), ("y", c_float), ("p_score", c_float)]


class Struct_ACT_Info(Structure):  # NLDJ_ACPRED_Infor
    _fields_ = [("dwPoseNum", c_int), ("fPosePos", Struct_POS * 100), ("pdwBowHead", c_int),
                ("pdwHandUp", c_int), ("pdwStandUp", c_int), ("pdwBendOverDesk", c_int), ("pdwPlayPhone", c_int),
                ("pdwStudy", c_int)]


class Struct_UP_Pos(Structure):  # NL_upbodyPos
    _fields_ = [("x", c_int), ("y", c_int), ("height", c_int), ("width", c_int)]


class Struct_ACT_VarOut(Structure):  # NLDJ_ACTION_VarOut
    _fields_ = [("dwPersonNum", c_int), ("pdjActionInfors", Struct_ACT_Info * 64), ("pdjUpBodyPos", Struct_UP_Pos * 64),
                ("bUpBodyPosTrue", c_bool * 64)]


# POSE_PAIRS
gPosePairs = [1, 2, 1, 5, 2, 3, 3, 4, 5, 6, 6, 7, 1, 8, 8, 9, 9, 10, 1,
              11, 11, 12, 12, 13, 1, 0, 0, 14, 14, 16, 0, 15, 15, 17]

# POSE_COLORS
gColors = [255, 0, 85, 255, 0, 0, 255, 85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,
           85, 255, 0, 0, 255, 0, 0, 255, 85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,
           85, 255, 0, 0, 255, 255, 0, 170, 170, 0, 255, 255, 0, 255, 85, 0, 255]

class NL_Pose(object):
    """docstring for NlPose"""

    def __init__(self, libNamePath):
        if not os.path.exists(libNamePath):
            print("library file not exit!", libNamePath)
            quit()
            return -1001
        else:
            self.PACT = cdll.LoadLibrary(libNamePath)  # linux版本

        # 指定函数参数类型
        self.PACT.NL_ACTION_Command.argtypes = (POINTER(Struct_Handle), c_char_p)
        self.PACT.NL_ACTION_Command.restype = c_int
        self.PACT.NL_ACTION_Process.argtypes = (POINTER(Struct_Handle),
                                                POINTER(Struct_ACT_VarIn),
                                                POINTER(Struct_ACT_VarOut))
        self.PACT.NL_ACTION_Process.restype = c_int
        self.PACT.NL_ACTION_UnloadModel.argtypes = (POINTER(Struct_Handle),)
        self.PACT.NL_ACTION_UnloadModel.restype = c_int

        # 初始化：结构体变量和函数
        self.djACTHandle = Struct_Handle()  # 结构体变量定义
        self.djACTVarIn = Struct_ACT_VarIn()  # 结构体变量定义
        self.djACTVarOut = Struct_ACT_VarOut()  # 结构体变量定义

    def NL_Pose_ComInit(self, configPath):
        if not os.path.exists(configPath):
            print("Config or model file not exit!")
            return -2501
        ret = self.PACT.NL_ACTION_Command(self.djACTHandle, configPath)
        if ret != 0:
            print("Command error code:", ret)
            return ret
        return ret

    def NL_Pose_InitVarIn(self, imgInput):
        # 输入参数设置
        imgResize = cv2.resize(imgInput, (1280, 960), interpolation=cv2.INTER_CUBIC)
        img_len = len(imgResize.shape)
        if img_len == 3:
            src_RGB = imgResize
        else:
            src_RGB = cv2.cvtColor(imgResize, cv2.COLOR_GRAY2BGR)
        h, w, c = src_RGB.shape
        self.djACTVarIn.dwChannel = c
        self.djACTVarIn.dwWidth = w
        self.djACTVarIn.dwHeight = h
        self.djACTVarIn.pubyIm = src_RGB.ctypes.data_as(POINTER(c_ubyte))  # src_RGB.astype(np.uint8).tostring()
        if h > 1:
            return 0
        else:
            print("Init VarIn Error!")
            return -3001

    def NL_Pose_Process_C(self):
        # 处理函数
        try:
            ret = self.PACT.NL_ACTION_Process(self.djACTHandle, self.djACTVarIn, self.djACTVarOut)
        except Exception as e:
            print(e)
        if ret != 0:
            print("Process Error code:", ret)
            return ret
        return int(self.djACTVarOut.dwPersonNum)

    def NL_Pose_Exit(self):
        ret = self.PACT.NL_ACTION_UnloadModel(self.djACTHandle)
        if ret != 0:
            print("UnloadModel Error code:", ret)
            return ret
        return ret


# 线程，算法处理
class ThreadPose(QThread):
    updatedImage = QtCore.pyqtSignal(int)

    def __init__(self, mw):
        self.mutex = QMutex()
        self.mw = mw
        # print(os.system("pstree -p " + str(os.getpid())))
        self.nlPose = None
        self.working = True
        self.isInit = False
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def myInit(self):
        if not self.isInit:
            self.nlPose = NL_Pose(self.mw.libNamePath)
            if self.nlPose == -1001:
                print('NL_Pose Error code:', self.nlPose)
                quit()
            ret = self.nlPose.NL_Pose_ComInit(self.mw.configPath)  # 初始化
            if ret != 0:
                print('ComInit Error code:', ret)
            self.isInit = True

#-----------------------------------------------------------------
    def coslike(self,spath,upath):
        # 标准视频和用户视频相似度比较 
        # spath:标准视频json数据路径；upath:用户视频json数据路径
        match=Coslike(spath,upath)
        return match.getLikeness()


#-----------------------------------------------------------------
    def run(self):
        self.myInit()
        # json_result={} #输出的json结果
        findex=0  #帧序号，从0开始，用于文件输出
        while self.working:
            self.mutex.lock()
            if self.mw.AlgIsbasy == False and not (self.mw.limg is None):
                self.mw.AlgIsbasy = True
                limg = self.mw.limg
                ret = self.nlPose.NL_Pose_InitVarIn(limg)
                if ret == 0:
                    ret = self.nlPose.NL_Pose_Process_C()  # 返回值是目标个数
                    # start = cv2.getTickCount()
                    # end = cv2.getTickCount()
                    # during = (end - start) / cv2.getTickFrequency()
                    # print('time used:' + str(during))
                    if ret > 0:
                        # 显示结果到图片上
                        height, width, bytesPerComponent = limg.shape
                        bytesPerLine = bytesPerComponent * width
                        rgb = cv2.cvtColor(limg, cv2.COLOR_BGR2RGB)
                        # 人脸检测结果输出
                        lineType = 8
                        threshold = 0.05
                        numberColors = len(gColors)
                        # 检查结果输出
                        json_result[str(findex)+".jpg"]={} # 构造json,初始化某一帧
                        # json_result[str(findex)+".jpg"]["fIndex"]=findex # 构造json,初始化某一帧的帧序号

                        for i in range(int(self.nlPose.djACTVarOut.dwPersonNum)):
                            djActionInfors = self.nlPose.djACTVarOut.pdjActionInfors[i]
                            # 【改】↓json文件输出相关
                            json_result[str(findex)+".jpg"]["people"+str(i)]=[] # 构造json,初始化某一人
                            for j in range(18): # 构造json,填充每一帧骨骼数据
                                json_result[str(findex)+".jpg"]["people"+str(i)].append(djActionInfors.fPosePos[j].x)
                                json_result[str(findex)+".jpg"]["people"+str(i)].append(djActionInfors.fPosePos[j].y)
                                json_result[str(findex)+".jpg"]["people"+str(i)].append(djActionInfors.fPosePos[j].p_score)

                            # 绘制关节点
                            for pose in range(djActionInfors.dwPoseNum):
                                djfPosePos = djActionInfors.fPosePos[pose]

                                if djfPosePos.p_score > threshold:
                                    centerPoint = (int(djfPosePos.x), int(djfPosePos.y))  # 关节点坐标

                                    #colorIndex = pose * 3
                                    # color = (
                                    # gColors[(colorIndex + 2) % numberColors], gColors[(colorIndex + 1) % numberColors],
                                    # gColors[colorIndex % numberColors])
                                    cv2.circle(rgb, centerPoint, 3, (0,255,0), 1, lineType)
                            # 绘制关节点连线
                            for pair in range(0, len(gPosePairs), 2):
                                fPosePos1 = djActionInfors.fPosePos[gPosePairs[pair]]
                                fPosePos2 = djActionInfors.fPosePos[gPosePairs[pair + 1]]
                                if (fPosePos1.p_score > threshold) and (fPosePos2.p_score > threshold):
                                    # colorIndex = gPosePairs[pair + 1] * 3
                                    # color = (gColors[(colorIndex + 2) % numberColors],
                                    #          gColors[(colorIndex + 1) % numberColors],
                                    #          gColors[colorIndex % numberColors])
                                    LineScaled = 5
                                    keypoint1 = (int(fPosePos1.x), int(fPosePos1.y))
                                    keypoint2 = (int(fPosePos2.x), int(fPosePos2.y))
                                    cv2.line(rgb, keypoint1, keypoint2, (0,255,0), LineScaled, lineType)

                            # 绘制上半身矩形框
                            # RectPoint1 = (
                            # self.nlPose.djACTVarOut.pdjUpBodyPos[i].x, self.nlPose.djACTVarOut.pdjUpBodyPos[i].y)
                            # RectPoint2 = (
                            # self.nlPose.djACTVarOut.pdjUpBodyPos[i].x + self.nlPose.djACTVarOut.pdjUpBodyPos[i].width,
                            # self.nlPose.djACTVarOut.pdjUpBodyPos[i].y + self.nlPose.djACTVarOut.pdjUpBodyPos[i].height)
                            # cv2.rectangle(rgb, RectPoint1, RectPoint2, (200, 0, 125), 5, 8)

                        findex=findex+1
                        showImage = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)
                        self.mw.showImage = QPixmap.fromImage(showImage)
                        self.updatedImage.emit(self.mw.frameID)
                    else:
                        # 显示结果到图片上
                        print('No object:', ret)
                        height, width, bytesPerComponent = limg.shape
                        bytesPerLine = bytesPerComponent * width
                        rgb = cv2.cvtColor(limg, cv2.COLOR_BGR2RGB)
                        showImage = QImage(rgb.data, width, height, bytesPerLine, QImage.Format_RGB888)
                        self.mw.showImage = QPixmap.fromImage(showImage)
                        self.updatedImage.emit(self.mw.frameID)
                else:
                    print('Var Init Error code:', ret)
                    sleep(0.001)
                self.mw.AlgIsbasy = False

            else:
                sleep(0.001)
            # 写json文件
            # filename=
            json_result["fnum"]=findex
            # with open(os.path.join('/system/ftproot/aa/pydemo/poses/',"json_result2.json"),'w') as output_file:
            #     json.dump(json_result,output_file)
            # # 返回评分结果[标准路径（前）为该动作的数据路径，用户路径（后）为该训练的数据路径，通过数据库获取]
            # score=self.coslike()
            self.mutex.unlock()


    def stop(self):  # 重写stop方法
        self.working = False
        self.mutex.lock()
        if self.isInit:
            self.nlPose.NL_Pose_Exit()
        self.mutex.unlock()
        print('算法线程退出了')
        filename="u_"+datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+".json"
        with open(os.path.join('./poses/',filename),'w') as output_file:
            json.dump(json_result,output_file)
        # 返回评分结果
        spath='./poses/json_result2.json' # 标准动作数据，调用的时候改为该动作标准数据路径
        upath='./poses/'+filename # 本次摄像头读取的用户数据
        global score
        score=self.coslike(spath,upath) # 这个是输出的得分
        print(score)
        gl.set_value("score",score)



# 线程读取摄像机
class ThreadCap(QThread):
    updatedCap = QtCore.pyqtSignal(int)

    def __init__(self, mw):
        self.mw = mw
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.mw.capWidth)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.mw.capHeight)
        self.working = True
        self.mutex = QMutex()
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while self.working:
            self.mutex.lock()
            QApplication.processEvents()
            if not self.mw.CapIsbasy:
                # 采集图像的过程中
                self.mw.CapIsbasy = True
                ret, image = self.cap.read()  # 获取新的一帧图片
                if not ret:
                    print("Capture Image Failed")
                    self.mw.isthreadActiv = False
                    self.mw.CapIsbasy = False
                    continue
                height = image.shape[0]
                width = image.shape[1]
                if height != 960 or width != 1280:
                    image_resize = cv2.resize(image, (1280, 960), interpolation=cv2.INTER_CUBIC)
                else:
                    image_resize = image
                img_len = len(image_resize.shape)
                if img_len == 3:
                    self.mw.limg = image_resize
                else:
                    self.mw.limg = cv2.cvtColor(image_resize, cv2.COLOR_GRAY2BGR)
                self.mw.CapIsbasy = False
                self.updatedCap.emit(self.mw.frameID)
            else:
                sleep(1.0 / 50)
            self.mutex.unlock()


    def stop(self):
        self.working = False
        self.mutex.lock()
        if not (self.cap is None):
            self.cap.release()
        self.cap = None
        self.mutex.unlock()
        print('摄像机线程退出了')
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

        self.startB.setEnabled(True)
        self.jumpToScoreP.setEnabled(False)
        self.libNamePath = "/system/3559v100_AI_libs/libNL_ACTIONENC.so"
        self.configPath = b"/system/3559v100_AI_model"
        # 线程变量初始化
        self.threadCap = None
        self.nlPose = None
        self.startB.clicked.connect(self.startBPressed)
        self.jumpToScoreP.clicked.connect(self.jumpToScoreP_clicked)
        self.capWidth = 640
        self.capHeight = 480

    def retranslateUi(self, StartTrainP):
        _translate = QtCore.QCoreApplication.translate
        StartTrainP.setWindowTitle(_translate("StartTrainP", "Form"))
        self.label.setText(_translate("StartTrainP", "整个画布大小用于显示摄像头的内容，由于还不能实现录制结束自动跳转，所以用完成录制按钮跳转到评分界面(现在只用了一个label，显示出摄影图片可能还需要改变该控件的内容)"))
        self.jumpToScoreP.setText(_translate("StartTrainP", "完成录制"))
        self.startB.setText(_translate("StartTrainP", "开始录制"))
        self.jumpToChooseP.setText(_translate("StartTrainP", "返回选择训练界面"))
    
    def startBPressed(self):
        # configPath = b"/system/3559v100_AI_model"
        # libNamePath = "/system/3559v100_AI_libs/libNL_ACTIONENC.so"  # 模型名字
        # box = VideoBox(libNamePath, configPath, 640, 480)
        # box.show()
    # def startButtonPressed(self):
        # self.info_label.setText('加载中......')
        print("clicked!")
        self.startB.setEnabled(False)
        self.jumpToScoreP.setEnabled(True)
        # 设置双线程
        self.frameID = 0
        self.CapIsbasy = False
        self.AlgIsbasy = False
        self.showImage = None
        self.limg = None
        # 线程1相机采集
        self.threadCap = None
        self.threadCap = ThreadCap(self)
        self.threadCap.start()

        # 线程2算法处理
        self.threadAlgorithm = None
        self.threadAlgorithm = ThreadPose(self)
        self.threadAlgorithm.updatedImage.connect(self.showframe)
        self.threadAlgorithm.start()

    def showframe(self):
        # self.info_label.setText('已加载完成！')
        self.label.setPixmap(self.showImage)
        # if not self.jumpToScoreP.isEnabled():
            # self.info_label.setText('已停止！')
    def jumpToScoreP_clicked(self):
        if self.threadCap:
            self.threadCap.stop()
            self.threadCap.wait()
            self.threadAlgorithm.stop()
            self.threadAlgorithm.wait()
        del self.threadCap
        del self.threadAlgorithm
        # self.startB.setEnabled(True)
        # self.j.setEnabled(False)
