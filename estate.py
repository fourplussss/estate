#
import sys
import io
import geocoder
import csv
data=[]#創一個空的list裝data

#讀檔並放進data 用list來裝dictionary
with open("a_lvr_land_a.txt", newline='') as csvfile:
    rows = csv.DictReader(csvfile)#讀成dictionary
    for row in rows:
        data.append(row)
print(data)
#print(csvfile) 
#把地址丟進open street map
for j in range(1,len(data)):#資料第1行是key 第2行為英文 真正資料從第3行開始
    for i in range(len(data[j]['土地區段位置建物區段門牌'])):#地址字數的迴圈
        print(data[j]['土地區段位置建物區段門牌'][0:len(data[j]['土地區段位置建物區段門牌'])-i])#要丟進去的資料
        g = geocoder.osm(data[j]['土地區段位置建物區段門牌'][0:len(data[j]['土地區段位置建物區段門牌'])-i])#丟進去
#        print(g.osm)#看有沒有東西
        if g.osm!=None:#有ㄌ
            data[j].update(g.osm)#把拿到的資料丟回去原本的資料
#            print(data[j])
            break
        if data[1]['土地區段位置建物區段門牌'][len(data[1]['土地區段位置建物區段門牌'])-1-i]is'路':#如果到路還沒有資料 那就不要這筆了
            break


