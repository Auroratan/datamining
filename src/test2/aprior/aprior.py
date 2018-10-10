import MyLogger as log

message = log.Logger('all.log',level='debug')



#首先生成一个数据集
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

#测试数据集dataset有了:
#第一步，我们要根据数据集dataset得到一个集合C1，
#集合C1中包含的元素为dataset的无重复的每个单元素，候选项集。
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])  # store all the item unrepeatly

    C1.sort()
    #返回的数据map计算得到一个元素为frozenset的集合。
    # return map(frozenset, C1)#frozen set, user can't change it.
    return list(map(frozenset, C1))

"""
第二步，计算C1<key>每个元素key的支持度。
支持度= count(key) / sizeof(C1)

先把dataset转成元素为集合的类型。
这里设置支持度为0.5。当key在dataset中出现的集合个数超过一半即认为是频繁项。
L1是根据计算C1中每个元素是否满足支持度规则过滤得到的C1的子集。
L1的元素两两组合构成C2，再根据C2中每个元素是否满足支持度规则过滤得到的C1的子集L2。依次类推，直到Lk是单元素集合。
添加如下代码，可以得到一个完整的找频繁项集的代码：
"""
def scanD(D, Ck, minSupport):
    # 参数：数据集、候选项集列表 Ck以及感兴趣项集的最小支持度 minSupport
    ssCnt = {}
    for tid in D:  # 遍历数据集
        for can in Ck:  # 遍历候选项
            if can.issubset(tid):  # 判断候选项中是否含数据集的各项
                # if not ssCnt.has_key(can): # python3 can not support
                if not can in ssCnt:
                    ssCnt[can] = 1  # 不含设为1
                else:
                    ssCnt[can] += 1  # 有则计数加1
    numItems = float(len(D))  # 数据集大小
    retList = []  # L1初始化
    supportData = {}  # 记录候选项中各个数据的支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems  # 计算支持度
        if support >= minSupport:
            retList.insert(0, key)  # 满足条件加入L1中
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):  # 组合，向上合并
    # creates Ck 参数：频繁项集列表 Lk 与项集元素个数 k
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):  # 两两组合遍历
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:  # 若两个集合的前k-2个项相同时,则将两个集合合并
                retList.append(Lk[i] | Lk[j])  # set union
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))  
    L1, supportData = scanD(D, C1, minSupport)  # 单项最小支持度判断 0.5，生成L1
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):  # 创建包含更大项集的更大列表,直到下一个大的项集为空
        Ck = aprioriGen(L[k - 2], k)  # Ck
        Lk, supK = scanD(D, Ck, minSupport)  # get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
        if (k == 4):
            break;
    return L, supportData

# 下面是关联规则   默认最小置信度为0.7   
# 主函数  
def generateRules(L, supportData, minConf=0.7):
    # 频繁项集列表、包含那些频繁项集支持数据的字典、最小可信度阈值
    bigRuleList = []  # 存储所有的关联规则
    for i in range(1, len(L)):  # 只获取有两个或者更多集合的项目，从1,即第二个元素开始，L[0]是单个元素的
        # 两个及以上的才可能有关联一说，单个元素的项集不存在关联问题
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            # 该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            if (i > 1):
                # 如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:  # 第一层时，后件数为1
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)  # 调用函数2
    return bigRuleList

"""
原代码，如果freqSet =[2,3,5] 
H={[frozenset([2, 3]), 
frozenset([2, 5]), 
frozenset([3, 5])]}
[2,3,5]去计算对[2][3][5]的置信度均不符合最小要求，
返回[]，无法继续对[2,3][2,5][3,5]进行置信度验证。
"""
#def calcConf(freqSet, H, supportData, brl, minConf=0.7):
#    # 针对项集中只有两个元素时，计算可信度
#    prunedH = []  # 返回一个满足最小可信度要求的规则列表
#    for conseq in H:  # 后件，遍历 H中的所有项集并计算它们的可信度值
#        conf = supportData[freqSet] / supportData[freqSet - conseq]  # 可信度计算，结合支持度数据
#        if conf >= minConf:
#            if (2000 in freqSet - conseq):
#                print('True', '-->', conseq, 'conf:', conf)
#                # 如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
#                brl.append((freqSet - conseq, conseq, conf))  # 添加到规则里，brl 是前面通过检查的 bigRuleList
#                prunedH.append(conseq)  # 同样需要放入列表到后面检查
#            if (5000 in freqSet - conseq):
#                print('False', '-->', conseq, 'conf:', conf, '  ')
#                # 如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
#                brl.append((freqSet - conseq, conseq, conf))  # 添加到规则里，brl 是前面通过检查的 bigRuleList
#                prunedH.append(conseq)  # 同样需要放入列表到后面检查
#    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    # 参数:一个是频繁项集,另一个是可以出现在规则右部的元素列表 H
    m = len(H[0])
    if (len(freqSet) > (m + 1)):  # 频繁项集元素数目大于单个集合的元素数
        Hmp1 = aprioriGen(H, m + 1)  # 存在不同顺序、元素相同的集合，合并具有相同部分的集合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)  # 计算可信度
        if (len(Hmp1) > 1):
            # 满足最小可信度要求的规则列表多于1,则递归来判断是否可以进一步组合这些规则
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


