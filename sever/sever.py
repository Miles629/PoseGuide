#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auth:马草原//作者
# Create date:2020-07-07///创建时间
# Update date:2020-07-10//签入时间
# Discrip:基本完成了后台服务器的响应功能，用于执行客户端发送过来的命令，并把执行结果返回给客户端//此处须注明更新的详细内容
import socket, traceback, subprocess
import string
import linksql
from datetime import datetime
# 设置服务器监听端口9998
host = '0.0.0.0'
port = 9998
#  连接阿里云的rds数据库
DbHandle = linksql.DataBaseHandle('rm-bp199ck9jt24iu4g8lo.mysql.rds.aliyuncs.com', 'kid', 'Kidofstudio', 'userinfo',
                                  3306)
# 创建socket连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)
# 开始循环监听
while 1:
    try:
        client_socket, client_addr = s.accept()
    except Exception, e:
        traceback.print_exc()
        continue

    try:
        print
        'From host:', client_socket.getpeername()
        while 1:
            # 接收socket连接中传输来的信息
            command = client_socket.recv(4096)
            if not len(command):
                break
            print
            # 打印出前端发送的信息来方便调试
            client_socket.getpeername()[0] + ':' + str(command)
            command = str(command)
            # 分割前端信息，获取有用的参数
            com = command.split()
            # 根据前端发送信息的不同的请求来进行操作
            if (com[0] == "login"):
                print("user" + com[1] + "key" + com[2])
                # 这里查询数据库验证用户名密码
                result = DbHandle.selectDblogin(com[1], com[2])
                if (result == True):
                    client_socket.send("True")
                else:
                    client_socket.send("False")
            if (com[0] == "signin"):
                # DbHandle.insertDB("insert into userkey(username,key,lasttime) values('%s','%s')"%(str(com[1]),str(com[2])))
                print("user" + com[1] + "key" + com[2] + "email" + com[3])
                result = DbHandle.insertDBsign(com[1], com[2], com[3])
                if (result == True):
                    client_socket.send("True")
                else:
                    client_socket.send("False")
            if (com[0] == "uphistory"):
                print("user" + com[1])
                # 查询该用户历史记录
                # 客户端发送指令需要按照顺序发送，空格分开，从1到7分别是u用户名item训练项目s分数date训练日期ccomment评论partscores分部位评分ttype类型
                date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
                result = DbHandle.insertDBhistory(com[1], com[2], com[3], date, com[4], com[5], com[6])
                if (result == True):
                    client_socket.send("True")
                else:
                    client_socket.send("False")
            if (com[0] == "askhistory"):
                print("user" + com[1])
                result = DbHandle.selectDbhistory(com[1])
                client_socket.send(str(result))
            if (com[0] == 'selectDbhistoryForRank'):
                result = DbHandle.selectDbhistoryForRank()
                client_socket.send(str(result))
            if (com[0] == 'selectDbhistoryForCount'):
                result = DbHandle.selectDbhistoryForCount()
                client_socket.send(str(result))
            if (com[0] == 'insertcollection'):
                result = DbHandle.insertDBcollections(com[1], com[2], com[3], com[4], com[5], com[6])
                client_socket.send(str(result))
            if (com[0] == 'askcollections'):
                result = DbHandle.selectDbcollections(com[1])
                client_socket.send(str(result))

            # 执行客户端传递过来的命令，现在已经弃用，备注作为备份
            # handler = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            # output = handler.stdout.readlines()
            # if output is None:
            #     output = []

            # for one_line in output:
            #     client_socket.sendall(one_line)
            #     client_socket.sendall("\n")

            # client_socket.sendall("ok")

    # 发生异常则输出异常信息
    except Exception, e:
        traceback.print_exc()

    try:
        # 关闭socket连接
        client_socket.close()
    except Exception, e:
        traceback.print_exc()