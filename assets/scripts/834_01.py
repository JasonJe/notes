import numpy as np
from collections import Counter

from decision_tree import DecisionTreeRegressor

class GBDT(object):
    def __init__(self, n_estimators, learning_rate, min_samples_split, min_impurity, max_depth, is_regression):
        '''
        n_estimators, int 树的数量
        learning_rate, float 梯度下降的学习率
        min_samples_split, int 内部节点需要的最小样本数
        min_impurity, float 计算阈值，选取最优划分特征
        max_depth, int 每棵子树的最大层数
        is_regression， bool 是否是回归问题
        '''
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.min_samples_split = min_samples_split
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        self.is_regression = is_regression

        self.trees = []
        for i in range(self.n_estimators):
            self.trees.append(DecisionTreeRegressor(min_impurity = self.min_impurity, max_depth = self.max_depth, min_samples_split = self.min_samples_split))
    
    def fit(self, X, y):
        '''
        预测

        X, numpy.array 样本数组
        y, numpy.array 类别数组、
        '''
        self.trees[0].fit(X, y) # 第一棵数去拟合数据，获取首个预测值
        y_pred = self.trees[0].predict(X)
        for i in range(1, self.n_estimators): # 不断拟合，让下一棵树去你和上一棵树的残差，即梯度，或者说是下一棵子树的导数
            if self.is_regression:
                gradient = - (y - y_pred)
            else:
                gradient = y - y_pred
            self.trees[i].fit(X, gradient)
            y_pred -= np.multiply(self.learning_rate, self.trees[i].predict(X)) # 学习率与预测值相乘，防止模型过拟合，对应公式中的系数 $\epsilon$
    
    def predict(self, X):
        '''
        预测

        X, numpy.array 测试数据集
        '''
        y_pred = self.trees[0].predict(X)
        for i in range(1, self.n_estimators):
            y_pred -= np.multiply(self.learning_rate, self.trees[i].predict(X))
        
        if not self.is_regression:
            y_pred = np.exp(y_pred) / np.expand_dims(np.sum(np.exp(y_pred), axis = 1), axis = 1)
            y_pred = np.argmax(y_pred, axis = 1)
        return y_pred

class GBDTRegressor(GBDT):
    '''
    GBDT回归树
    '''
    def __init__(self, n_estimators = 200, learning_rate = 0.5, min_samples_split = 2, min_impurity = 1e-7, max_depth = 4):
        '''
        n_estimators, int 树的数量
        learning_rate, float 梯度下降的学习率
        min_samples_split, int 内部节点需要的最小样本数
        min_impurity, float 计算阈值，选取最优划分特征
        max_depth, int 每棵子树的最大层数
        is_regression， bool 是否是回归问题
        '''
        super().__init__(n_estimators = n_estimators,
                            learning_rate = learning_rate,
                            min_samples_split = min_samples_split,
                            min_impurity = min_impurity,
                            max_depth = max_depth,
                            is_regression = True)

class GBDTClassifier(GBDT):
    def __init__(self, n_estimators = 200, learning_rate = .5, min_samples_split = 2, min_impurity = 1e-7, max_depth = 2):
        '''
        n_estimators, int 树的数量
        learning_rate, float 梯度下降的学习率
        min_samples_split, int 内部节点需要的最小样本数
        min_impurity, float 计算阈值，选取最优划分特征
        max_depth, int 每棵子树的最大层数
        is_regression， bool 是否是回归问题
        '''
        super().__init__(n_estimators = n_estimators,
                            learning_rate = learning_rate,
                            min_samples_split = min_samples_split,
                            min_impurity = min_impurity,
                            max_depth = max_depth,
                            is_regression = False)

    def _one_hot(self, x, n_col = None):
        '''
        独热编码

        y, numpy.array 类别数据集
        n_col, int 类别数
        '''
        if not n_col:
            n_col = np.amax(x) + 1 # np.amax 一维数组中的最大值
        one_hot = np.zeros((x.shape[0], n_col))
        one_hot[np.arange(x.shape[0]), x] = 1
        return one_hot

    def fit(self, X, y):
        '''
        训练模型
        
        X, numpy.array 样本数组
        y, numpy.array 类别数组
        '''
        y = np.array([i[0] for i in y.tolist()])
        y = self._one_hot(y)
        super().fit(X, y)

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn import tree, preprocessing, datasets
    from sklearn.cross_validation import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, mean_squared_error

    # =========== GBDT Classification Tree ===========
    X, y = datasets.make_classification(n_samples = 100, n_features = 10, n_classes = 2) # 生成100个2分类的样本，特征数量为100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
    y_train = y_train.reshape(X_train.shape[0], 1)
    y_test = y_test.reshape(X_test.shape[0], 1)

    clf = GBDTClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy is: ", accuracy_score(y_test, y_pred))

    # =========== GBDT Regression Tree ===========
    X, y = datasets.make_regression(n_samples=100, n_features=1,n_targets=1, noise=2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
    y_train = y_train.reshape(X_train.shape[0], 1)
    y_test = y_test.reshape(X_test.shape[0], 1)

    clf = GBDTRegressor()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print("Mse is: ", mse)

    cmap = plt.get_cmap('viridis')
    test = plt.scatter(366 * X_test, y_test, color = cmap(0.5), s=10)
    pred = plt.scatter(366 * X_test, y_pred, color = 'red', s=10)
    plt.suptitle("GBDT Regression Tree")
    plt.title("Mse: %.2f" % mse, fontsize=10)
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend((test, pred), ("Test data", "Prediction"), loc='lower right')
    plt.show()