if __name__ == "__main__":
    dataSet = loadDataSet();
    L, suppData = apriori(dataSet, minSupport=0.1)
    print(L)
    print(suppData)
    print("rules")
    rules = generateRules(L, suppData, minConf=0.1)
    print(rules)
    
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item]) #store all the item unrepeatly

    C1.sort()
    #return map(frozenset, C1)#frozen set, user can't change it.
    return list(map(frozenset, C1))

def scanD(D,Ck,minSupport):
#参数：数据集、候选项集列表 Ck以及感兴趣项集的最小支持度 minSupport
    ssCnt={}
    for tid in D:#遍历数据集
        for can in Ck:#遍历候选项
            if can.issubset(tid):#判断候选项中是否含数据集的各项
                #if not ssCnt.has_key(can): # python3 can not support
                if not can in ssCnt:
                    ssCnt[can]=1 #不含设为1
                else: ssCnt[can]+=1#有则计数加1
    numItems=float(len(D))#数据集大小
    retList = []#L1初始化
    supportData = {}#记录候选项中各个数据的支持度
    for key in ssCnt:
        support = ssCnt[key]/numItems#计算支持度
        if support >= minSupport:
            retList.insert(0,key)#满足条件加入L1中
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk, k): #组合，向上合并
    #creates Ck 参数：频繁项集列表 Lk 与项集元素个数 k
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): #两两组合遍历
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: #若两个集合的前k-2个项相同时,则将两个集合合并
                retList.append(Lk[i] | Lk[j]) #set union
    return retList


def apriori(dataSet, minSupport = 0.5):
   
    C1 = createC1(dataSet)
    D = list(map(set, dataSet)) #python3
    L1, supportData = scanD(D, C1, minSupport)#单项最小支持度判断 0.5，生成L1
    
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):#创建包含更大项集的更大列表,直到下一个大的项集为空
        Ck = aprioriGen(L[k-2], k)#Ck
        Lk, supK = scanD(D, Ck, minSupport)#get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
        if(k==4):
            break;
    return L, supportData

def generateRules(L, supportData, minConf=0.7):
    #频繁项集列表、包含那些频繁项集支持数据的字典、最小可信度阈值
    bigRuleList = [] #存储所有的关联规则
    for i in range(1, len(L)):  #只获取有两个或者更多集合的项目，从1,即第二个元素开始，L[0]是单个元素的
        # 两个及以上的才可能有关联一说，单个元素的项集不存在关联问题
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            #该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            if (i > 1):
            #如果频繁项集元素数目超过2,那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:#第一层时，后件数为1
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)# 调用函数2
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    #针对项集中只有两个元素时，计算可信度
    prunedH = []#返回一个满足最小可信度要求的规则列表
    for conseq in H:#后件，遍历 H中的所有项集并计算它们的可信度值
        conf = supportData[freqSet]/supportData[freqSet-conseq] #可信度计算，结合支持度数据
        if conf >= minConf:
            if(2000 in freqSet-conseq):
                #print ('True','-->',conseq,'conf:',conf)
                message.logger.info('True %s %s, %s %s','-->',conseq,'conf:',conf)
                #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
                brl.append((freqSet-conseq, conseq, conf))#添加到规则里，brl 是前面通过检查的 bigRuleList
                prunedH.append(conseq)#同样需要放入列表到后面检查
            if(5000 in freqSet-conseq):
                #print ('False','-->',conseq,'conf:',conf,'  ')
                message.logger.info('False %s %s, %s %s','-->',conseq,'conf:',conf)
                #如果某条规则满足最小可信度值,那么将这些规则输出到屏幕显示
                brl.append((freqSet-conseq, conseq, conf))#添加到规则里，brl 是前面通过检查的 bigRuleList
                prunedH.append(conseq)#同样需要放入列表到后面检查
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    #参数:一个是频繁项集,另一个是可以出现在规则右部的元素列表 H
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #频繁项集元素数目大于单个集合的元素数
        Hmp1 = aprioriGen(H, m+1)#存在不同顺序、元素相同的集合，合并具有相同部分的集合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)#计算可信度
        if (len(Hmp1) > 1):
        #满足最小可信度要求的规则列表多于1,则递归来判断是否可以进一步组合这些规则
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
if __name__ == "__main__":
    dataSet=loadDataSet();
    L, suppData = apriori(dataSet, minSupport=0.1)
    print(L)
    print(suppData)
    print("rules")
    rules = generateRules(L, suppData, minConf=0.1)
    print(rules)