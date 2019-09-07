import numpy as np
from collections import Counter

from decision_tree import DecisionTree

'''
XGBoost 的简单实现
'''

class XGBoostRegressor(DecisionTree):
    def __init__(self, impurity = None, leaf_value = None, min_impurity = 1e-7, max_features = None, max_depth = np.inf, min_samples_split = 2):
        super().__init__(impurity = impurity, leaf_value = leaf_value) # 继承自决策树

    def _divide(self, y):
        '''
        分割上次迭代预测值与 真实值，为后续服务

        y, numpy.array 真实值和预测值的数组
        '''
        col = int(np.shape(y)[1]/2)
        y, y_pred = y[:, :col], y[:, col:]
        return y, y_pred
    
    def _gain(self, y, y_pred):
        '''
        计算树结构的分数 Obj
        
        y, numpy.array 真实值类别数组
        y_pred, numpy.array 上次迭代预测值
        '''
        nominator = np.power((y - y_pred).sum(), 2)
        denonminator = np.ones_like(y).sum()  # numpy.ones_like() 返回一个跟输入形状和类型一致的数组
        return 0.5 * (nominator / denonminator)

    def _gain_by_taylor(self, y, y1, y2):
        '''
        计算收益 Gain

        y, numpy.array  需要进行计算的数据集
        y1, numpy.array 需要进行计算的左子树数据集
        y2, numpy.array 需要进行计算的右子树数据集
        '''
        y, y_pred = self._divide(y)
        y1, y1_pred = self._divide(y1)
        y2, y2_pred = self._divide(y2)

        true_gain = self._gain(y1, y1_pred) # 左子树
        false_gain = self._gain(y2, y2_pred) # 右子树
        gain = self._gain(y, y_pred)
        return true_gain + false_gain - gain
    
    def _approximate_update(self, y):
        '''
        计算近似概率
        
        y, numpy.array 类别数组
        '''
        y, y_pred = self._divide(y)
        gradient = np.sum((y - y_pred), axis = 0)
        hessian = np.sum(np.ones_like(y), axis = 0)
        update_approximation = gradient / hessian
        return update_approximation

    def fit(self, X, y):
        '''
        训练
        
        X, numpy.array 样本数组
        y, numpy.array 类别数组
        '''
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
        for i in range(self.n_estimators): # 进行 n_estimators 次迭代，生成 n_estimators 个决策树
            self.trees.append(XGBoostRegressor(min_impurity = self.min_impurity, max_depth = self.max_depth, min_samples_split = self.min_samples_split))
    
    def fit(self, X, y):
        '''
        训练，遍历 n_estimators 次

        X, numpy.array 样本数组
        y, numpy.array 类别数组
        '''
        m = X.shape[0]
        y = np.reshape(y, (m, -1))
        y_pred = np.zeros(np.shape(y))
        for i in range(self.n_estimators):
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

