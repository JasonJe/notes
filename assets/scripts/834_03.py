import numpy    as np 
import pandas   as pd
import xgboost  as xgb
import lightgbm as lgb

from sklearn import datasets 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier


# 生成二分类使用的数据集
X, y = datasets.make_classification(n_samples = 1000, n_features = 10, n_classes = 2) # 生成100个2分类的样本，特征数量为100
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
y_train = y_train.reshape(X_train.shape[0], 1)
y_test = y_test.reshape(X_test.shape[0], 1)

###### GBDT 训练与测试，基于 sklearn
gbc = GradientBoostingClassifier() # 基于默认参数进行学习
'''
class sklearn.ensemble.GradientBoostingClassifier(
    loss='deviance', 
    learning_rate=0.1, 
    n_estimators=100, 
    subsample=1.0, 
    criterion='friedman_mse', 
    min_samples_split=2, 
    min_samples_leaf=1, 
    min_weight_fraction_leaf=0.0, 
    max_depth=3, 
    min_impurity_decrease=0.0, 
    min_impurity_split=None, 
    init=None, 
    random_state=None, 
    max_features=None, 
    verbose=0, 
    max_leaf_nodes=None, 
    warm_start=False, 
    presort='auto'
)
'''
gbc.fit(X_train,y_train)
gbc_score = gbc.score(X_test, y_test)
print("GBDT Accuracy is: ", gbc_score)

###### 原生实现 XGBoost
dtrain = xgb.DMatrix(X_train, y_train)
dtest  = xgb.DMatrix(X_test , y_test)

params = {
    'booster'         : 'gbtree',
    'objective'       : 'multi:softmax', # 多分类问题
    'num_class'       : 2,               # 类别数，与multi softmax并用
    'gamma'           : 0.1,             # 用于控制是否后剪枝的参数，越大越保守，一般0.1 0.2的样子
    'max_depth'       : 12,              # 构建树的深度，越大越容易过拟合
    'lambda'          : 2,               # 控制模型复杂度的权重值的L2 正则化项参数，参数越大，模型越不容易过拟合
    'subsample'       : 0.7,             # 随机采样训练样本
    'colsample_bytree': 0.1,               # 这个参数默认为1，是每个叶子里面h的和至少是多少，对于正负样本不均衡时的0-1分类而言，假设h在0.01附近，min_child_weight为1，意味着叶子节点中最少需要包含100个样本。这个参数非常影响结果，控制叶子节点中二阶导的和的最小值，该参数值越小，越容易过拟合
    'silent'          : 0,               # 设置成1 则没有运行信息输入，最好是设置成0
    'eta'             : 0.007,           # 如同学习率
    'seed'            : 1000,
    'nthread'         : 4,               # CPU线程数
    'eval_metric'     : 'mlogloss'       # 自定义测评函数
}
xgbc = xgb.train(
        params                = params,              # 训练中的参数关键字和对应的值
        dtrain                = dtrain,              # 训练的数据
        num_boost_round       = 10,                  # 指提升迭代的个数
        evals                 = [(dtrain, 'train')], # 对训练过程中进行评估列表中的元素
        obj                   = None,                # 自定义目的函数
        feval                 = None,                # 自定义评估函数
        maximize              = False,               # 是否对评估函数进行最大化
        early_stopping_rounds = None,                # 停止迭代的参数，假设为100，验证集的误差迭代到一定程度在100次内不能再继续降低，就停止迭代。
        evals_result          = None,                # 存储在 evals 中的元素的评估结果
        verbose_eval          = True,                # 如果为True，则对evals中元素的评估结果会输出在结果中；如果输入数字，假设为5，则每隔5个迭代输出一次。
        learning_rates        = None,                # 每一次提升的学习率的列表
        xgb_model             = None                 # 训练之前用于加载的xgb_model
)

y_pred = xgbc.predict(xgb.DMatrix(X_test))
print("XGBoost Accuracy is: ", accuracy_score(y_test, y_pred))

###### sklearn 接口实现 XGBoost
xgbc2 = XGBClassifier(
    learning_rate    = 0.007,           # 学习率
    n_estimators     = 10,              # 树的个数
    max_depth        = 12,              # 树的深度
    min_child_weight = 0.1,             # 叶子节点最小权重
    gamma            = 0.1,             # 惩罚项中叶子结点个数前的参数
    subsample        = 0.7,             # 随机选择70%样本建立决策树
    colsample_btree  = 0.1,             # 随机选择10%特征建立决策树
    objective        = 'multi:softmax', # 指定损失函数
    scale_pos_weight = 1,               # 解决样本个数不平衡的问题
    random_state     = 1000,            # 随机数
    num_class        = 2                # 类别数
)

xgbc2.fit(
    X_train,
    y_train,
    eval_set              = [(X_train, y_train)], # 对训练过程中进行评估列表中的元素
    eval_metric           = "mlogloss",           # 自定义测评函数
    early_stopping_rounds = 10,                   # 停止迭代的参数
    verbose               = True                  # 是否打印信息
)
y_pred = xgbc2.predict(X_test)
print("Sklearn XGBoost Accuracy is: ", accuracy_score(y_test, y_pred))


###### LightGBM 原生实现
lgb_train = lgb.Dataset(X_train, y_train.ravel())
lgb_eval  = lgb.Dataset(X_train, y_train.ravel(), reference = lgb_train)
params = {
    'task'            : 'train',
    'boosting_type'   : 'gbdt',                    # 设置提升类型
    'objective'       : 'binary',                  # 目标函数
    'metric'          : {'binary_logloss', 'auc'}, # 评估函数
    'num_leaves'      : 2,                         # 叶子节点数
    'max_depth'       : 12,                        # 树的深度
    'learning_rate'   : 0.007,                     # 学习速率
    'feature_fraction': 0.7,                       # 建树的特征选择比例
    'bagging_fraction': 0.1,                       # 建树的样本采样比例
    'verbose'         : 1                          # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
}
lgbc = lgb.train(
        params,
        lgb_train,
        num_boost_round       = 10,         # 树的个数，迭代次数
        valid_sets            = [lgb_eval], # 对训练过程中进行评估列表中的元素
        early_stopping_rounds = 5           # 停止迭代的参数
)
y_pred_c = lgbc.predict(X_test, num_iteration = lgbc.best_iteration)
y_pred = [1 if i > 0.5 else 0 for i in y_pred_c]
print("LightGBM Accuracy is: ", accuracy_score(y_test, y_pred))
