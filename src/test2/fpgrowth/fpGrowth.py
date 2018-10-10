# -*- coding: utf-8 -*-

import csv

import random
from astropy.wcs.docstrings import row
import MyLogger as log
message = log.Logger('all.log',level='debug')

class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        
        self.name=nameValue
        self.count=numOccur
        self.nodeLink=None     #nodeLink 变量用于链接相似的元素项
        self.parent=parentNode #指向当前节点的父节点
        self.children={}  #空字典，存放节点的子节点
        
    def inc(self,numOccur):
        self.count += numOccur
      
    #将树以文本形式显示    
    def display(self,ind=1):
        print(' '*ind,self.name,' ',self.count)
        for child in self.children.values():
            child.display(ind+1)
            

#构建FP-tree
def createTree(dataSet,minSup=1):
    headerTable={}
    for transaction in dataSet:
        for item in transaction:
              #用头指针表统计各个类别的出现的次数，计算频繁量：头指针表[类别]=出现次数
            headerTable[item]=headerTable.get(item,0)+dataSet[transaction]
             
             
#    for k in headerTable.keys():
#        if headerTable[k] < minSup:
#            del(headerTable[k])
            
    for k in list(headerTable): #删除未达到最小频繁度的数据
        if headerTable[k] < minSup:
            del(headerTable[k]) 
    freqItemSet=set(headerTable.keys()) #保存达到要求的数据
    print ('freqItemSet: ',freqItemSet)
    message.logger.info('freqItemSet: %s ',freqItemSet)
    
    if len(freqItemSet)==0:
        return None,None #若达到要求的数目为0
    
    
    for k in headerTable:
        headerTable[k]=[headerTable[k],None]
    print ('headerTable: ',headerTable)
    message.logger.info('headerTable: %s',headerTable)
    rootTreeNode=treeNode('null',1,None)#初始化tree
    
    
    for transet,count in dataSet.items(): # 第二次遍历：
        LocalD={}
        for item in transet:
            if item in freqItemSet:
                #只对频繁项集进行排序
                LocalD[item]=headerTable[item][0]
        if len(LocalD)>0:
            orderedItem=[v[0] for v in sorted(LocalD.items(),key=lambda p:p[1],reverse=True)]
            updateTree(orderedItem,rootTreeNode,headerTable,count)
    return rootTreeNode,headerTable#返回树和头指针表


def updateTree(items,inTree,headerTable,count):# 首先检查是否存在该节点
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count) # 存在则计数增加
    else:
        inTree.children[items[0]]=treeNode(items[0],count,inTree) #创建一个新节点
        if headerTable[items[0]][1]==None: #若原来不存在该类别，更新头指针列表
            headerTable[items[0]][1]=inTree.children[items[0]]
        else:
            #更新指向
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items)>1:   
        #仍有未分配完的树，迭代
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)        


#节点链接指向树中该元素项的每一个实例。
# 从头指针表的 nodeLink 开始,一直沿着nodeLink直到到达链表末尾
def updateHeader(nodeToTest,targetNode):
    while(nodeToTest.nodeLink!=None):
        nodeToTest=nodeToTest.nodeLink
    nodeToTest.nodeLink=targetNode
    
#从FP树中发现频繁项集
def ascendTree(LeafNode,prefixPath):
    #递归上溯整棵树
    if LeafNode.parent!=None:
        prefixPath.append(LeafNode.name)
        ascendTree(LeafNode.parent, prefixPath)
        
#寻找当前非空节点的前缀        
def findPrefixPath(basePat,treeNode):
    condPats={}
    while treeNode!=None:
        prefixPath=[]
        ascendTree(treeNode, prefixPath)
        if len(prefixPath):
            condPats[frozenset(prefixPath[1:])]=treeNode.count  #将条件模式基添加到字典中
        treeNode=treeNode.nodeLink
    return condPats

