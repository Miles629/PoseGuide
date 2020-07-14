#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Auth://作者 张智敏
Create date:///创建时间 2020.7.9
Update date://签入时间 2020.7.11
Discrip://这里是为了解决跨文件传输分数的问题，使训练界面文件中得到的分数能够传递回主函数界面，目前代码结构先这样，后续更改
'''
def _init():
    global _global_dict
    _global_dict = {}
# 创建全局变量
def set_value(name, value):
    _global_dict[name] = value
# 获取全局变量
def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue