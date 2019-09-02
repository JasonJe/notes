import numpy as np
from collections import Counter

from decision_tree import DecisionTree

class XGBoostRegressor(DecisionTree):
    def _split(self, y):
        '''
        划分数据集，获得左右子树
        '''
        col = int(np.shape(y)[1]/2)
        y, y_pred = y[:, :col], y[:, col:]
        return y, y_pred
    
    def _gain(self, y, y_pred):
        nominator = np.power((y - y_pred).sum(), 2) # gradient
        denonminator = np.ones_like(y).sum()  # loss
        return 0.5 * (nominator / denonminator)

    def _gain_by_taylor(self, y, y1, y2):
        y, y_pred = self._split(y)
        y1, y1_pred = self._split(y1)
        y2, y2_pred = self._split(y2)

        true_gain = self._gain(y1, y1_pred)
        false_gain = self._gain(y2, y2_pred)
        gain = self._gain(y, y_pred)
        return true_gain + false_gain - gain
    
    def _approximate_update(self, y):
        y, y_pred = self._split(y)
        gradient = np.sum((y - y_pred), axis = 0)
        hessian = np.sum(np.ones_like(y), axis = 0)
        update_approximation = gradient / hessian
        return update_approximation

    def fit(self, X, y):
        self.impurity_func = self._gain_by_taylor
        self.leaf_value_func = self._approximate_update
        super().fit(X, y)


class XGBoost(object):
    def __init__(self, n_estimators, learning_rate, min_samples_split, min_impurity, max_depth):
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
            update_pred = tree.pedict(X)
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
    pass
