import numpy as np
import pandas as pd
from collections import Counter

def _calc_gini(data_set):
    '''
    计算基尼指数
    $gini = 1 - \sum_{k = 1}^{K} p_k^2$
    $k$为类别
    '''
    gini = 1
    labels = Counter(data_set[:, -1].tolist()) # 标签列
    for amount in labels.values():
        prob = amount / data_set.shape[0] # 类别 amount 的概率
        gini -= np.power(prob, 2)
    return gini

def _bootstrap(data_set):
    '''
    自助法进行采样
    '''
    m = data_set.shape[0]
    choosed_feature = np.random.choice(m, m, replace = True) # 可重复采样
    train_data = data_set[choosed_feature, :]
    return train_data

def _split(data_set, feature, value):
    '''
    分离数据集，只针对离散型数据集
    '''
    left = data_set[np.nonzero(data_set[:, feature] == value)[0], :]
    right = data_set[np.nonzero(data_set[:, feature] != value)[0], :]
    return left, right

def _choose_best_feature(data_set, max_features):
    '''
    基于基尼指数选取最优特征
    '''
    best_feature = -1
    best_value = 0
    min_gini = np.inf
    split_gini = 0
    n = data_set.shape[1] - 1

    rand_feature = np.random.choice(n, max_features, replace = False) # 随机选择特征，最多 max_features 个

    for feature in rand_feature:
        values = np.unique(data_set[:, feature]) # 获取该特征的唯一值列表
        for value in values:
            left, right = _split(data_set, feature, value) # 按照该特征进行划分
            split_gini = left.shape[0] / data_set.shape[0] * _calc_gini(left) + right.shape[0] / data_set.shape[0] * _calc_gini(right)
            if split_gini < min_gini:
                min_gini = split_gini
                best_feature = feature
                best_value = value

    return best_feature, best_value

def _create_tree(data_set, max_features):
    if data_set.shape[0] == 0:
        return
    if np.unique(data_set[:, -1]).shape[0] == 1:
        return data_set[0, -1]
    
    best_feature, best_value = _choose_best_feature(data_set, max_features)

    tree = {}
    tree['feature'] = best_feature
    tree['value'] = best_value
    left, right = _split(data_set, best_feature, best_value)
    tree['left'] = _create_tree(left, max_features)
    tree['right'] = _create_tree(right, max_features)
    return tree

def fit(data_set, n_estimators, max_features):
    data_set = np.array(data_set)
    rand_forests = []
    for i in range(n_estimators):
        train_data = _bootstrap(data_set)
        tree = _create_tree(train_data, max_features)
        rand_forests.append(tree)
    
    return rand_forests

def _predict_by_tree(tree, test_data):
    if not isinstance(tree, dict): 
        return tree
    feature = tree['feature']
    value = tree['value']
    if test_data[feature] == value:
        return _predict_by_tree(tree['left'], test_data)
    else: 
        return _predict_by_tree(tree['right'], test_data)

def predict(rand_forests, test_data):
    test_data = np.array(test_data)
    prediction = []
    for data in test_data:
        temp = []
        if isinstance(data, np.ndarray):
            for tree in rand_forests:
                temp.append(_predict_by_tree(tree, data))
            prediction.append(Counter(temp).most_common(1)[0][0])
        else:
            for tree in rand_forests:
                temp.append(_predict_by_tree(tree, test_data))
            prediction.append(Counter(temp).most_common(1)[0][0])
            break
    return prediction

if __name__ == "__main__":
    from sklearn.datasets import make_classification # 生成200个2分类的样本，特征数量为100
    data, lables = make_classification(n_samples = 200, n_features = 100,n_classes = 2)
    data_set = np.concatenate((data, lables.reshape(200, 1)), axis=1)
    np.random.shuffle(data_set) # 随机打乱数据

    train_data_set = data_set[:150, :] # 选取 75% 数据进行训练
    rand_forests = fit(train_data_set, n_estimators = 4, max_features = 20)
    prediction = predict(rand_forests, train_data_set[:, : -1])
    correct = [1 if a == b else 0 for a, b in zip(prediction, train_data_set[:, -1])]
    print('训练集的准确率:%.3f%%' % (correct.count(1) / 150 * 100))
    
    test_data_set = data_set[150:, : -1] # 选取 25% 数据进行测试
    test_labels = data_set[150:, -1]
    
    prediction = predict(rand_forests, test_data_set)
    correct = [1 if a == b else 0 for a, b in zip(prediction, test_labels)]
    print('测试集的准确率:%.3f%%' % (correct.count(1) / 50 * 100))

    from sklearn.ensemble import RandomForestClassifier # 使用 Scikit-Learn 内置的随机森林分类模块进行分类

    rf = RandomForestClassifier(max_features = 20, n_estimators = 4) 
    rf.fit(train_data_set[:, :-1], train_data_set[:, -1])
    print(rf)

    prediction = rf.predict(train_data_set[:, :-1])
    correct = [1 if a == b else 0 for a, b in zip(prediction, train_data_set[:, -1])]
    print('训练集的准确率:%.3f%%' % (correct.count(1) / 150 * 100))

    prediction = rf.predict(test_data_set)
    correct = [1 if a == b else 0 for a, b in zip(prediction, test_labels)]
    print('测试集的准确率:%.3f%%' % (correct.count(1) / 50 * 100))