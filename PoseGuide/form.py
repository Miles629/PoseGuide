# -*- coding: utf-8 -*-
import sys
import cv2
import os
import numpy as np
import datetime
import math
import json
from time import sleep
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore, QtWidgets
import threading
from threading import Timer, Thread, Event
from ctypes import *
from camera import ThreadCap
from NL_pose import NL_Pose
from camera import ThreadCap


# POSE_PAIRS
gPosePairs = [1, 2, 1, 5, 2, 3, 3, 4, 5, 6, 6, 7, 1, 8, 8, 9, 9, 10, 1,
              11, 11, 12, 12, 13, 1, 0, 0, 14, 14, 16, 0, 15, 15, 17]

# POSE_COLORS
gColors = [255, 0, 85, 255, 0, 0, 255, 85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,
           85, 255, 0, 0, 255, 0, 0, 255, 85, 0, 255, 170, 0, 255, 255, 0, 170, 255, 0,
           85, 255, 0, 0, 255, 255, 0, 170, 170, 0, 255, 255, 0, 255, 85, 0, 255]

class VideoBox(QWidget):
    def __init__(self, libNamePath, configPath, capWidth, capHeight):
        QWidget.__init__(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.move(0, 0)
        self.pictureLabel = QLabel()
        self.pictureLabel.setObjectName("Picture")
        self.pictureLabel.setScaledContents(True)

        # 设置按钮组件 QPushButton
        self.stopButton = QPushButton("Stop")
        self.stopButton.setMaximumSize(QtCore.QSize(150, 60))
        self.stopButton.setEnabled(True)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.stopButton.clicked.connect(self.stopButtonPressed)

        # 设置按钮组件 QPushButton
        self.playButton = QPushButton("start")
        self.playButton.setMaximumSize(QtCore.QSize(150, 60))
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.startButtonPressed)

        # 信息提示
        self.info_label = QLabel()
        self.info_label.setText('')
        self.info_label.setMaximumSize(QtCore.QSize(150, 60))

        # 设置按键大小边框 QHBoxLayout
        control_box = QHBoxLayout()
        control_box.setContentsMargins(0, 0, 0, 0)
        control_box.addWidget(self.playButton)
        control_box.addWidget(self.info_label)
        control_box.addWidget(self.stopButton)

        layout = QVBoxLayout()
        layout.addWidget(self.pictureLabel)
        layout.addLayout(control_box)
        self.setLayout(layout)

        self.capWidth = capWidth
        self.capHeight = capHeight
        self.libNamePath = libNamePath
        self.configPath = configPath
        # 线程变量初始化
        self.threadCap = None
        self.nlPose = None
    def startButtonPressed(self):
        self.info_label.setText('加载中......')
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(True)
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
        self.info_label.setText('已加载完成！')
        self.pictureLabel.setPixmap(self.showImage)
        if not self.stopButton.isEnabled():
            self.info_label.setText('已停止！')

    def stopButtonPressed(self):
        if self.threadCap:
            self.threadCap.stop()
            self.threadCap.wait()
            self.threadAlgorithm.stop()
            self.threadAlgorithm.wait()
        del self.threadCap
        del self.threadAlgorithm
        self.playButton.setEnabled(True)
        self.stopButton.setEnabled(False)


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

#-----------------------------------------------------------------
    def run(self):
        self.myInit()
        findex=0 #帧序号，从0开始，用于文件输出
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
                        json_result={} #用于文件输出
                        # json_result[str(findex)]={}
                        for i in range(int(self.nlPose.djACTVarOut.dwPersonNum)):
                            djActionInfors = self.nlPose.djACTVarOut.pdjActionInfors[i]
                            # 【改】↓

                            json_result["people"+str(i)]=[] #初始化某一人
                            for j in range(18):
                                json_result["people"+str(i)].append(djActionInfors.fPosePos[j].x)
                                json_result["people"+str(i)].append(djActionInfors.fPosePos[j].y)
                                json_result["people"+str(i)].append(djActionInfors.fPosePos[j].p_score)

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
                        filename="fPose"+str(findex)+".json"
                        with open(os.path.join('/system/ftproot/aa/',filename),'w') as output_file:
                            output_file.write(str(json_result))
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
            self.mutex.unlock()


    def stop(self):  # 重写stop方法
        self.working = False
        self.mutex.lock()
        if self.isInit:
            self.nlPose.NL_Pose_Exit()
        self.mutex.unlock()
        print('算法线程退出了')

