#!/usr/bin/env python
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

