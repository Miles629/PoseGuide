'''
Auth://作者 zzm
Create date:///创建时间 2020.7.9
Update date://签入时间 2020.7.11
Discrip://此处须注明更新的详细内容
    7.11
    整合了动态时间规整算法和余弦比较算法，调用该类getLikeness（）可以进行相似度比较
    算法结果目前不太好，待完善
    修改了部分细节便于进行输出和判断
    7.12
    优化了余弦比较算法中的权重，分数拉开了10分，帧比较部分还可以继续优化
    7.15
    增加了分部位的评分，增加了改进建议
'''
import math
import json
import numpy as np
from dtw import dtw


class Coslike():

    spath='' #标准视频的json文件路径(含文件名)
    upath='' #用户视频的json文件路径（含文件名）

    def __init__(self,myspath,myupath):
        self.spath=myspath
        self.upath=myupath

    #计算向量夹角余弦
    def __VectorCosine(self,p,o,q,pose):
        #其中p,o,q为三个点的序号，返回值为∠POQ的余弦值
        # 读取O\P\Q三个点的x,y,c【置信度】
        xp=pose[3*p]
        yp=pose[3*p+1]
        cp=pose[3*p+2]
        xo=pose[3*o]
        yo=pose[3*o+1]
        co=pose[3*o+2]
        xq=pose[3*q]
        yq=pose[3*q+1]
        cq=pose[3*q+2]

        c=(cp+cq+co)/3  #角置信度为三点置信度的平均值【【【待改进】】】
        # 若有一点的置信度小于0.1，直接返回cos值-2
        if (cp<0.1)|(co<0.1)|(cq<0.1):
            return [-2.0,c]
        #计算向量OP(x1,y1)、OQ(x2,y2)
        x1=xp-xo
        y1=yp-yo
        x2=xq-xo
        y2=yq-yo
        cosine=(x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2))
        cosine=float(format(cosine,'.6f'))
        # cosine=int(cosine*100000)/100000
        return [cosine,c]

    def __CalcuCosAngles(self,pose):
        # 计算某一帧的10个角度，返回值为列表[[角1余弦，角置信度1],[角2余弦，角置信度2]...]
        cosines=[]
        cosines.append(self.__VectorCosine(0,1,2,pose))
        cosines.append(self.__VectorCosine(1,2,3,pose))
        cosines.append(self.__VectorCosine(2,3,4,pose))
        cosines.append(self.__VectorCosine(0,1,5,pose))
        cosines.append(self.__VectorCosine(1,5,6,pose))
        cosines.append(self.__VectorCosine(5,6,7,pose))
        cosines.append(self.__VectorCosine(1,8,9,pose))
        cosines.append(self.__VectorCosine(8,9,10,pose))
        cosines.append(self.__VectorCosine(1,11,12,pose))
        cosines.append(self.__VectorCosine(11,12,13,pose))
        return cosines

    def __CalcuPartsScores(self,spose,upose):
        # 计算单帧中，各身体部位的分数
        sangles = self.__CalcuCosAngles(spose)  # standard单帧所有角度余弦值
        uangles = self.__CalcuCosAngles(upose)  # user单帧所有角度余弦值
        part_scores={}
        part_scores["头部"]=self.__CalcuPartScore(0,3,sangles,uangles)
        part_scores["左臂"]=self.__CalcuPartScore(4,5,sangles,uangles)
        part_scores["右臂"]=self.__CalcuPartScore(1,2,sangles,uangles)
        part_scores["左腿"]=self.__CalcuPartScore(8,9,sangles,uangles)
        part_scores["右腿"]=self.__CalcuPartScore(6,7,sangles,uangles)
        return part_scores


    def __CalcuPartScore(self,index1,index2,sangles,uangles):
        # 计算某部分的分数 index1,index2是该身体部位的两个角的序号
        if (sangles[index1][0]!=-2.0)&(uangles[index1][0]!=-2.0)&(sangles[index2][0]!=-2.0)&(uangles[index2][0]!=-2.0):
            c0 = (sangles[index1][1] + uangles[index1][1]) / 2
            c1 = (sangles[index2][1] + uangles[index2][1]) / 2

            d0=abs(math.acos(sangles[index1][0]) - math.acos(uangles[index1][0]))
            d1=abs(math.acos(sangles[index2][0]) - math.acos(uangles[index2][0]))
            ds=d0+d1
            w0 = c0*d0/ds
            w1 = c1*d1/ds
            return 1-(d0*w0+d1*w1)/(2*math.pi*(w0+w1))
        else:
            return -1


    def __CalcuDistance(self,spose, upose):
        # 计算距离，用于动态时间规整
        sangles = self.__CalcuCosAngles(spose)  # standard单帧所有角度余弦值
        uangles = self.__CalcuCosAngles(upose)  # user单帧所有角度余弦值
        ds = 0  # ds是该帧中有效角度差之和
        w = 0
        cmpare_angles=0 #成功匹配的角度数目

        for i in range(len(sangles)):
            # 当某个角在用户和标准动作中都有较高置信度时[等于-2.0表示置信度小于0.1]
            if (sangles[i][0] != -2.0) & (uangles[i][0] != -2.0):
                wi = (sangles[i][1] + uangles[i][1]) / 2  # 平均值求权重【【【权重可优化】】】
                ds += abs(math.acos(sangles[i][0]) - math.acos(uangles[i][0])) * wi  # 角度差的绝对值*该角的平均权重
                w += wi
                cmpare_angles=cmpare_angles+1
        if cmpare_angles!=0:  # w！=0,可以进行除法计算
            Distance = ds / (2 * math.pi) / w
        else:
            Distance=-1

        return Distance

    def __CalcuLikeness(self,spose,upose):
        # 以下是单帧对比求相似度
        sangles=self.__CalcuCosAngles(spose)  #standard单帧所有角度余弦值
        uangles=self.__CalcuCosAngles(upose)  #user单帧所有角度余弦值
        ds=0  #ds是该帧中有效角度差之和
        w=0   #用于加权
        s=0   #用于计算分子
        cmpare_angles=0 #成功匹配的角度数目
        
        for i in range(len(sangles)):
            # 当某个角在用户和标准动作中都有较高置信度时[等于-2.0表示置信度小于0.1]
            if (sangles[i][0]!=-2.0)&(uangles[i][0]!=-2.0):
                ds+=abs(math.acos(sangles[i][0])-math.acos(uangles[i][0]))  # 求角度差之和
        # 根据角度差，给每一个角赋予权重
        for i in range(len(uangles)):
            # 当某个角在用户和标准动作中都有较高置信度时[等于-2.0表示置信度小于0.1]
            if (sangles[i][0]!=-2.0)&(uangles[i][0]!=-2.0):
                ci=(sangles[i][1]+uangles[i][1])/2   #平均置信度
                da=abs(math.acos(sangles[i][0])-math.acos(uangles[i][0]))   # 角度差da
                wi=ci*da/ds # wi是角度的权重
                s+=da*wi
                w+=wi
                cmpare_angles=cmpare_angles+1
        if cmpare_angles!=0:  # w！=0,可以进行除法计算
            likeness=1-s/(2*math.pi)/w
        else:
            likeness=-1
        return likeness

    # 获取数据
    def getData(self,sf_name, uf_name):
        with open(sf_name, 'r') as load_sf, open(uf_name, 'r') as load_uf:
            spose = json.load(load_sf)
            upose = json.load(load_uf)
        slength = spose["fnum"]
        ulength = upose["fnum"]
        sdata = []
        udata = []
        for i in range(slength):
            sdata.append(spose[str(i) + ".jpg"]["people0"])
        sdata = np.array(sdata).reshape(slength, 54)
        for i in range(ulength):
            udata.append(upose[str(i) + ".jpg"]["people0"])
        udata = np.array(udata).reshape(ulength, 54)

        return sdata, udata

    # 动态时间规整，返回规整后序列长度，以及规整后的序列编号，index[0]为标准序列，index[1]为用户序列
    def dtww(self,sf_name,uf_name):
        sdata,udata = self.getData(sf_name, uf_name)
        distance = lambda x, y: self.__CalcuDistance(x, y)
        d, cost_matrix, acc_cost_matrix, index = dtw(sdata, udata, dist=distance)
        pathLength = len(index[0])
        return pathLength,index

    def getLikeness(self):
        # 计算标准动作和用户动作的相似度（多帧）
        Length,index = self.dtww(self.spath,self.upath)
        sdata, udata = self.getData(self.spath, self.upath)

        # 规整后的数据
        ssdata = []  # 标准
        uudata = []  # 用户
        for i in range(Length):
            ssdata.append(sdata[index[0][i]])
            uudata.append(udata[index[1][i]])

        # 把规整后的数据改为 帧数*54 大小的二维列表
        ssdata = np.array(ssdata).reshape(Length,54)
        uudata = np.array(uudata).reshape(Length,54)
        scores=[] # 逐帧存储分数

        # 对有效帧逐帧进行相似度比较
        for f in range(Length):
            scoref=self.__CalcuLikeness(ssdata[f],uudata[f])
            if scoref != -1:
                scores.append(scoref)
        # print(scores)
        avg_score=np.nanmean(scores)

        # 计算各部分相似度
        part_scores={"头部":[],"左臂":[],"右臂":[],"左腿":[],"右腿":[]}
        for f in range(Length):
            fpart_score=self.__CalcuPartsScores(ssdata[f],uudata[f])
            print(fpart_score)
            for k in part_scores.keys():
                if fpart_score[k] !=-1:
                    part_scores[k].append(fpart_score[k])
        for k in part_scores.keys():
            part_scores[k]=np.nanmean(part_scores[k])
        print(part_scores)


        return avg_score,part_scores,comment
