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
import structdef

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
        self.PACT.NL_ACTION_Command.argtypes = (POINTER(structdef.Struct_Handle), c_char_p)
        self.PACT.NL_ACTION_Command.restype = c_int
        self.PACT.NL_ACTION_Process.argtypes = (POINTER(structdef.Struct_Handle),
                                                POINTER(structdef.Struct_ACT_VarIn),
                                                POINTER(structdef.Struct_ACT_VarOut))
        self.PACT.NL_ACTION_Process.restype = c_int
        self.PACT.NL_ACTION_UnloadModel.argtypes = (POINTER(structdef.Struct_Handle),)
        self.PACT.NL_ACTION_UnloadModel.restype = c_int

        # 初始化：结构体变量和函数
        self.djACTHandle = structdef.Struct_Handle()  # 结构体变量定义
        self.djACTVarIn = structdef.Struct_ACT_VarIn()  # 结构体变量定义
        self.djACTVarOut = structdef.Struct_ACT_VarOut()  # 结构体变量定义

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