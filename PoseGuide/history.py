#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
# 这下面的服务器连接设置是我调试使用的，和界面调用的时候请酌情注释
target_host = "39.106.96.98"
target_port = 9998
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))


def gethistory(username):
    # 查询某用户的历史记录，跟的是用户名，如果没有记录返回b'()'如果有则返回b'(记录内容)'
    # 测试数据包括
    # "uphistory u item s dp dur date"
    # "uphistory u 加油操 69 system/p 11:12 20-7-8"
    # 然后进行查询结果如下
    # b"((u'-1990937634878078585', u'u', u'\\u52a0\\u6cb9\\u64cd', u'69', u'system/p', u'11:12', u'20-7-8'), (u'-6171808383927979350', u'u', u'item', u's', u'dp', u'dur', u'date'))"
    msg="askhistory "+username
    msg=msg.encode()
    client.send(msg)
    response = client.recv(4096)
    print (response)
msg="askhistory u"
msg=msg.encode()
client.send(msg)
response = client.recv(4096)
print (response)