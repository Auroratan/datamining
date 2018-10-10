# -*- coding: utf-8 -*-

import numpy as np
import aprior as ap

#从数据文件夹获取数据
def getData(filepath): 
    #创建数据list
    listArr = []
    num = 1200
    
    for i in range(num):
        arr = np.loadtxt(filepath+str(i)+'_item.txt')
        listArr.append(arr)
        
    print(listArr)
    return listArr


if __name__ == "__main__":
    
    path="./../item/"
    arr = getData(path)
    dataSet = arr;
    L, suppData = ap.apriori(dataSet, minSupport=0.1)
    print(L)
    print(suppData)
    print("rules")
    rules = ap.generateRules(L, suppData, minConf=0.7)

