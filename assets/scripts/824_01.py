import random
import numpy as np
from matplotlib import pyplot as plt

def load_dataset(filepath):
    data_mat, label_mat= [], []
    f = open(filepath)
    for line in f.readlines():
        line_list = line.split(',')
        data_mat.append([float(line_list[0]), float(line_list[1])])
        label_mat.append(float(line_list[2]))
    return data_mat, label_mat

def show_dataset(data_mat, label_mat):
    data_plus = []
    data_minus = []
    for i in range(len(data_mat)):
        if label_mat[i] > 0:
            data_plus.append(data_mat[i])
        else:
            data_minus.append(data_mat[i])
    data_plus_np = np.array(data_plus)
    data_minus_np = np.array(data_minus)
    plt.scatter(np.transpose(data_plus_np)[0], np.transpose(data_plus_np)[1])
    plt.scatter(np.transpose(data_minus_np)[0], np.transpose(data_minus_np)[1])
    plt.show()

def _get_w(data_mat, label_mat, alphas):
    X = np.mat(data_mat)
    label_mat = np.mat(label_mat).transpose()
    m,n = np.shape(X)
    w = np.zeros((n,1))
    for i in range(m):
        w += np.multiply(alphas[i] * label_mat[i], X[i, :].T)
    return w

def show_classifer(data_mat, label_mat, b, alphas):
    w = _get_w(data_mat, label_mat, alphas)
    data_plus = []
    data_minus = []
    for i in range(len(data_mat)):
        if label_mat[i] > 0:
            data_plus.append(data_mat[i])
        else:
            data_minus.append(data_mat[i])
    data_plus_np = np.array(data_plus)
    data_minus_np = np.array(data_minus)
    plt.scatter(np.transpose(data_plus_np)[0], np.transpose(data_plus_np)[1], s=30, alpha=0.7)
    plt.scatter(np.transpose(data_minus_np)[0], np.transpose(data_minus_np)[1], s=30, alpha=0.7)
    x1 = max(data_mat)[0]
    x2 = min(data_mat)[0]
    a1, a2 = w
    b = float(b)
    a1 = float(a1[0])
    a2 = float(a2[0])
    y1, y2 = (-b - a1*x1)/a2, (- b - a1*x2)/a2
    plt.plot([x1, x2], [y1, y2])
    for i, alpha in enumerate(alphas):
        if alpha > 0:
            x, y = data_mat[i]
            plt.scatter([x], [y], s=150, c='none', alpha=0.7, linewidth=1.5, edgecolor='red')
    plt.show()

def _calc_Ek(data_mat, label_mat, alphas, b, k):
    # return float(np.multiply(alphas, label_mat).T * (data_mat[:,] * data_mat[k, :].T)) + b - float(label_mat[k])
    return float(np.multiply(alphas, label_mat).T * data_mat[:, k] + b) - float(label_mat[k])

def _update_Ek(data_mat, label_mat, alphas, b, error_cache, k):
    Ek = _calc_Ek(data_mat, label_mat, alphas, b, k)
    error_cache[k] = [1, Ek]
    return error_cache

