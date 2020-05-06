import math
import json


# 计算向量长度
def calculateSize(self):
    result = 0
    num = len(self.coordinates)
    for i  in range(num):
        result +=self.coordinates[i] * self.coordinates[i]
    result = math.sqrt(result)
    return round(result,3)

# 将向量归一化
def standardizaiton(self):
    size = self.calculateSize()
    new_corrdinate = [round(x/size,3) for x in self.coordinates]
    return Vector(new_corrdinate)

#计算向量夹角余弦
def VectorCosine(p,o,q,pose):
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

    c=(cp+cq+co)/3

    # 若有一点的置信度小于0.1，直接返回cos值-2
    if (cp<0.1)|(co<0.1)|(cq<0.1):
        return [-2.0,c]

    #计算向量OP(x1,y1)、OQ(x2,y2)
    x1=xp-xo
    y1=yp-yo
    x2=xq-xo
    y2=yq-yo
    cosine=(x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2))
    return [cosine,c]

# 计算某一帧的10个角度，返回值为列表[[角1，角置信度1],[角2，角置信度2]...]
def CalcuAngles(pose):
    cosines=[]
    cosines.append(VectorCosine(0,1,2,pose))
    cosines.append(VectorCosine(1,2,3,pose))
    cosines.append(VectorCosine(2,3,4,pose))
    cosines.append(VectorCosine(0,1,5,pose))
    cosines.append(VectorCosine(1,5,6,pose))
    cosines.append(VectorCosine(5,6,7,pose))
    cosines.append(VectorCosine(1,8,9,pose))
    cosines.append(VectorCosine(8,9,10,pose))
    cosines.append(VectorCosine(1,11,12,pose))
    cosines.append(VectorCosine(11,12,13,pose))
    return cosines

def CalcuLikeness(spose,upose):
    # 以下是单帧对比求相似度
    sangles=CalcuAngles(spose)
    uangles=CalcuAngles(upose)
    ds=0  #ds是该帧中有效角度差之和
    w=0
    for i in range(len(sangles)):
        # 当某个角在用户和标准动作中都有较高置信度时
        if (sangles[i][0]!=-2.0)&(uangles[i][0]!=-2.0):
            wi=(sangles[i][1]+sangles[i][1])/2 #平均值求权重
            ds+=abs(math.acos(sangles[i][0])-math.acos(uangles[i][0]))*wi
            w+=wi

    likeness=1-ds/(2*math.pi)/w
    return likeness

def main():
    # 加载标准视频的json文件【spose】
    with open("E:\\项目竞赛\\大二\\运动识别\\workspace\\AlphaPose\\output\\test3\\alphapose-results.json",'r') as load_sf:
        spose=json.load(load_sf)
        # print(spose["0.jpg"]["people"][0]["pose_keypoints_2d"])
        # print(CalcuAngles(spose["0.jpg"]["people"][0]["pose_keypoints_2d"]))
    # 加载用户视频的json文件【upose】
    with open("E:\\项目竞赛\\大二\\运动识别\\workspace\\AlphaPose\\output\\test3\\alphapose-results.json",'r') as load_uf:
        upose=json.load(load_uf)
        # print(CalcuAngles(upose["0.jpg"]["people"][0]["pose_keypoints_2d"]))

    print(CalcuLikeness(spose["2.jpg"]["bodies"][0]["joints"],upose["3.jpg"]["bodies"][0]["joints"]))
    
if __name__ == '__main__':
    main()