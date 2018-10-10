# -*- coding: utf-8 -*-


import numpy as np
import fpGrowth as fpg

#从数据文件夹获取数据
def getData(filepath, num = 12): 
    #创建数据list
    listArr = []
    for i in range(num):
        arr = np.loadtxt(filepath+str(i)+'_item.txt')
        listArr.append(arr)
        
    #print(listArr)
    return listArr


if __name__ == "__main__":
    
    path="./../item/"
    arr = getData(path,3)
    dataSet = arr;
    print(dataSet)
    inputData={}
    for line in dataSet:
        inputData[frozenset(line)] = 1
        
        
    print(len(inputData))
    #print(inputData)
    fp_items=[]
    fp_items_temp=[]
    Fptree,headerTable=fpg.createTree(inputData, 0.1*len(inputData))
    Fptree.display()
    fpg.mineTree(Fptree, headerTable,  0.1*len(inputData), set([]), fp_items_temp)
    print(headerTable)
#    for item in fp_items_temp:
#        item2=sorted(item)
#        fp_items.append(set(item2))    
#        
#    
#    supportdata={}
#    for fp in fp_items:
#        for transaction in inputData:
#            if fp.issubset(transaction):
#                if frozenset(fp) in supportdata:
#                    supportdata[frozenset(fp)] += 1
#                else:supportdata[frozenset(fp)] = 1
#    print(fp_items)
#    print("===============")
#    print(supportdata)            
#    alist = fpg.getRules(supportdata,fp_items,len(inputData),lift=3.0)
#    print(alist)
#    

