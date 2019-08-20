import numpy as np
from collections import Counter

class DecisionTree(object):
    def __init__(self, impurity, leaf_value, min_impurity = 1e-7, max_features = None, max_depth = np.inf, min_samples_split = 2, loss = None):
        '''
        impurity, 树分割方法
        leaf_value, 树节点取值方法
        max_features：int, 需要考虑的特征数
        max_depth: int, 树的最大深度
        min_samples_split：int, 内部节点需要的最小样本数
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
    
    def _choose_best_feature(self, data_set, max_features, current_depth):
        best_feature = -1
        best_threshold = None
        largest_impurity = 0.0
        n_samples, n_features = data_set[:, :-1].shape

        if not max_features:
            features = n_features

        if n_samples >= self.min_samples_split and current_depth <= self.max_depth:
            for feature in range(features):
                thresholds = np.unique(data_set[:, feature])
                print("--------------")
                print(thresholds)

                for threshold in thresholds:
                    left, right = self._split(data_set, feature, threshold)

                    if (left.shape[0] > 0) and (right.shape[0] > 0):
                        split_impurity = self.impurity_func(data_set, left, right)

                        if split_impurity > largest_impurity:
                            largest_impurity = split_impurity
                            best_feature = feature
                            best_threshold = threshold
        return best_feature, best_threshold, largest_impurity
    
    def _create_tree(self, data_set, max_features, current_depth = 0):
        if data_set.shape[0] == 0:
            return
        if np.unique(data_set[:, -1].tolist()).shape[0] == 1:
            return data_set[0, -1]
        
        best_feature, best_threshold, largest_impurity = self._choose_best_feature(data_set, max_features, current_depth)

        tree = {}
        if largest_impurity > self.min_impurity:
            left, right = self._split(data_set, best_feature, best_threshold)
            tree['left'] = self._create_tree(left, max_features, current_depth + 1)
            tree['right'] = self._create_tree(right, max_features, current_depth + 1)
            tree['feature'] = best_feature
            tree['threshold'] = best_threshold
            return tree

        tree = {}
        value = self.leaf_value_func(data_set[:, -1])
        tree['value'] = value
        return tree
    
    def predict(self, test_data):
        test_data = np.array(test_data)
        prediction = []
        for data in test_data:
            prediction.append(self._predict_by_tree(self.tree, data))
        return prediction

class DecisionTreeClassifier(DecisionTree):
    def __init__(self, impurity, leaf_value):
        super().__init__(impurity, leaf_value)
        
    def _shannon_ent(self, data_set, left, right):
        shannon_ent = 0.0
        labels_counts = Counter(data_set[:, -1].tolist())
        for key in labels_counts:
            prob = float(labels_counts[key]) / data_set[:, :-1].shape[0]
            shannon_ent -= prob * np.log2(prob)
        return shannon_ent
    
    def _gini(self, data_set, left, right):
        gini = 1
        labels_counts = Counter(data_set[:, -1].tolist())
        for key in labels_counts:
            prob = float(labels_counts[key]) / data_set[:, :-1].shape[0]
            gini -= np.power(prob, 2)
        return gini
    
    def _vote(self, y):
        return Counter(y.tolist()).most_common(1)[0][0]
    
    def _split(self, data_set, feature, value):
        left = data_set[np.nonzero(data_set[:, feature] == value)[0], :]
        right = data_set[np.nonzero(data_set[:, feature] != value)[0], :]
        return left, right
    
    def _predict_by_tree(self, tree, test_data):
        if tree is None:
            return self.tree
        if not isinstance(tree, dict): 
            return tree
        if tree.get('value', None) is not None:
            return tree['value']
        feature = tree['feature']
        threshold = tree['threshold']
        if test_data[feature] == threshold:
            return self._predict_by_tree(tree['left'], test_data)
        else: 
            return self._predict_by_tree(tree['right'], test_data)
    
    def fit(self, X, y, max_features = None):
        if self.impurity == 'gain':
            self.impurity_func = self._shannon_ent
        else:
            self.impurity_func = self._gini
        self.leaf_value_func = self._vote
        data_set = np.concatenate((X, y.reshape(X.shape[0], 1)), axis=1)
        self.tree = self._create_tree(data_set, max_features)

class DecisionTreeRegressor(DecisionTree):
    def __init__(self):
        super().__init__(impurity = None, leaf_value = None)
    
    def _var(self, data_set, left, right):
        variance_reduction = np.var(data_set[:, -1]) - (left.shape[0] / data_set.shape[0] * np.var(left[:, -1]) + right.shape[0] / data_set.shape[0] * np.var(right[:, -1]))
        return np.sum(variance_reduction)
    
    def _mean(self, y):
        value = np.mean(y, axis=0)
        return value if len(value) > 1 else value[0]
    
    def _split(self, data_set, feature, value):
        left = data_set[np.nonzero(data_set[:, feature] >= value)[0], :]
        right = data_set[np.nonzero(data_set[:, feature] < value)[0], :]
        return left, right
    
    def _predict_by_tree(self, tree, test_data):
        if tree is None:
            return tree
        if not isinstance(tree, dict): 
            return tree
        if tree.get('value', None):
            return tree['value']
        feature = tree['feature']
        threshold = tree['threshold']
        if test_data[feature] >= threshold:
            return self._predict_by_tree(tree['left'], test_data)
        else: 
            return self._predict_by_tree(tree['right'], test_data)
    
    def fit(self, X, y, max_features = None):
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
    X, y = datasets.make_classification(n_samples = 100, n_features = 100, n_classes = 2) # 生成200个2分类的样本，特征数量为100

    # data = datasets.load_iris()
    # X = data.data
    # y = data.target

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
    # X_train, X_test, y_train, y_test = X[:10, :], X[:10, :], y[:10], y[:10]

    data = pd.read_csv('822_01.txt', ',', index_col='编号')
    for col in data.columns:
        data[col] = preprocessing.LabelEncoder().fit_transform(data[col])
    y = np.array(data['好瓜'])
    X = np.array(data[data.columns[:-1]])

    X_train, X_test, y_train, y_test = X, X, y, y

    impurity, leaf_value = 'gain', 'vote'
    dtc = DecisionTreeClassifier(impurity, leaf_value)
    dtc.fit(X_train, y_train)
    y_pred = dtc.predict(X_test)
    print("ACCURACY is: ", accuracy_score(y_test, y_pred))

    # =========== Regression Tree ===========
    # X, y = datasets.make_regression(n_samples=100, n_features=2,n_targets=1, noise=2)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    # dtr = DecisionTreeRegressor()
    # dtr.fit(X_train, y_train)

    # y_pred = dtr.predict(X_test)

    # print("MSE is: ", mean_squared_error(y_test, y_pred))

    # plt.plot(X_test, y_test,'o')
    # plt.plot(X_test, y_pred,'*')
    # plt.show()

