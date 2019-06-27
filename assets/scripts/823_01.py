import numpy as np
import pandas as pd

#获取各个类别条件概率
def get_pred(dataSet, inputSimple):
    p0classData = []#初始化类别矩阵
    p1classData = []
    classLabels = dataSet[dataSet.columns[-1]]#选取类别列
    for i in range(len(dataSet.columns) - 1):
        columnLabels = dataSet[dataSet.columns[i]]#特征列
        pData = pd.concat([columnLabels, classLabels], axis = 1)#拼接特征列和类别列
        classSet = list(set(classLabels))
        for pclass in classSet:
            filterClass = pData[pData[pData.columns[-1]] == pclass]#根据类别划分数据集
            filterClass = filterClass[pData.columns[-2]]
            if isinstance(inputSimple[i], float):#判断是否是连续变量
                classVar = np.var(filterClass)#方差
                classMean = np.mean(filterClass)#均值
                pro_l = 1/(np.sqrt(2*np.pi) * np.sqrt(classVar))
                pro_r = np.exp(-(inputSimple[i] - classMean)**2/(2 * classVar))
                pro = pro_l * pro_r#概率
                if pclass == '是':
                    p0classData.append(pro)
                else:
                    p1classData.append(pro)
            else:
                classNum = np.count_nonzero(filterClass == inputSimple[i])#计算属于样本特征的数量
                pro = (classNum + 1)/(len(filterClass) + len(set(filterClass)))#此处进行了拉普拉斯修正
                if pclass == '是':
                    p0classData.append(pro)
                else:
                    p1classData.append(pro)
    return p0classData, p1classData

filename = '821_02.txt'
dataSet = pd.read_csv(filename, sep = ',', index_col = '编号')
inputSimple = ['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.697, 0.460]
p0classData, p1classData = get_pred(dataSet, inputSimple)
if np.prod(p0classData) > np.prod(p1classData):#计算条件概率的累积
    print('该瓜是好瓜！')
else:
    print('烂瓜！')

testData =[list(dataSet.ix[i][:-1]) for i in range(1,len(dataSet) + 1)]#list化
testLabels = []
for test in testData:
    p0classData, p1classData = get_pred(dataSet, test)
    if np.prod(p0classData) > np.prod(p1classData):
        testLabels.append('是')#保存测试结果
    else:
        testLabels.append('否')
accuracy = np.mean(testLabels == dataSet[dataSet.columns[-1]])
print('模型精度为%f' %accuracy)

#### Sklearn库简单实现朴素贝叶斯

import pandas as pd

filename = '821_02.txt'
dataSet = pd.read_csv(filename, sep = ',', index_col = '编号')

#哑变量处理
featureDict = []
new_dataSet = pd.DataFrame()
for i in range(len(dataSet.columns)):
    featureList = dataSet[dataSet.columns[i]]
    classSet = list(set(featureList))
    count = 0
    for feature in classSet:
        d = dict()
        if isinstance(feature, float):#判断是否为连续变量
            continue
        else:
            featureList[featureList == feature] = count
            d[feature] = count
            count += 1
        featureDict.append(d)
    new_dataSet = pd.concat([new_dataSet, featureList], axis = 1)

import numpy as np
from sklearn.naive_bayes import MultinomialNB

#设置训练数据集
X = [list(new_dataSet.ix[i][:-1]) for i in range(1,len(new_dataSet) + 1)]
Y = list(new_dataSet[new_dataSet.columns[-1]])

clf = MultinomialNB()#分类器
clf.fit(X, Y)#训练
print(clf)
predicted = clf.predict(X)
print('精度为：%f ' %np.mean(predicted == Y))