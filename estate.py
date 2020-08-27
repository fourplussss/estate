#!/usr/local/bin/python3

import sys
import io
import geocoder
import csv
import pandas as pd
import numpy as np
import math
import ast
from fastnumbers import fast_real

def main():
#    pass


#! Todo
#! 1. Refine coding style (No Chinese in code, move code into main function)
#! 2. Add space before and after assignment operator
#! 3. Use python3 native logging system to log out debug info
    data = []
    with open("a_lvr_land_a.txt", newline='') as csvfile:
        rows = csv.DictReader(csvfile)#read as dictionary
        for row in rows:
            data.append(row)
    data.pop(0)
    fea = 2#how manyfeature
    des = np.empty([len(data),fea],dtype=float)#x,y
    pri = np.empty([len(data),1],dtype=float)#price

    for j in range(0,len(data)):
        addr = data[j]['土地區段位置建物區段門牌']
        #index = {'巷':11,'號':17}
        for i in range(len(data[j]['土地區段位置建物區段門牌'])):#all the word in addres
            if addr[len(addr)-1-i] != '號'and addr[len(addr)-1-i]!='段'and addr[len(addr)-1-i]!='路'and addr[len(addr)-1-i]!='巷'and addr[len(addr)-1-i]!='街'and addr[len(addr)-1-i]!='弄':
                continue
            g = geocoder.osm(addr[0:len(addr)-i])#find
            if g.osm:
                data[j].update(g.osm)#updata the new information
                print(data[j])
                break
    no = []

#    fea = 2#how manyfeature
#    des = np.empty([len(data),fea],dtype=float)#x,y
#    pri = np.empty([len(data),1],dtype=float)#price
    for i in range(len(data)):
       	if 'x' in data[i] and data[i]['單價元平方公尺']!='':
           	continue
           	print('a')
       	else:
           	no.append(i)
           	print('b')
    for i in range(len(no)-1,-1,-1):
       	data.pop(no[i])
#    fea = 2#how manyfeature
#    des = np.empty([len(data),fea],dtype=float)#x,y
#    pri = np.empty([len(data),1],dtype=float)#price
    for i in range(len(data)):
       	des[i,0]=data[i]['x']
       	des[i,1]=data[i]['y']
       	pri[i,0]=fast_real(data[i]['單價元平方公尺'])
#normalize
    meandes=np.mean(des,axis=0)
    stddes=np.std(des,axis=0)
    for i in range(len(des)):#how many different feature
        for j in range(len(des[0])):#same feature have how many data
            if stddes[j]!=0:
                des[i,j] = (des[i,j]-meandes[j])/stddes[j]
    destrain = des[:math.floor(len(data)*0.8),:]
    pritrain = pri[:math.floor(len(data)*0.8),:]
    desvalid = des[math.floor(len(data)*0.8):math.floor(len(data)*0.8),:]
    privalid = pri[math.floor(len(data)*0.8):math.floor(len(data)*0.8),:]
    destest = des[math.floor(len(data)*0.9):,:]
    pritest = pri[math.floor(len(data)*0.9):,:]
#train
    wei = np.zeros([fea,1])
    learningrate = 100
    iter = 100000
    loss = 0
    gradient = 0
    adagrad = 0
    eps = 0.000000001
    for t in range(iter):
        loss = np.sqrt(np.sum(np.power(np.dot(destrain,wei)-pritrain,2))/fea)
        if(t%100==0):
            print('第')
            print(t)
            print('次: loss=')
            print(loss)
    gradient = 2*np.dot(destrain.transpose(),np.dot(destrain,wei)-pritrain)
    adagrad += gradient**2
    wei = wei-learningrate*gradient/np.sqrt(adagrad+eps)
    np.save('weight.npy',wei)
    print(wei)
#test
    acc=(privalid-np.dot(desvalid,wei)/privalid)
    print('valid準確率為')
    print(acc)


if __name__ == "__main__":
	main()

