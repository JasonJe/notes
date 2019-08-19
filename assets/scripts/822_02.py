import numpy as np
from collections import Counter

class DecisionTree(object):
    def __init__(self, criterion, splitter, max_features = None, max_depth = None, min_samples_split = 2, loss = None):
        '''
        criterion：str, 分类质量衡量
        splitter：str, 分类策略
        max_features：int, 需要考虑的特征数
        max_depth: int, 树的最大深度
        min_samples_split：int, 内部节点需要的最小样本数
        '''
        self.root = None
        self.criterion = criterion
        self.splitter = splitter
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
    
class DecisionTreeClassifier(DecisionTree):
    def __init__(self, X, y, criterion, splitter):
        super().__init__(criterion, splitter)
        self.data_set = np.hstack((X, y))
    
    def _shannon_ent(self, data_set):
        
        shannon_ent = 0.0
        labels_counts = Counter(data_set[:, -1].flatten().tolist()[0])
        for key in labels_counts:
            prob = float(labels_counts[key]) / data_set[:, :-1].shape[0]
            shannon_ent -= prob * np.log2(prob)
        return shannon_ent
    
    def _gini(self, data_set):
        gini = 1
        labels_counts = Counter(data_set[:, -1].flatten().tolist()[0])
        for key in labels_counts:
            prob = float(labels_counts[key]) / data_set[:, :-1].shape[0]
            gini -= np.power(prob, 2)
        return gini

    def _split(self, feature, value):
        left = self.data_set[np.nonzero(self.data_set[:, feature] == value)[0], :]
        right = self.data_set[np.nonzero(self.data_set[:, feature] != value)[0], :]
        return left, right

    def _choose_best_feature(self):
        best_feature = -1
        best_value = 0
        min_criterion = np.inf
        split_criterion = 0
        n_samples, n_features = self.data_set[:, :-1].shape

        features = n_features

        for feature in range(features):
            values = np.unique(self.data_set[:, feature])
            for value in values:
                left, right = self._split(feature, value)
                if self.criterion == 'gain':
                    split_criterion = left.shape[0] / n_samples * self._shannon_ent(left) + right.shape[0] / n_samples * self._shannon_ent(right)
                else:
                    split_criterion = left.shape[0] / n_samples * self._gini(left) + right.shape[0] / n_samples * self._gini(right)
                if split_criterion < min_criterion:
                    min_criterion = split_criterion
                    best_feature = feature
                    best_value = value
        return best_feature, best_value


        
if __name__ == "__main__":
    import pandas as pd
    from sklearn import tree, preprocessing

    data = pd.read_csv('822_01.txt', ',', index_col='编号')
    labels = list(data.columns)
    for col in data.columns:
        data[col] = preprocessing.LabelEncoder().fit_transform(data[col])
    labels = np.mat(data['好瓜']).T
    dataSet = np.mat(data[data.columns[:-1]])

    criterion, splitter = 'gain', 'max'

    dtc = DecisionTreeClassifier(dataSet, labels, criterion, splitter)
    a = dtc._choose_best_feature()
    print('1111', a)