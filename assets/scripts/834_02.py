import numpy as np
from collections import Counter

from decision_tree import DecisionTree

class XGBoostRegressor(DecisionTree):
    def __init__(self, impurity = None, leaf_value = None, min_impurity = 1e-7, max_features = None, max_depth = np.inf, min_samples_split = 2):
        super().__init__(impurity = impurity, leaf_value = leaf_value)

    def _divide(self, y):
        col = int(np.shape(y)[1]/2)
        y, y_pred = y[:, :col], y[:, col:]
        return y, y_pred
    
    def _gain(self, y, y_pred):
        nominator = np.power((y - y_pred).sum(), 2) # gradient
        denonminator = np.ones_like(y).sum()  # loss
        return 0.5 * (nominator / denonminator)

    def _gain_by_taylor(self, y, y1, y2):
        y, y_pred = self._divide(y)
        y1, y1_pred = self._divide(y1)
        y2, y2_pred = self._divide(y2)

        true_gain = self._gain(y1, y1_pred)
        false_gain = self._gain(y2, y2_pred)
        gain = self._gain(y, y_pred)
        return true_gain + false_gain - gain
    
    def _approximate_update(self, y):
        y, y_pred = self._divide(y)
        gradient = np.sum((y - y_pred), axis = 0)
        hessian = np.sum(np.ones_like(y), axis = 0)
        update_approximation = gradient / hessian
        return update_approximation

    def fit(self, X, y):
        self.impurity_func = self._gain_by_taylor
        self.leaf_value_func = self._approximate_update
        
        self.n_features = X.shape[1]
        data_set = np.concatenate((X, y), axis=1)
        self.tree = self._create_tree(data_set, max_features = None)

class XGBoost(object):
    def __init__(self, n_estimators = 200, learning_rate = 0.5, min_samples_split = 2, min_impurity = 1e-7, max_depth = 4):
        '''
        n_estimators, int 树的数量
        learning_rate, float 梯度下降的学习率
        min_samples_split, int 内部节点需要的最小样本数
        min_impurity, float 计算阈值，选取最优划分特征
        max_depth, int 每棵子树的最大层数
        '''
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.min_samples_split = min_samples_split
        self.min_impurity = min_impurity
        self.max_depth = max_depth
        
        self.trees = []
        for i in range(self.n_estimators):
            self.trees.append(XGBoostRegressor(min_impurity = self.min_impurity, max_depth = self.max_depth, min_samples_split = self.min_samples_split))
    
    def fit(self, X, y):
        '''
        预测

        X, numpy.array 样本数组
        y, numpy.array 类别数组、
        '''
        m = X.shape[0]
        y = np.reshape(y, (m, -1))
        y_pred = np.zeros(np.shape(y))
        for i in range(self.n_estimators): # 不断拟合，让下一棵树去你和上一棵树的残差，即梯度，或者说是下一棵子树的导数
            tree = self.trees[i]
            y_and_pred = np.concatenate((y, y_pred), axis = 1)
            tree.fit(X, y_and_pred)
            update_pred = tree.predict(X)
            update_pred = np.reshape(update_pred, (m, -1))
            y_pred += update_pred
    
    def predict(self, X):
        '''
        预测

        X, numpy.array 测试数据集
        '''
        y_pred = None
        m = X.shape[0]
        for tree in self.trees:
            update_pred = tree.predict(X)
            update_pred = np.reshape(update_pred, (m, -1))
            if y_pred is None:
                y_pred = np.zeros_like(update_pred)
            y_pred += update_pred
        return y_pred


if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn import tree, preprocessing, datasets
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score, mean_squared_error
    
    # =========== XGBoost ===========
    X, y = datasets.make_classification(n_samples = 100, n_features = 10, n_classes = 2) # 生成100个2分类的样本，特征数量为100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
    y_train = y_train.reshape(X_train.shape[0], 1)
    y_test = y_test.reshape(X_test.shape[0], 1)

    clf = XGBoost()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy is: ", accuracy_score(y_test, y_pred))

