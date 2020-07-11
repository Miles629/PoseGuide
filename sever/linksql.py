# -*- coding:utf-8 -*-

import pymysql,traceback,hashlib,time

class DataBaseHandle(object):
    def __init__(self,host,username,password,database,port):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(self.host,self.username,self.password,self.database,self.port,charset='utf8')

    def selectDbhistory(self,u):
        self.cursor = self.db.cursor()
        sql='select * from history where username="%s"'%(u)
        print(sql)
        try:
            tt=self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            print(tt)
            data = self.cursor.fetchall() # 返回所有记录列表
            print(data)
            msg=str(tt)+str(data)
            return msg
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

    # 这行函数是向数据库的训练历史记录发送插入,u用户名item训练项目s分数dp存储路径dur持续时间date训练日期
    def insertDBhistory(self,u,item,s,dp,dur,date):
        self.cursor = self.db.cursor()
        i=hash(time.localtime())
        i=str(i)
        sql='insert into history(id,username,itemname,score,datapath,duration,ddate) values ("%s","%s","%s","%s","%s","%s","%s")'%(pymysql.escape_string(i) ,pymysql.escape_string(u) ,
        pymysql.escape_string(item) ,pymysql.escape_string(s) ,pymysql.escape_string(dp) ,pymysql.escape_string(dur) ,pymysql.escape_string(date))
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



    def insertDBsign(self,u,k,em):
        ''' 插入数据库操作 '''

        self.cursor = self.db.cursor()
        # sql = "INSERT INTO userinfo(username, key) VALUES ("+u+","+k+")"
        sql='insert into userkey(username,password,umail) values ("%s","%s","%s")'%(pymysql.escape_string(u) ,pymysql.escape_string(k) ,pymysql.escape_string(em))
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



    def deleteDB(self,sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()





    def updateDb(self,sql):
        ''' 更新数据库操作 '''

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





    def selectDblogin(self,u,k):
        ''' 数据库查询 '''
        self.cursor = self.db.cursor()
        sql='select * from userkey where username="%s" and password="%s"'%(u,k)
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
                # 遍历打印结果
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
        ''' 数据库连接关闭 '''
        self.db.close()



# if __name__ == '__main__':

    # DbHandle = DataBaseHandle('127.0.0.1','kid','Kidofstudio','userinfo',3306)

    # DbHandle.insertDB('insert into test(name) values ("%s")'%('FuHongXue'))
    # DbHandle.insertDB('insert into test(name) values ("%s")'%('FuHongXue'))
    # DbHandle.selectDb('select * from test')
    # DbHandle.updateDb('update test set name = "%s" where sid = "%d"' %('YeKai',22))
    # DbHandle.selectDb('select * from test')
    # DbHandle.insertDB('insert into test(name) values ("%s")'%('LiXunHuan'))
    # DbHandle.deleteDB('delete from test where sid > "%d"' %(25))
    # DbHandle.selectDb('select * from test')
    # DbHandle.closeDb()