#递归查找频繁项集
def mineTree(intTree,headerTable,minSup,preFix,freqItemList):
    # 头指针表中的元素项按照频繁度排序,从小到大
    bigL=[v[0] for v in sorted(headerTable.items(),key=lambda p: str(p[1]))]
    for basePat in bigL:
        #加入频繁项列表
        newFreqSet=preFix.copy()
        newFreqSet.add(basePat)
        print ('finalFrequent Item: ',newFreqSet)
        message.logger.info('finalFrequent Item: %s',newFreqSet)
        freqItemList.append(newFreqSet)
        
        #递归调用函数来创建基
        condPattBases=findPrefixPath(basePat, headerTable[basePat][1])
        #构建条件模式Tree
        myCondTree,myHead=createTree(condPattBases, minSup)
        #将创建的条件基作为新的数据集添加到fp-tree
        
        print ('head from conditional tree: ', myHead)
        message.logger.info('head from conditional tree: %s', myHead)
        if myHead!=None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
            
def getRules(supportdata,fp_items,count,lift=1.0):
    print("getRules")
    bigRuleList = []
    print("-----")
    freqRuleList=[]
    for items in fp_items:
        
        if len(items) > 1 :#and set(['ship1']).issubset(set(items)):
            H1=[frozenset([item]) for item in items]
            
           
            for h in H1:
                temp=frozenset(sorted(items-h))
                sab=(float)(supportdata[frozenset(items)])
                sa=(float)(supportdata[h])
                sb=(float)(supportdata[temp])              
                s=sab*count/(sa*sb)
                if s>lift:
                    print(str(items-h)+'->'+str(h)+' '+str(s))
                    message.logger.info(str(items-h)+'->'+str(h)+' '+str(s))
                    calcConf(items, H1, supportdata, bigRuleList, minConf=0.7)
    return freqRuleList    

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    #针对项集中只有两个元素时，计算可信度
    prunedH = []#返回一个满足最小可信度要求的规则列表
    for conseq in H:#后件，遍历 H中的所有项集并计算它们的可信度值
        conf = supportData[frozenset(freqSet)]/supportData[frozenset(freqSet-conseq)] #可信度计算，结合支持度数据
        #print(conf)
        if conf >= minConf:
            if(2000 in freqSet-conseq):
                
                message.logger.info('True %s %s, %s %s','-->',conseq,'conf:',conf)
                print ('True','-->',conseq,'conf:',conf)
                #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
                brl.append((freqSet-conseq, conseq, conf))#添加到规则里，brl 是前面通过检查的 bigRuleList
                prunedH.append(conseq)#同样需要放入列表到后面检查
            if(5000 in freqSet-conseq):
                message.logger.info('False %s %s, %s %s','-->',conseq,'conf:',conf)
                print ('False','-->',conseq,'conf:',conf,'  ')
                #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
                brl.append((freqSet-conseq, conseq, conf))#添加到规则里，brl 是前面通过检查的 bigRuleList
                prunedH.append(conseq)#同样需要放入列表到后面检查
    return prunedH
