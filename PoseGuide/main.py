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
import coslike
from form import VideoBox 

so = cdll.LoadLibrary("/usr/lib/libopencv_core.so")
so = cdll.LoadLibrary("/system/3559v100_AI_libs/libNL_POSE.so")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    configPath = b"/system/3559v100_AI_model"
    libNamePath = "/system/3559v100_AI_libs/libNL_ACTIONENC.so"  # 模型名字
    box = VideoBox(libNamePath, configPath, 640, 480)
    box.show()
    sys.exit(app.exec_())
