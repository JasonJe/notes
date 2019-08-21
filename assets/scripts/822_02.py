import numpy as np
from collections import Counter

class DecisionTree(object):
    '''
    决策树基类
    '''
    def __init__(self, impurity, leaf_value, min_impurity = 1e-7, max_features = None, max_depth = np.inf, min_samples_split = 2, loss = None):
        '''
        impurity, str 树分割方法
        impurity_func, func 树分割方法
        min_impurity, float 计算阈值，选取最优划分特征
        leaf_value, str 树节点取值方法
        leaf_value_func, func 树节点取值方法
        max_features：int 需要考虑的特征数
        max_depth: int 树的最大深度
        min_samples_split：int 内部节点需要的最小样本数
        loss: 
        '''
        self.tree = None

        self.impurity = impurity
        self.impurity_func = None
        self.min_impurity = min_impurity

        self.leaf_value = leaf_value
        self.leaf_value_func = None

        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
    
    def _split(self, data_set, feature, value):
        '''
        划分数据集，获得左右子树

        data_set, numpy.array 需要划分的数据集
        feature, 特征值
        value, 划分阈值
        '''
        if isinstance(value, int) or isinstance(value, float): # 考虑数值型特征
            left = data_set[np.nonzero(data_set[:, feature] >= value)[0], :]
            right = data_set[np.nonzero(data_set[:, feature] < value)[0], :]
        else: # 考虑非数值型特征
            left = data_set[np.nonzero(data_set[:, feature] == value)[0], :]
            right = data_set[np.nonzero(data_set[:, feature] != value)[0], :]
        return left, right

    def _choose_best_feature(self, data_set, max_features, current_depth):
        '''
        选取最优特征

        data_set, numpy.array 需要进行计算的数据集
        max_features, int 需要考虑的特征数
        current_depth, int 当前树的深度
        '''
        best_criteria = None
        largest_impurity = 0.0
        n_samples, n_features = data_set[:, :-1].shape

        if not max_features:
            features = n_features

        if n_samples >= self.min_samples_split and current_depth <= self.max_depth: # 样本数小于最小样本数 或 当前树深度大于等于最大设定深度时候跳出
            for feature in range(features): # 遍历所有特征
                thresholds = np.unique(data_set[:, feature]) # 当前特征的唯一值列表

                for threshold in thresholds:
                    left, right = self._split(data_set, feature, threshold) # 根据特征和相应的特征值进行左右子树划分
                    
                    if (left.shape[0] > 0) and (right.shape[0] > 0):
                        split_impurity = self.impurity_func(data_set, left, right) # 计算最优划分
                        if split_impurity > largest_impurity:
                            largest_impurity = split_impurity # 更新最优划分
                            best_criteria = dict(
                                largest_impurity = largest_impurity,
                                best_feature = feature,
                                best_threshold = threshold,
                                left = left,
                                right = right
                            )
        return best_criteria
    
    def _create_tree(self, data_set, max_features, current_depth = 0):
        '''
        递归创建树

        data_set, numpy.array 需要进行计算的数据集
        max_features, int 需要考虑的特征数
        current_depth, 当前树深度
        '''
        if data_set.shape[0] == 0:
            return
        
        best_criteria = self._choose_best_feature(data_set, max_features, current_depth) # 获取最优划分

        if best_criteria is not None:
            best_feature, best_threshold, largest_impurity, left, right = best_criteria['best_feature'], best_criteria['best_threshold'], best_criteria['largest_impurity'], best_criteria['left'], best_criteria['right']

            tree = {}
            if largest_impurity > self.min_impurity: # 生成树，左右子树
                tree['left'] = self._create_tree(left, max_features, current_depth + 1)
                tree['right'] = self._create_tree(right, max_features, current_depth + 1)
                tree['feature'] = best_feature
                tree['threshold'] = best_threshold
                return tree

        tree = {} # 叶子节点生成
        value = self.leaf_value_func(data_set[:, -1])
        tree['value'] = value
        return tree
    
    def _predict_by_tree(self, tree, test_data):
        '''
        递归进行预测

        tree, dict 训练得到的树
        test_data, numpy.array 测试数据集
        '''
        if tree is None: # 树为空，从根节点重新开始
            tree = self.tree
        if tree.get('value', None) is not None: # 到达叶子节点，返回叶子值
            return tree['value']
        else:
            feature = tree['feature']
            threshold = tree['threshold']
            if isinstance(feature, int) or isinstance(feature, float): # 数值型特征划分方法
                if test_data[feature] >= threshold:
                    return self._predict_by_tree(tree['left'], test_data)
                else: 
                    return self._predict_by_tree(tree['right'], test_data)
            else: # 非数值型特征划分方法
                if test_data[feature] == threshold:
                    return self._predict_by_tree(tree['left'], test_data)
                else: 
                    return self._predict_by_tree(tree['right'], test_data)

    def predict(self, test_data):
        '''
        预测

        test_data, numpy.array 测试数据集
        '''
        test_data = np.array(test_data)
        prediction = []
        for data in test_data: # 遍历测试数据
            prediction.append(self._predict_by_tree(self.tree, data))
        return prediction

