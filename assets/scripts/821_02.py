#导入numpy和pandas库
import numpy as np
import pandas as pd

#解析数据文件
def loadDataSet(filename):
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

    dataMat = [list(new_dataSet.loc[i][:-1]) for i in range(1,len(new_dataSet) + 1)]
    labelMat = list(new_dataSet[new_dataSet.columns[-1]])
    return dataMat, labelMat

filename = '821_02.txt'
dataMat, labelMat = loadDataSet(filename)

import pprint
pprint.pprint(dataMat)
pprint.pprint(labelMat)

# 定义Sigmoid函数
def sigmoid(inX):
    return 1.0/(1 + np.exp(- inX))

# 随机的梯度上升法
def gradAscent(dataMatIn, classLabels, numIter = 150):
    # 获得行数和列数，即样本数和特征数
    m, n = np.shape(dataMatIn)
    # 权重初始化
    weights = np.ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0 + j + i) + 0.01
            randIndex = int(np.random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMatIn[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights = weights + np.dot(alpha * error, dataMatIn[randIndex])
    return weights

weights = gradAscent(dataMat, labelMat)
print(weights)

def classfy(testdir, weights):
    dataMat, labelMat = loadDataSet(testdir)
    dataMat = np.mat(dataMat)
    weights = np.mat(weights)
    h = sigmoid(dataMat * weights.transpose())
    h = h.tolist()
    m = len(h)
    error = 0.0
    for i in range(m):
        if h[i][0] > 0.5:
            print(int(labelMat[i]),'is classfied as: 1')
            if int(labelMat[i])!=1:
                error += 1
                print('error')
        else:
            print(int(labelMat[i]),'is classfied as: 0')
            if int(labelMat[i])!=0:
                error += 1
                print('error')
    print('error rate is:','%.4f' %(error/m))

print(classfy(filename, weights))

#### 通过Scikit - Learn库实现Logistic的分类

from sklearn.linear_model import LogisticRegression

X, Y = loadDataSet(filename)

clf = LogisticRegression()
clf.fit(X, Y)
print(clf)
y_pred = clf.predict(X)
accuracy = np.mean(Y == y_pred)
print('准确度为：', accuracy)