# -*- coding:utf-8 -*-
# Auth:马草原//作者
# Create date:2020-07-07///创建时间
# Update date:2020-07-10//签入时间
# Discrip:实现了访问数据库的相关内容，并对askhistory返回值进行了修改//此处须注明更新的详细内容

import pymysql,traceback,hashlib,time
# 创建一个数据库操作对象
class DataBaseHandle(object):
    def __init__(self,host,username,password,database,port):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host,self.username,self.password,self.database,self.port,charset='utf8')
#   在数据库中查找用户历史记录
    def selectDbhistory(self,usrname):
        self.cursor = self.db.cursor()
        sql='select * from history where username="%s"'%(usrname)
        print(sql)
        try:
            tt=self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            print(tt)#打印出查询语句来方便判断传入语句是否有问题
            data = self.cursor.fetchall() # 返回所有记录列表
            print(data)
            # msg=str(tt)+str(data)
            return data
            # 调试时用于确认返回信息，已弃用
            # for row in data:
            #     sid = row[0]
            #     name = row[1]
            #     # 遍历打印结果
            #     print('sid = %s,  name = %s'%(sid,name))

        except Exception, e:
            traceback.print_exc()
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()

    # 这行函数是向数据库的训练历史记录发送插入
    # u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
    def insertDBhistory(self,u,item,s,dp,dur,date,com,part):
        self.cursor = self.db.cursor()
        # 生成一个哈希码来作为数据库主键
        hashcode=hash(time.localtime())
        hashcode=str(hashcode)
        sql='insert into history(id,username,itemname,score,datapath,duration,ddate,ccomment,partscores) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(pymysql.escape_string(hashcode) ,pymysql.escape_string(u) ,
        pymysql.escape_string(item) ,pymysql.escape_string(s) ,pymysql.escape_string(dp) ,pymysql.escape_string(dur) ,pymysql.escape_string(date) ,pymysql.escape_string(com) ,pymysql.escape_string(part))
        print(sql)
        try:
            tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            print(tt)
            self.db.commit()
            return True
        except Exception,e:
            traceback.print_exc()
            print("insert error:")
            # 发生错误时回滚
            self.db.rollback()
            return False
        finally:
            self.cursor.close()


#   进行用户注册，向数据库中插入信息，其中：
    def insertDBsign(self,usrname,ukey,uemail):
        # ''' 插入数据库操作 '''

        self.cursor = self.db.cursor()
        # sql = "INSERT INTO userinfo(username, key) VALUES ("+u+","+k+")"
        sql='insert into userkey(username,password,umail) values ("%s","%s","%s")'%(pymysql.escape_string(usrname) ,pymysql.escape_string(ukey) ,pymysql.escape_string(uemail))
        print(sql)
        try:
            # 执行sql
            # self.cursor.execute(sql)
            tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # tt=self.cursor.executemany(sql,val)
            print(tt)
            self.db.commit()
            return True
        except Exception, e:
            traceback.print_exc()
            print("insert error:")
            # 发生错误时回滚
            self.db.rollback()
            return False
        finally:
            self.cursor.close()


#       产品逻辑中暂无设置相应的删除操作，因此先注释掉，备用
    # def deleteDB(self,sql):
    #     # ''' 操作数据库数据删除 '''
    #     self.cursor = self.db.cursor()

    #     try:
    #         # 执行sql
    #         self.cursor.execute(sql)
    #         # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
    #         # print(tt)
    #         self.db.commit()
    #     except:
    #         # 发生错误时回滚
    #         self.db.rollback()
    #     finally:
    #         self.cursor.close()




#   产品逻辑中暂无需要对数据库进行更新的操作，以后可能会做修改密码等操作时再根据情况进行修改
    def updateDb(self,sql):
        # ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            # self.cursor.execute(sql)
            tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()




#   登录时进行数据库查询，能够找到用户名密码一样的情况则返回True
    def selectDblogin(self,usrname,ukey):
        self.cursor = self.db.cursor()
        sql='select * from userkey where username="%s" and password="%s"'%(usrname,ukey)
        print(sql)
        try:
            tt=self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            print(tt)
            data = self.cursor.fetchall() # 返回所有记录列表
            print(data)
            # 结果遍历
            for row in data:
                sid = row[0]
                name = row[1]
                # 遍历打印结果,便于调试
                print('sid = %s,  name = %s'%(sid,name))
            if(tt!=0):
                return True
            else:
                return False
        except Exception, e:
            traceback.print_exc()
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()


    def closeDb(self):
        # ''' 数据库连接关闭 '''
        self.db.close()



    # 数据库访问相关语句例子   
    # DbHandle = DataBaseHandle('127.0.0.1','kid','Kidofstudio','userinfo',3306)
    # DbHandle.insertDB('insert into test(name) values ("%s")'%('FuHongXue'))
    # DbHandle.selectDb('select * from test')
    # DbHandle.updateDb('update test set name = "%s" where sid = "%d"' %('YeKai',22))
    # DbHandle.deleteDB('delete from test where sid > "%d"' %(25))
    # DbHandle.closeDb()