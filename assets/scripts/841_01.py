import numpy as np
import operator

filename = '822_01.txt'
def factor2dummy_variable(filename):
    fr = open(filename,encoding = 'utf-8')#以utf-8读取文件
    dataColumns = fr.readline()#去除首行
    arrayLines = fr.readlines()#读取所有行
    lines = np.array([line.replace('\n','').split(',') for line in arrayLines]).T#按行指定分隔符，并进行转置
    lines = lines[1:,:]#实际使用的数据部分
    setFactors = [set(line) for line in lines]#set操作，只保存一种分类的集合
    k = 0
    for i in setFactors:
        dummy_num = 0
        line = lines[k]
        for j in i:
            line[line == j] = dummy_num#哑变量转换
            dummy_num += 1
        k += 1
    lines = lines.T#转置
    return lines

lines = factor2dummy_variable(filename)
dataSet = lines
filename = '841_01.txt'
def data2txt(dataSet,filename):
    fw = open(filename,'w',encoding='utf-8')#以utf-8编码写入
    for line in dataSet:
        for element in line:
            fw.write(element)
            fw.write(',')#tab键分割符号
        fw.write('\n')#换行
    fw.close()

data2txt(dataSet, filename)

filename = '841_01.txt'
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()#读取所有行
    numberOfLines = len(arrayOLines)#计算记录数量
    numberOfcloumns = len(arrayOLines[0].replace(',\n','').split(',')) - 1#计算变量数量
    returnMat = np.zeros((numberOfLines, numberOfcloumns))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()#去除空格
        listFromLine = line.split(',')#按tab键分割
        returnMat[index, :] = listFromLine[:-2]#得到分类变量数组
        classLabelVector.append(int(listFromLine[-2]))#类别变量数组
        index += 1
    return returnMat, classLabelVector

def autoNorm(dataSet):
    minValue = dataSet.min(0)#得到每列的最小值
    maxValue = dataSet.max(0)#每列最大值
    ranges = maxValue - minValue#分母
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]#行数
    normDataSet = dataSet - np.tile(minValue, (m,1))#分子
    normDataSet = normDataSet/np.tile(ranges, (m,1))
    return normDataSet, ranges, minValue

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]#得到行数
    diffMat = np.tile(inX, (dataSetSize,1)) - dataSet#计算输入向量inX与训练样本的差
    sqDiffMat = diffMat**2#计算差值的平方
    sqDistances = sqDiffMat.sum(axis = 1)#距离平方和
    distances = sqDistances**0.5#开方得到距离
    sortedDistIndicies = distances.argsort()#距离进行排序,得到排序的下标
    classCount = {}
    for i in range(k):#确定前k个距离中最小元素所属分类
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1#对出现的label进行计数
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)#按照计数值进行降序排序
    #operator.itemgetter(1)确定一个函数取出classCount中的第一个域的值，即将value取出
    return sortedClassCount[0][0]#返回最大的计数值的分类

dataLines, datalabels = file2matrix('841_01.txt')
i=0
errorCount = 0.0
for line in dataLines:
    print('记录%s的原始分类是:%d，划分分类是:%d' %(str(line), datalabels[i], classify0(line, dataLines ,datalabels, 1)))
    if (datalabels[i] != classify0(line, dataLines ,datalabels, 1)):
        errorCount += 1.0
    i += 1
print('错误率为: %f' %(errorCount/float(len(dataLines))))

#### Sklearn 实现kNN过程
import numpy as np
from sklearn import neighbors

data = []
labels = []
with open('841_01.txt') as ifile:
    for line in ifile:
        tokens = line.replace(',\n','').split(',')
        data.append([float(tk) for tk in tokens[:-1]])
        labels.append(tokens[-1])
x = np.array(data)
y = np.array(labels)

clf = neighbors.KNeighborsClassifier(algorithm = 'kd_tree', n_neighbors = 1)
clf.fit(x,y)

answer = clf.predict(x)
print('准确率为:%f' % float(np.mean(answer == y)))#正确率