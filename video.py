# -*- coding: utf-8 -*-
import numpy as np
import cv2
from time import sleep
import sys
import cv2
import os
# class videoshow(object):
#     def __init__(self):
#         print("视频播放")
#     def __del__(self):
#         self.wait()
#     def run(self):
#         if videoisbusy ==False:
#             cap = cv2.VideoCapture('test.mp4') ###修改路径
#             cv2.namedWindow("video", 0)
#             cv2.resizeWindow("video", 1920, 1080)
#             while(cap.isOpened()):
#                 ret, frame = cap.read()
#                 if ret == True:
#                     cv2.imshow('video', frame)
#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                         break
#                 else:
#                     break
#             cap.release()
#             cv2.destroyAllWindows()
#     def stop(self):
#         cap.release()
#         cv2.destroyAllWindows()
print("视频播放")
cap = cv2.VideoCapture('test.mp4') ###修改路径
cv2.namedWindow("video", 0)
cv2.resizeWindow("video", 1920, 1080)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

