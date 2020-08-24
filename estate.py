#
#import java.util.Scanner
import sys
import io
import geocoder
import csv
import pandas as pd
import numpy as np
import math
import ast
from fastnumbers import fast_real
data=[]#創一個空的list裝data
#讀檔並放進data 用list來裝dictionary
with open("a_lvr_land_a.txt", newline='') as csvfile:
    rows = csv.DictReader(csvfile)#讀成dictionary
    for row in rows:
        data.append(row)
print(len(data))
#print(data)
#print(csvfile) 
#把地址丟進open street map
#if data[1]['土地區段位置建物區段門牌'][1]=='北'
#    print('A')

for j in range(1,len(data)):#資料第1行是key 第2行為英文 真正資料從第3行開始
    for i in range(len(data[j]['土地區段位置建物區段門牌'])):#地址字數的迴圈
        print(data[j]['土地區段位置建物區段門牌'][0:len(data[j]['土地區段位置建物區段門牌'])-i])#要丟進去的資料
#        g = geocoder.osm(data[j]['土地區段位置建物區段門牌'][0:len(data[j]['土地區段位置建物區段門牌'])-i])#丟進去
#        print(g.osm)#看有沒有東西
        if data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i] != '號'and data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i]!='段'and data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i]!='路'and data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i]!='巷'and data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i]!='街'and data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i]!='弄':
            continue
        g = geocoder.osm(data[j]['土地區段位置建物區段門牌'][0:len(data[j]['土地區段位置建物區段門牌'])-i])#丟進去
        print('gggggggggg')
        if g.osm!=None:#有ㄌ
            data[j].update(g.osm)#把拿到的資料丟回去原本的資料
            print(data[j])
            break
        if data[j]['土地區段位置建物區段門牌'][len(data[j]['土地區段位置建物區段門牌'])-1-i]is'路':#如果到路還沒有資料 那就不要這筆了
            break
#        print('aaaaaa')
#整理要train的資料
#des=np.empty([len(data),2],dtype=float)#經度緯度
#y=np.empty([len(data),1],dtype=float)#價錢
print('data0')
print(data[0])
no=[]
for i in range(len(data)):
    if 'x' in data[i] and '單價元平方公尺' in data[i]:
        continue
    else:
        no.append(i)
for i in range(len(no)-1,-1,-1):
    data.pop(no[i])
fea=2#多少feature
des=np.empty([len(data),fea],dtype=float)#經度緯度
pri=np.empty([len(data),1],dtype=float)#價錢

for i in range(len(data)):

    des[i,0]=data[i]['x']
    des[i,1]=data[i]['y']
    pri[i,0]=fast_real(data[i]['單價元平方公尺'])
#正規化
meandes=np.mean(des,axis=0)
stddes=np.std(des,axis=0)


for i in range(len(des)):#特徵種類
    for j in range(len(des[0])):#同特徵所含樣本數
        if stddes[j]!=0:
            des[i,j]=(des[i,j]-meandes[j])/stddes[j]
#print(des)
destrain=des[:math.floor(len(data)*0.6),:]
pritrain=pri[:math.floor(len(data)*0.6),:]
desvalid=des[math.floor(len(data)*0.6):math.floor(len(data)*0.8),:]
privalid=pri[math.floor(len(data)*0.6):math.floor(len(data)*0.8),:]
destest=des[math.floor(len(data)*0.8):,:]
pritest=pri[math.floor(len(data)*0.8):,:]
#train
wei=np.zeros([fea,1])
learningrate=100
iter=100000
loss=0
gradient=0
adagrad=0
eps=0.000000001
for t in range(iter):
    loss=np.sqrt(np.sum(np.power(np.dot(destrain,wei)-pritrain,2))/fea)
    if(t%100==0):
        print('第')
        print(t)
        print('次: loss=')
        print(loss)
    gradient=2*np.dot(destrain.transpose(),np.dot(destrain,wei)-pritrain)
    adagrad+=gradient**2
    wei=wei-learningrate*gradient/np.sqrt(adagrad+eps)
np.save('weight.npy',wei)
print(wei)


