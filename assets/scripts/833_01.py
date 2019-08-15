import numpy as np

def load_dataset(filepath):
    '''
    加载数据集，并转化为矩阵
    '''
    data_mat, label_mat= [], []
    f = open(filepath)
    for line in f.readlines():
        line_list = line.split(',')
        data_mat.append([float(i) for i in line_list[:-1]])
        label_mat.append(float(line_list[-1]))
    data = np.mat(data_mat)
    labels = np.mat(label_mat).T
    return data, labels

def _weak_classifier(data, feature, thresh, thresh_inequal):
    '''
    弱分类器定义，基于阈值对类别进行划分
    '''
    result = np.ones((data.shape[0], 1))
    if thresh_inequal == 'lt':
        result[data[:, feature] <= thresh] = -1.0
    else:
        result[data[:, feature] > thresh] = -1.0
    return result

def _find_best_classifier(data, labels, D):
    '''
    找到最优的分类器，选择能在两类中使得误差降到最低的特征
    '''
    m, n = data.shape
    num_steps = 10.0
    best_classifier = {}
    best_classification_result = np.mat(np.zeros((m, 1)))
    min_error = np.inf # 初始化最小误差为无穷大

    for i in range(n): # 遍历数据集的所有特征
        min_feature = data[:, i].min() # 每列特征中的最小值
        max_feature = data[:, i].max() # 每列特征中的最大值
        step = (max_feature - min_feature) / num_steps # 步长
        for j in range(-1, int(num_steps) + 1): # 
            for ineuqal in ['lt', 'gt']:
                thresh = (min_feature + float(j) * step) # 计算阈值
                prediction = _weak_classifier(data, i, thresh, ineuqal) # 弱分类器预测的结果
                error = np.mat(np.ones((m, 1)))
                error[prediction == labels] = 0 # 计算误差
                weighted_error = D.T * error # 计算权重

                if weighted_error < min_error: # 更新最小误差
                    min_error = weighted_error
                    best_classification_result = prediction.copy()
                    best_classifier['feature'] = i
                    best_classifier['thresh'] = thresh
                    best_classifier['ineq'] = ineuqal
    return best_classifier, min_error, best_classification_result

def adaboost_train(data, labels, max_iter = 40):
    weak_classifier = []
    m = data.shape[0]
    D = np.mat(np.ones((m ,1)) / m) # 样本权重向量
    alpha_classification_result = np.mat(np.zeros((m, 1)))

    for i in range(max_iter): # 迭代 max_iter 次
        best_classifier, error, classification_result = _find_best_classifier(data, labels, D) # 获取该次迭代的最优弱分类器

        alpha = float(0.5 * np.log((1.0 - error) / max(error, 1e-16)))
        best_classifier['alpha'] = alpha # 计算 alpha，防止分母为零，使用 max(error, 1e-16)

        weak_classifier.append(best_classifier)

        D = np.multiply(D, np.exp(np.multiply(-1 * alpha * labels, classification_result)))
        D = D / D.sum() # 更新权重矩阵

        alpha_classification_result += alpha * classification_result # 投票法更新预测结果
        e_m = np.multiply(np.sign(alpha_classification_result) != labels, np.ones((m ,1))) # 计算错误个数

        error_rate = e_m.sum() / m # 计算错误率
        if error_rate == 0.0:
            break
    return weak_classifier, alpha_classification_result # 返回每轮迭代的最优弱分类器和对应权重

def predict(data, weak_classifier):
    m = data.shape[0]
    alpha_classification_result = np.mat(np.zeros((m, 1)))
    for classifier in weak_classifier:
        result = _weak_classifier(data, classifier['feature'], classifier['thresh'], classifier['ineq'])
        alpha_classification_result += classifier['alpha'] * result # 投票法更新预测结果
    return np.sign(alpha_classification_result)

if __name__ == "__main__":
    data, labels = load_dataset('833_01.txt')
    weak_classifier, alpha_classification_result = adaboost_train(data, labels)
    prediction = predict(data, weak_classifier)
    error = np.mat(np.ones((data.shape[0], 1)))
    print('训练集的准确率:%.3f%%' % float(100 - error[prediction != labels].sum() / data.shape[0] * 100))

    test_data, test_labels = load_dataset('833_02.txt')
    prediction = predict(test_data, weak_classifier)
    error = np.mat(np.ones((test_data.shape[0], 1)))
    print('测试集的准确率:%.3f%%' % float(100 - error[prediction != test_labels].sum() / test_data.shape[0] * 100))

    from sklearn.ensemble import AdaBoostClassifier # 使用 Scikit-Learn 内置的 AdaBoost 分类模块进行分类

    clf = AdaBoostClassifier(n_estimators = 40, random_state = 0)
    clf.fit(data, labels)
    print(clf)

    print('训练集的准确率:%.3f%%' % (clf.score(data, labels) * 100))
    print('测试集的准确率:%.3f%%' % (clf.score(test_data, test_labels) * 100))