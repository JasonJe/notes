import pandas as pd # 导入pandas库
import numpy as np # 导入numpy库

data = pd.read_csv('822_01.txt', ',', index_col='编号')
labels = list(data.columns)
dataSet = np.array(data).tolist() # 处理读入数据为list类型，方便后续计算

#### 实现根结点信息熵的计算

from math import log

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)#计算样本集的总样本数量
    labelCounts = {}#设置一个空的dict类型变量
    for featVec in dataSet:#遍历每行样本集
        currentLabel = featVec[-1]#选取样本集最后一列，设置为labelCounts变量的key值
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0#key对应value初始化
        labelCounts[currentLabel] += 1#累计value，即计算同类别样本数
    shannonEnt = 0.0#初始化信息熵
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries#计算频率
        shannonEnt -= prob * log(prob, 2)#计算信息熵
    return shannonEnt

print(calcShannonEnt(dataSet))

#### 计算不同子属性信息熵

def splitDataSet(dataSet, axis, value):
    #dataSet为样本集
    #axis为子属性下标，如0代表子属性“色泽”
    #value为上述子属性取值
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

newdataSet1=splitDataSet(dataSet, 0, '青绿')#将为“青绿”的样本集合划分出来
newdataSet2=splitDataSet(dataSet, 0, '乌黑')#将为“青绿”的样本集合划分出来
newdataSet3=splitDataSet(dataSet, 0, '浅白')#将为“青绿”的样本集合划分出来

print(newdataSet1)
print(newdataSet2)
print(newdataSet3)

print(calcShannonEnt(newdataSet1))
print(calcShannonEnt(newdataSet2))
print(calcShannonEnt(newdataSet3))

#### 实现信息增益的计算

numFeatures = len(dataSet[0]) - 1#计算子属性的数量
baseEntropy = calcShannonEnt(dataSet)#计算根结点信息熵
columns=['色泽','根蒂','敲声','纹理','脐部','触感']#子属性
for i in range(numFeatures):
    featList = [example[i] for example in dataSet]
    uniqueVals = set(featList)
    newEntropy = 0.0
    for value in uniqueVals:
        #根据子属性及其取值划分样本子集
        subDataSet = splitDataSet(dataSet, i, value)
        prob = len(subDataSet) / float(len(dataSet))#权值
        newEntropy += prob * calcShannonEnt(subDataSet)
        print(value,'的信息熵为：',calcShannonEnt(subDataSet))#不同取值的信息熵
    infoGain = baseEntropy - newEntropy#计算信息增益
    print(columns[i],'信息增益为：',infoGain)
    print('----------------------------------')

#### 基于信息增益选择最优划分属性
def chooseBestFeatureToSplit_Gain(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0#初始最优信息增益
    bestFeature = -1#初始最优子属性
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):#选择最优子属性
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

print(chooseBestFeatureToSplit_Gain(dataSet))

#### 基于信息增益率划分最优子属性

def chooseBestFeatureToSplit_GainRatio(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestGainRatio = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        iv = 0.0#初始化“固有值”
        GainRatio = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            iv -= prob * log(prob, 2)#计算每个子属性“固有值”
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        GainRatio = infoGain / iv#计算信息增益率
        if (GainRatio > bestGainRatio):#选择最优节点
            bestGainRatio = GainRatio
            bestFeature = i
    return bestFeature

print(chooseBestFeatureToSplit_GainRatio(dataSet))

#### 实现了基尼指数的计算

def calcGini(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        Gini = 1.0
        for key in labelCounts:
            prob = float(labelCounts[key]) / numEntries
            Gini -= prob * prob
    return Gini

print(calcGini(dataSet)) # 根结点基尼指数

#### 基于基尼指数选择最优划分属性(只能对离散型特征进行处理)
def chooseBestFeatureToSplit_Gini(dataSet):
    numFeatures = len(dataSet[0]) - 1
    bestGini = 100000.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newGiniIndex = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newGiniIndex += prob * calcGini(subDataSet)
        if (newGiniIndex < bestGini):
            bestGini = newGiniIndex
            bestFeature = i
    return bestFeature

print(chooseBestFeatureToSplit_Gini(dataSet))

#### 创建树

import operator

# 选择下一个根结点
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0#初始化子属性取值的计数
        classCount[vote] += 1#累计
    #根据第二个域，即dict的value降序排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]#返回子属性取值

# 创建树
def createTree(dataSet, labels, chooseBestFeatureToSplit):
    classList = [example[-1] for example in dataSet]#初始化根结点
    if classList.count(classList[0]) == len(classList):#只存在一种取值情况
        return classList[0]
    if len(dataSet[0]) == 1:#样本集只存在一个样本情况
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)#最优划分属性选取
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}#初始化树
    del (labels[bestFeat])#删除已划分属性
    featValues = [example[bestFeat] for example in dataSet]#初始化下层根结点
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        #遍历实现树的创建
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels, chooseBestFeatureToSplit)
    return myTree

chooseBestFeatureToSplit=chooseBestFeatureToSplit_Gain#根据信息增益创建树
# chooseBestFeatureToSplit=chooseBestFeatureToSplit_GainRatio#根据信息增益率创建树
# chooseBestFeatureToSplit=chooseBestFeatureToSplit_Gini#根据基尼指数创建树
myTree = createTree(dataSet, labels, chooseBestFeatureToSplit)

print(myTree)

#### 分类器实现

# 分类测试器
def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]#下一层树
    featIndex = featLabels.index(firstStr)#将Labels标签转换为索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:#判断是否为与分支节点相同，即向下探索子树
            if type(secondDict[key]).__name__ == 'dict':
                #递归实现
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel#返回判断结果

print(classify(myTree, ['色泽','根蒂','敲声','纹理','脐部','触感'],['乌黑','稍蜷','沉闷','稍糊','稍凹','硬滑']))

#### 保存和加载树

# 保存树
def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'wb+')
    pickle.dump(inputTree,fw)
    fw.close()

# 加载树
def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)

storeTree(myTree,'822_02.txt') # 保存到822_02.txt文件中
grabTree('822_02.txt') # 加载保存的决策树

#### 使用Scikit - Learn库实现决策树

import numpy as np
import pandas as pd
from sklearn import tree, preprocessing

'''由于在此库中需要使用数值进行运算，这里需要对样本集进行处理'''
data = pd.read_csv('822_01.txt', ',', index_col='编号')
for col in data.columns:
    data[col] = preprocessing.LabelEncoder().fit_transform(data[col])
labels = np.array(data['好瓜'])
dataSet = np.array(data[data.columns[:-1]])

clf = tree.DecisionTreeClassifier(criterion = 'entropy')#参数criterion = 'entropy'为基于信息熵，‘gini’为基于基尼指数
clf.fit(dataSet, labels)#训练模型
print(clf)

with open("822_01.dot", 'w') as f:#将构建好的决策树保存到tree.dot文件中
    f = tree.export_graphviz(clf,feature_names = np.array(data.columns[:-1]), out_file = f)