def _select_rand_j(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j

def _select_j(data_mat, label_mat, alphas, b, error_cache, m, i, Ei):
    max_k = -1
    max_delta_E = 0
    Ej = 0 
    error_cache[i] = [1, Ei]
    valid_error_cache_list = np.nonzero(error_cache[:, 0].A)[0]
    if (len(valid_error_cache_list)) > 1:
        for k in valid_error_cache_list:
            if k == i:
                continue
            Ek = _calc_Ek(data_mat, label_mat, alphas, b, k)
            delta_E = abs(Ei - Ek)
            if (delta_E > max_delta_E):
                max_k = k
                max_delta_E = delta_E
                Ej = Ek
        return max_k, Ej
    else:
        j = _select_rand_j(i, m)
        Ej = _calc_Ek(data_mat, label_mat, alphas, b, j)
    return j, Ej

def _clip_alpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def _smo_iter(data_mat, label_mat, alphas, b, error_cache, C, toler, m, n, K, i):
    Ei = _calc_Ek(K, label_mat, alphas, b, i)
            
    if ((label_mat[i] * Ei < - toler) and (alphas[i] < C)) or ((label_mat[i] * Ei > toler) and (alphas[i] > 0)):

        j, Ej = _select_j(K, label_mat, alphas, b, error_cache, m, i, Ei)

        alpha_old_i = alphas[i].copy()
        alpha_old_j = alphas[j].copy()

        if (label_mat[i] != label_mat[j]):
            L = max(0, alphas[j] - alphas[i])
            H = min(C, C + alphas[j] - alphas[i])
        else:
            L = max(0, alphas[j] + alphas[i] - C)
            H = min(C, alphas[j] + alphas[i])
        if L==H: return alphas, b, error_cache, 0
        
        # eta = 2.0 * data_mat[i,:] * data_mat[j,:].T - data_mat[i,:] * data_mat[i,:].T - data_mat[j,:] * data_mat[j,:].T
        eta = 2.0 * K[i, j] - K[i, i] - K[j, j]
        if eta >= 0: return alphas, b, error_cache, 0
        
        alphas[j] -= label_mat[j]*(Ei - Ej)/eta
        
        alphas[j] = _clip_alpha(alphas[j], H, L)
        error_cache = _update_Ek(K, label_mat, alphas, b, error_cache, j)
        if (abs(alphas[j] - alpha_old_j) < 0.00001): return alphas, b, error_cache, 0
        
        alphas[i] += label_mat[j] * label_mat[i] * (alpha_old_j - alphas[j])
        error_cache = _update_Ek(K, label_mat, alphas, b, error_cache, i)

        # b1 = b - Ei - label_mat[i] * (alphas[i] - alpha_old_i) * data_mat[i, :] * data_mat[i, :].T - label_mat[j] * (alphas[j] - alpha_old_j) * data_mat[i, :] * data_mat[j, :].T
        # b2 = b - Ej - label_mat[i] * (alphas[i] - alpha_old_i)*data_mat[i, :] * data_mat[j, :].T - label_mat[j] * (alphas[j] - alpha_old_j) * data_mat[j, :] * data_mat[j, :].T

        b1 = b - Ei - label_mat[i] * (alphas[i] - alpha_old_i) * K[i, i] - label_mat[j] * (alphas[j] - alpha_old_j) * K[i, j] 
        b2 = b - Ej - label_mat[i] * (alphas[i] - alpha_old_i)* K[i, j] - label_mat[j] * (alphas[j] - alpha_old_j) * K[j, j]

        if (0 < alphas[i]) and (C > alphas[i]):
            b = b1
        elif (0 < alphas[j]) and (C > alphas[j]):
            b = b2
        else:
            b = (b1 + b2)/2.0
        return alphas, b, error_cache, 1
    else:
        return alphas, b, error_cache, 0

def _kernel_map(X, A, **params):
    m, n = np.shape(X)
    K = np.mat(np.zeros((m, 1)))

    if not params['sigma']:
        params['sigma'] = 1 / m
        
    if params['kernel'] == 'linear':
        K = X * A.T
    elif params['kernel'] == 'rbf':
        for j in range(m):
            delta_row = X[j, :] - A
            K[j] = delta_row * delta_row.T
        K = np.exp(K/(-1 * params['sigma'] ** 2)) 
    elif params['kernel'] == 'laplace':
        for j in range(m):
            delta_row = X[j, :] - A
            K[j] = delta_row * delta_row.T
            K[j] = np.sqrt(K[j])
        K = np.exp(- K/params['sigma'])     
    elif params['kernel'] == 'poly':
        K = X * A.T
        for j in range(m):
            K[j] = K[j] ** params['degree']
    elif params['kernel'] == 'sigmoid':
        K = X * A.T
        for j in range(m):
            K[j] = np.tanh(params['sigma'] * K[j] + params['theta']) 
    else:
        raise NameError('核函数无法识别')
    return K

def svm(data_mat, label_mat, C = 1, toler = 0.01, max_iter = 1000, kernel = 'rbf', sigma = None, degree = 3, theta = 0.2):
    data_mat = np.mat(data_mat)
    label_mat = np.mat(label_mat).transpose()
    b = 0
    m, n = np.shape(data_mat)
    alphas = np.mat(np.zeros((m, 1)))
    error_cache = np.mat(np.zeros((m,2)))

    K = np.mat(np.zeros((m, m)))
    for i in range(m):
        K[:, i] = _kernel_map(data_mat, data_mat[i,:], kernel = kernel, sigma = sigma, degree = degree, theta = theta)

    iter_num = 0
    alpha_pairs_changed = 0
    entire_set = True
  
    while (iter_num < max_iter) and ((alpha_pairs_changed > 0) or entire_set): # 遍历整个数据集都alpha也没有更新或者超过最大迭代次数,则退出循环
        alpha_pairs_changed = 0
        if entire_set:
            for i in range(m):
                alphas, b, error_cache, is_alpha_pairs_changed = _smo_iter(data_mat, label_mat, alphas, b, error_cache, C, toler, m, n, K,i)
                alpha_pairs_changed += is_alpha_pairs_changed
                print("全样本遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter_num, i, alpha_pairs_changed))
            iter_num += 1
        else:
            non_bound_Is = np.nonzero((alphas.A > 0) * (alphas.A < C))[0]
            for i in non_bound_Is:
                alphas, b, error_cache, is_alpha_pairs_changed = _smo_iter(data_mat, label_mat, alphas, b, error_cache, C, toler, m, n, K, i)
                alpha_pairs_changed += is_alpha_pairs_changed
                print("非边界遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter_num, i, alpha_pairs_changed))
            iter_num += 1
        
        if entire_set:
            entire_set = False
        elif (alpha_pairs_changed == 0):
            entire_set = True 
        print("迭代次数: %d" % iter_num)
    error_count = predict(data_mat, label_mat, b, alphas, kernel = kernel, sigma = sigma, degree = degree, theta = theta)
    print("训练集错误率: %.2f%%" % (error_count * 100))
    return b, alphas

def predict(data_mat, label_mat, b, alphas, **params):
    support_vector_index = np.nonzero(alphas.A > 0)[0]
    support_vectors = data_mat[support_vector_index]
    label_support_vectors = label_mat[support_vector_index]
    
    m, n = np.shape(data_mat)
    error_count = 0
    for i in range(m):
        kernel_eval = _kernel_map(support_vectors, data_mat[i, :], **params)
        predict = kernel_eval.T * np.multiply(label_support_vectors, alphas[support_vector_index]) + b
        if np.sign(predict) != np.sign(label_mat[i]):
            error_count += 1
    return float(error_count) / m

if __name__ == "__main__":
    data_mat, label_mat = load_dataset('824_01.txt')
    b, alphas = svm(data_mat, label_mat, kernel = 'linear')
    show_classifer(data_mat, label_mat, b, alphas)

    ##########
    data_mat, label_mat = load_dataset('824_02.txt')
    b, alphas = svm(data_mat, label_mat, C = 200, toler = 0.0001, max_iter = 100)

    ##########
    data_mat, label_mat = load_dataset('824_03.txt')
    data_mat = np.mat(data_mat)
    label_mat = np.mat(label_mat).transpose()
    error_count = predict(data_mat, label_mat, b, alphas, kernel = 'rbf', sigma = None, degree = 3, theta = 0.2)
    print("测试集错误率: %.2f%%" % (error_count * 100))

