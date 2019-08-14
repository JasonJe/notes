import numpy as np

def load_dataset(filepath):
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
    result = np.ones((data.shape[0], 1))
    if thresh_inequal == 'lt':
        result[data[:, feature] <= thresh] = -1.0
    else:
        result[data[:, feature] > thresh] = -1.0
    return result

import sys
def _find_best_classifier(data, labels, D):
    m, n = data.shape
    num_steps = 10.0
    best_classifier = {}
    best_classification_result = np.mat(np.zeros((m, 1)))
    min_error = np.inf

    for i in range(n):
        min_feature = data[:, i].min()
        max_feature = data[:, i].max()
        step = (max_feature - min_feature) / num_steps
        for j in range(-1, int(num_steps) + 1):
            for ineuqal in ['lt', 'gt']:
                thresh = (min_feature + float(j) * step)
                prediction = _weak_classifier(data, i, thresh, ineuqal)
                error = np.mat(np.ones((m, 1)))
                error[prediction == labels] = 0
                weighted_error = D.T * error

                if weighted_error < min_error:
                    min_error = weighted_error
                    best_classification_result = prediction.copy()
                    best_classifier['feature'] = i
                    best_classifier['thresh'] = thresh
                    best_classifier['ineq'] = ineuqal
    return best_classifier, min_error, best_classification_result

def adaboost_train(data, labels, max_iter = 40):
    weak_classifier = []
    m = data.shape[0]
    D = np.mat(np.ones((m ,1)) / m)
    alpha_classification_result = np.mat(np.zeros((m, 1)))

    for i in range(max_iter):
        best_classifier, error, classification_result = _find_best_classifier(data, labels, D)

        alpha = float(0.5 * np.log((1.0 - error) / max(error, 1e-16)))
        best_classifier['alpha'] = alpha

        weak_classifier.append(best_classifier)

        D = np.multiply(D, np.exp(np.multiply(-1 * alpha * labels, classification_result)))
        D = D / D.sum()

        alpha_classification_result += alpha * classification_result
        e_m = np.multiply(np.sign(alpha_classification_result) != labels, np.ones((m ,1)))

        error_rate = e_m.sum() / m
        if error_rate == 0.0:
            break
    return weak_classifier, alpha_classification_result

def predict(data, weak_classifier):
    m = data.shape[0]
    alpha_classification_result = np.mat(np.zeros((m, 1)))
    for classifier in weak_classifier:
        result = _weak_classifier(data, classifier['feature'], classifier['thresh'], classifier['ineq'])
        alpha_classification_result += classifier['alpha'] * result
    return np.sign(alpha_classification_result)

if __name__ == "__main__":
    data, labels = load_dataset('833_01.txt')
    weak_classifier, alpha_classification_result = adaboost_train(data, labels)
    prediction = predict(data, weak_classifier)
    error = np.mat(np.ones((data.shape[0], 1)))
    print('训练集的错误率:%.3f%%' % float(error[prediction != labels].sum() / data.shape[0] * 100))

    test_data, test_labels = load_dataset('833_02.txt')
    prediction = predict(test_data, weak_classifier)
    error = np.mat(np.ones((test_data.shape[0], 1)))
    print('测试集的错误率:%.3f%%' % float(error[prediction != test_labels].sum() / test_data.shape[0] * 100))
    
    