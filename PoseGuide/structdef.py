import sys
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