#def loadDataSet():
#    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def loadSimpDat():
#    simpDat = [['r','z','h','j','p'],
#               ['z','y','x','w','v','u','t','s'],
#               ['z'],
#               ['r','x','n','o','s'],
#               ['y','r','x','z','q','t','p'],
#               ['y','z','x','e','q','s','t','m']]
    
    simpDat=[[624,631,633,635,6.410000000000000000e+02,6.450000000000000000e+02,
             6.470000000000000000e+02,6.590000000000000000e+02,6.610000000000000000e+02,
             6.670000000000000000e+02,2.000000000000000000e+03],
             [6.030000000000000000e+02,6.120000000000000000e+02,6.190000000000000000e+02,
              6.240000000000000000e+02,6.310000000000000000e+02,6.330000000000000000e+02,
              6.350000000000000000e+02,6.410000000000000000e+02,6.450000000000000000e+02,
              6.470000000000000000e+02,6.590000000000000000e+02,6.610000000000000000e+02,
              6.670000000000000000e+02,5.000000000000000000e+03],
              [4.940000000000000000e+02,5.210000000000000000e+02,5.250000000000000000e+02,
               5.390000000000000000e+02,5.400000000000000000e+02,5.640000000000000000e+02,
               5.720000000000000000e+02,5.810000000000000000e+02,5.940000000000000000e+02,
               6.040000000000000000e+02,6.120000000000000000e+02,
               6.190000000000000000e+02,6.240000000000000000e+02,6.310000000000000000e+02,
               6.330000000000000000e+02,6.350000000000000000e+02,
               6.410000000000000000e+02,6.450000000000000000e+02,
               6.470000000000000000e+02,6.590000000000000000e+02,
               6.610000000000000000e+02,6.670000000000000000e+02,2.000000000000000000e+03],
               [4.330000000000000000e+02,4.500000000000000000e+02,4.960000000000000000e+02,
                5.220000000000000000e+02,5.250000000000000000e+02,5.350000000000000000e+02,
                5.440000000000000000e+02,5.650000000000000000e+02,5.730000000000000000e+02,
                5.910000000000000000e+02,5.950000000000000000e+02,6.040000000000000000e+02,
                6.130000000000000000e+02,6.180000000000000000e+02,6.240000000000000000e+02,
                6.310000000000000000e+02,6.330000000000000000e+02,6.350000000000000000e+02,
                6.410000000000000000e+02,6.450000000000000000e+02,6.470000000000000000e+02,
                6.590000000000000000e+02,6.610000000000000000e+02,6.670000000000000000e+02,
                2.000000000000000000e+03]
            ]
    
    return simpDat


if __name__ == "__main__":
    
    #dataSet = loadDataSet();
    dataSet = loadSimpDat()

   
    inputData={}
    for line in dataSet:
        inputData[frozenset(line)] = 1
        
        
#    print(len(inputData))
#    print(inputData)
    fp_items=[]
    fp_items_temp=[]
    Fptree,headerTable=createTree(inputData, 0.1*len(inputData))
    #Fptree.display()
    mineTree(Fptree, headerTable,  0.1*len(inputData), set([]), fp_items_temp)
    #print(headerTable)
    for item in fp_items_temp:
        item2=sorted(item)
        fp_items.append(set(item2))    
        
    
    supportdata={}
    for fp in fp_items:
        for transaction in inputData:
            if fp.issubset(transaction):
                if frozenset(fp) in supportdata:
                    supportdata[frozenset(fp)] += 1
                else:supportdata[frozenset(fp)] = 1
    print(fp_items)
    print("===============")
    print(supportdata)            
    alist = getRules(supportdata,fp_items,len(inputData),lift=3.0)
    print(alist)
                    

  
    
#data=open(r'../../../data/Test2_Data.csv')
#reader =csv.reader(data)
#headers = next(reader) 
##print(headers)
#inputData={}
#for row in reader:
#    if random.random()<=1:
#        inputData[frozenset(row)]=1
#print(len(inputData))
#print(inputData)
#fp_items=[]
#fp_items_temp=[]
#Fptree,headerTable=createTree(inputData, 0.1*len(inputData))
#mineTree(Fptree, headerTable,  0.1*len(inputData), set([]), fp_items_temp)
 
# for item in fp_items_temp:
#     item2=sorted(item)
#     fp_items.append(set(item2))
# 
# supportdata={}
# for fp in fp_items:
#     for transaction in inputData:
#         if fp.issubset(transaction):
#                 if not supportdata.has_key(frozenset(fp)):
#                     supportdata[frozenset(fp)]=1
#                 else:supportdata[frozenset(fp)]+=1
# getRules(supportdata,fp_items,len(inputData),lift=1.0)
#print("success")