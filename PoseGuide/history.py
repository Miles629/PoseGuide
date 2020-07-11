#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
# 这下面的服务器连接设置是我调试使用的，和界面调用的时候请酌情注释
target_host = "39.106.96.98"
target_port = 9998
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))


def askhistory(username):
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
    # response=response.encode()
    # 想方设法将返回的信息中的历史记录总条数给提取出来
    alist=response.decode().split('\'')
    num=alist[0].split('"')
    num=num[0].split('(')
    num=num[0]
    # print(num)

    # i=0
    # for a in alist:
    #     print(str(i)+":"+a)
    #     i=i+1
    # 用户有用的历史信息用户名3,项目名5,分数7,存储数据路径9，持续时间11，训练日期13；；；
    # 第二个则从17开始依次加2,对应用户名17，项目名19.......
    for a in range(1,int(num)+1):
        for b in range(1,7):
            i=14*a-11
            print(alist[i+2*b-2])
    # 上面是一个例子，调用这个函数返回的是alist，里面有用的数据就是用这个for循环得到
    return alist