class DecisionTreeClassifier(DecisionTree):
    '''
    决策分类树
    '''
    def __init__(self, impurity, leaf_value):
        super().__init__(impurity, leaf_value)
        
    def _shannon_ent(self, data_set):
        '''
        计算信息熵
        
        data_set, numpy.array 需要进行计算的数据集
        '''
        shannon_ent = 0.0
        labels_counts = Counter(data_set[:, -1].tolist())
        for key in labels_counts:
            prob = float(labels_counts[key]) / data_set[:, :-1].shape[0]
            shannon_ent -= prob * np.log2(prob)
        return shannon_ent

    def _gain(self, data_set, left, right):
        '''
        计算信息增益
        
        data_set, numpy.array 需要进行计算的数据集
        left, numpy.array 需要进行计算的左子树数据集
        right, numpy.array 需要进行计算的右子树数据集
        '''
        prob = left.shape[0] / data_set.shape[0]
        entropy = self._shannon_ent(data_set)
        info_gain = entropy - prob * self._shannon_ent(left) - (1 - prob) * self._shannon_ent(right)
        return info_gain
        
    def _gini(self, data_set, left, right):
        '''
        计算基尼指数
        
        data_set, numpy.array 需要进行计算的数据集
        left, numpy.array 需要进行计算的左子树数据集
        right, numpy.array 需要进行计算的右子树数据集
        '''
        gini = 1
        labels_counts = Counter(data_set[:, -1].tolist())
        for key in labels_counts:
            prob = float(labels_counts[key]) / data_set[:, :-1].shape[0]
            gini -= np.power(prob, 2)
        return gini
    
    def _vote(self, y):
        '''
        投票法确定最后类别

        y, numpy.array 类别数组
        '''
        return Counter(y.tolist()).most_common(1)[0][0]
    
    def fit(self, X, y, max_features = None):
        '''
        训练模型
        
        X, numpy.array 样本数组
        y, numpy.array 类别数组、
        max_features, int 需要考虑的特征数 
        '''
        if self.impurity == 'gain':
            self.impurity_func = self._gain
        else:
            self.impurity_func = self._gini
        self.leaf_value_func = self._vote
        data_set = np.concatenate((X, y.reshape(X.shape[0], 1)), axis=1)
        self.tree = self._create_tree(data_set, max_features)

class DecisionTreeRegressor(DecisionTree):
    '''
    决策回归树
    '''
    def __init__(self):
        super().__init__(impurity = None, leaf_value = None)
    
    def _var(self, data_set, left, right):
        '''
        计算方差
        
        data_set, numpy.array 需要进行计算的数据集
        left, numpy.array 需要进行计算的左子树数据集
        right, numpy.array 需要进行计算的右子树数据集
        '''
        variance_reduction = np.var(data_set[:, -1]) - (left.shape[0] / data_set.shape[0] * np.var(left[:, -1]) + right.shape[0] / data_set.shape[0] * np.var(right[:, -1]))
        return np.sum(variance_reduction)
    
    def _mean(self, y):
        '''
        计算均值

        y, numpy.array 类别数组
        '''
        value = np.mean(y, axis=0)
        return value

    def fit(self, X, y, max_features = None):
        '''
        训练模型
        
        X, numpy.array 样本数组
        y, numpy.array 类别数组、
        max_features, int 需要考虑的特征数 
        '''
        self.impurity_func = self._var
        self.leaf_value_func = self._mean
        data_set = np.concatenate((X, y.reshape(X.shape[0], 1)), axis=1)
        self.tree = self._create_tree(data_set, max_features)

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn import tree, preprocessing, datasets
    from sklearn.cross_validation import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, mean_squared_error

    # =========== Classification Tree ===========
    X, y = datasets.make_classification(n_samples = 100, n_features = 5, n_classes = 2) # 生成100个2分类的样本，特征数量为100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    impurity, leaf_value = 'gain', 'vote'
    dtc = DecisionTreeClassifier(impurity, leaf_value)
    dtc.fit(X_train, y_train)
    y_pred = dtc.predict(X_test)
    print("Accuracy is: ", accuracy_score(y_test, y_pred))

    # =========== Regression Tree ===========
    X, y = datasets.make_regression(n_samples=100, n_features=1,n_targets=1, noise=2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    dtr = DecisionTreeRegressor()
    dtr.fit(X_train, y_train)

    y_pred = dtr.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print("Mse is: ", mse)

    cmap = plt.get_cmap('viridis')
    test = plt.scatter(366 * X_test, y_test, color = cmap(0.5), s=10)
    pred = plt.scatter(366 * X_test, y_pred, color = 'red', s=10)
    plt.suptitle("Regression Tree")
    plt.title("Mse: %.2f" % mse, fontsize=10)
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend((test, pred), ("Test data", "Prediction"), loc='lower right')
    plt.show()

