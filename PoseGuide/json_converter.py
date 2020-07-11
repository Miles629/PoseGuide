'''
Auth://作者 zzm
Create date:///创建时间 2020.7.11
Update date://签入时间 2020.7.11
Discrip://此处须注明更新的详细内容
    用于把alphapose-cmu格式的json数据转换成指定格式json数据
'''

import json
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,help="path to the input alphapose-json")
ap.add_argument("-o", "--output", required=True,help="path to output directory to store spose-json")

inputpath=ap.parse_args().input
outputpath=ap.parse_args().output

json_result={}
with open(inputpath,'r') as input_file:
    inputpose=json.load(input_file)
i_findex=0
for i in range(len(inputpose)):
    json_result[str(i)+".jpg"]={}    
    json_result[str(i)+".jpg"]["people0"]=inputpose[str(i_findex)+".jpg"]["bodies"][0]["joints"]
    i_findex=i_findex+2
json_result["fnum"]=len(inputpose)
with open(outputpath,'w') as output_file:
    json.dump(json_result,output_file)
