import socket
target_host = "39.106.96.98"
target_port = 9998
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
# 登录的时候你就按照下面的格式来，例子是用户名99，密码66
# 如果要查询该用户的历史记录，就要发送msg="history 99"
# 返回值还没写，登录注册就是True和False作为成功失败，历史还没想好什么格式
def login(str):
    # 登录只能用用户名密码
    msg="login 99 69"
    msg=msg.encode()
    client.send(msg)
    response = client.recv(4096)
    print (response)
def askhistory(str):
    # 查询某用户的历史记录，跟的是用户名，如果没有记录返回b'()'如果有则返回b'(记录内容)'
    # 测试数据包括
    # "uphistory u item s dp dur date"
    # "uphistory u 加油操 69 system/p 11:12 20-7-8"
    # 然后进行查询结果如下
    # b"((u'-1990937634878078585', u'u', u'\\u52a0\\u6cb9\\u64cd', u'69', u'system/p', u'11:12', u'20-7-8'), (u'-6171808383927979350', u'u', u'item', u's', u'dp', u'dur', u'date'))"
    msg="askhistory u"
    msg=msg.encode()
    client.send(msg)
    response = client.recv(4096)
    print (response)
def signin(str):
    # 注册按照这个格式
    msg="signin 99 69 email@xx.com"
    msg=msg.encode()
    client.send(msg)
    response = client.recv(4096)
    print (response)
def uphistory():
    # 上传训练历史记录的格式如下，u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
    msg="uphistory u item s dp dur date"
    msg=msg.encode()
    client.send(msg)
    response = client.recv(4096)
    print (response)
msg="askhistory u"
msg=msg.encode()
client.send(msg)
response = client.recv(4096)
print (response)
