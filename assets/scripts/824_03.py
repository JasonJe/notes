import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def load_dataset(filepath):
    data_mat, label_mat = [], []
    f = open(filepath)
    for line in f.readlines():
        line_list = line.split(',')
        data_mat.append([float(line_list[0]), float(line_list[1])])
        label_mat.append(float(line_list[2]))
    return data_mat, label_mat

if __name__ == "__main__":
    data_mat, label_mat = load_dataset('824_02.txt')

    clf = SVC(C = 200, gamma = 1.3, tol = 0.0001, max_iter = 100)
    clf.fit(data_mat, label_mat)
    print(clf)
    y_train_pred = clf.predict(data_mat)
    print(accuracy_score(label_mat, y_train_pred, normalize = False))

    test_data_mat, test_label_mat = load_dataset('824_03.txt')
    y_pred = clf.predict(test_data_mat)
    print(accuracy_score(label_mat, y_pred, normalize = False))

    
    