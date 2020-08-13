#
import sys
import io
import geocoder
import csv
import pandas as pd
import numpy as np
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
des=np.empty([len(data),2],dtype=float)#經度緯度
y=np.empty([len(data),1],dtype=float)#價錢



print('data0')
print(data[0])

for i in range(len(data)):
    if 'x' in data[i]:
        continue
    else:
        data[i].pop(i)
        print('QQQQQQQQQQQQQQQQQQQQQQ')
        print(i)


for i in range(len(data)):
#    if 'x' in data[i]:
        des[i,0]=data[i]['x']
        des[i,1]=data[i]['y']
#    else:
#        continue
print('------------------------------------')
print(data[1].get('z'))
print(des)
print(y)
