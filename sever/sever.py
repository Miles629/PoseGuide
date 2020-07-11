#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
# #执行客户端发送过来的命令，并把执行结果返回给客户端
import socket, traceback, subprocess
import string
import linksql

host = '0.0.0.0'
port = 9998
#  连接数据库
DbHandle = linksql.DataBaseHandle('rm-bp199ck9jt24iu4g8lo.mysql.rds.aliyuncs.com','kid','Kidofstudio','userinfo',3306)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
s.bind((host, port))
s.listen(1)
 
while 1:
    try:
        client_socket, client_addr = s.accept()
    except Exception,e:
        traceback.print_exc()
        continue
 
    try:
        print 'From host:', client_socket.getpeername()
        while 1:
            command = client_socket.recv(4096)
            if not len(command):
                break
            print client_socket.getpeername()[0] + ':' + str(command)
            command=str(command)
            com=command.split()
            if (com[0]=="login"):
                print("user"+com[1]+"key"+com[2])
                # 这里查询数据库验证用户名密码
                ins=DbHandle.selectDblogin(com[1],com[2])
                if (ins==True):
                    client_socket.send("True")
                else:
                    client_socket.send("False")
            if (com[0]=="signin"):
                # DbHandle.insertDB("insert into userkey(username,key,lasttime) values('%s','%s')"%(str(com[1]),str(com[2])))
                print("user"+com[1]+"key"+com[2]+"email"+com[3])
                ins=DbHandle.insertDBsign(com[1],com[2],com[3])
                if (ins==True):
                    client_socket.send("True")
                else:
                    client_socket.send("False")
            if (com[0]=="uphistory"):
                print("user"+com[1])
                # 查询该用户历史记录
                # 客户端发送指令需要按照顺序发送，空格分开，从1到6分别是u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
                ins=DbHandle.insertDBhistory(com[1],com[2],com[3],com[4],com[5],com[6])
                if (ins==True):
                    client_socket.send("True")
                else:
                    client_socket.send("False")
            if (com[0]=="askhistory"):
                print("user"+com[1])
                ins=DbHandle.selectDbhistory(com[1])
                client_socket.send(str(ins))



                
            
            # 执行客户端传递过来的命令
            # handler = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            # output = handler.stdout.readlines()
            # if output is None:
            #     output = []
 
            # for one_line in output:
            #     client_socket.sendall(one_line)
            #     client_socket.sendall("\n")
 
            # client_socket.sendall("ok")
 
 
    except Exception, e:
        traceback.print_exc()
 
    try:
        client_socket.close()
    except Exception, e:
        traceback.print_exc()