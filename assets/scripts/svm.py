import random
import numpy as np
from matplotlib import pyplot as plt

class SVM(object):
    def __init__(self, data_mat, label_mat, C = 1, toler = 0.01, max_iter = 1000, kernel = 'rbf', sigma = None, degree = 3, theta = 0.2):
        self.data_mat = np.mat(data_mat)
        self.label_mat = np.mat(label_mat).transpose()

        self.C = C
        self.toler = toler
        self.max_iter = max_iter

        self.kernel = kernel
        self.sigma = sigma
        self.degree = degree
        self.theta = theta
        
        self.b = 0
        self.m, self.n = np.shape(data_mat)
        self.alphas = np.mat(np.zeros((self.m, 1)))
        self.error_cache = np.mat(np.zeros((self.m,2)))

        self.K = np.mat(np.zeros((self.m, self.m)))
        for i in range(self.m):
            self.K[:, i] = self._kernel_map(self.data_mat, self.data_mat[i,:])
    
    def _kernel_map(self, X, A):
        m, n = np.shape(X)
        K = np.mat(np.zeros((m, 1)))

        if not self.sigma:
            self.sigma = 1 / m
            
        if self.kernel == 'linear':
            K = X * A.T
        elif self.kernel == 'rbf':
            for j in range(m):
                delta_row = X[j, :] - A
                K[j] = delta_row * delta_row.T
            K = np.exp(K/(-1 * self.sigma ** 2)) 
        elif self.kernel == 'laplace':
            for j in range(m):
                delta_row = X[j, :] - A
                K[j] = delta_row * delta_row.T
                K[j] = np.sqrt(K[j])
            K = np.exp(- K/self.sigma)     
        elif self.kernel == 'poly':
            K = X * A.T
            for j in range(m):
                K[j] = K[j] ** self.degree
        elif self.kernel == 'sigmoid':
            K = X * A.T
            for j in range(m):
                K[j] = np.tanh(self.sigma * K[j] + self.theta) 
        else:
            raise NameError('核函数无法识别')
        return K
    
    def _calc_Ek(self, k):
        return float(np.multiply(self.alphas, self.label_mat).T * self.K[:, k] + self.b) - float(self.label_mat[k])
    
    def _update_Ek(self, k):
        Ek = self._calc_Ek(k)
        self.error_cache[k] = [1, Ek]
        return self.error_cache
    
    def _select_rand_j(self, i):
        j = i
        while (j == i):
            j = int(random.uniform(0, self.m))
        return j

    def _select_j(self, i, Ei):
        max_k = -1
        max_delta_E = 0
        Ej = 0 
        self.error_cache[i] = [1, Ei]
        valid_error_cache_list = np.nonzero(self.error_cache[:, 0].A)[0]
        if (len(valid_error_cache_list)) > 1:
            for k in valid_error_cache_list:
                if k == i:
                    continue
                Ek = self._calc_Ek(k)
                delta_E = abs(Ei - Ek)
                if (delta_E > max_delta_E):
                    max_k = k
                    max_delta_E = delta_E
                    Ej = Ek
            return max_k, Ej
        else:
            j = self._select_rand_j(i)
            Ej = self._calc_Ek(j)
        return j, Ej

    def _clip_alpha(self, aj, H, L):
        if aj > H:
            aj = H
        if L > aj:
            aj = L
        return aj

    def _smo_iter(self, i):
        Ei = self._calc_Ek(i)
                
        if ((self.label_mat[i] * Ei < - self.toler) and (self.alphas[i] < self.C)) or ((self.label_mat[i] * Ei > self.toler) and (self.alphas[i] > 0)):

            j, Ej = self._select_j(i, Ei)

            alpha_old_i = self.alphas[i].copy()
            alpha_old_j = self.alphas[j].copy()

            if (self.label_mat[i] != self.label_mat[j]):
                L = max(0, self.alphas[j] - self.alphas[i])
                H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
            else:
                L = max(0, self.alphas[j] + self.alphas[i] - self.C)
                H = min(self.C, self.alphas[j] + self.alphas[i])
            if L==H: return 0
            
            eta = 2.0 * self.K[i, j] - self.K[i, i] - self.K[j, j]
            if eta >= 0: return 0
            
            self.alphas[j] -= self.label_mat[j]*(Ei - Ej)/eta
            
            self.alphas[j] = self._clip_alpha(self.alphas[j], H, L)
            self.error_cache = self._update_Ek(j)
            if (abs(self.alphas[j] - alpha_old_j) < 0.00001): return 0
            
            self.alphas[i] += self.label_mat[j] * self.label_mat[i] * (alpha_old_j - self.alphas[j])
            self.error_cache = self._update_Ek(i)

            b1 = self.b - Ei - self.label_mat[i] * (self.alphas[i] - alpha_old_i) * self.K[i, i] - self.label_mat[j] * (self.alphas[j] - alpha_old_j) * self.K[i, j] 
            b2 = self.b - Ej - self.label_mat[i] * (self.alphas[i] - alpha_old_i)* self.K[i, j] - self.label_mat[j] * (self.alphas[j] - alpha_old_j) * self.K[j, j]

            if (0 < self.alphas[i]) and (self.C > self.alphas[i]):
                self.b = b1
            elif (0 < self.alphas[j]) and (self.C > self.alphas[j]):
                self.b = b2
            else:
                self.b = (b1 + b2)/2.0
            return 1
        else:
            return 0

    def train(self):
        iter_num = 0
        alpha_pairs_changed = 0
        entire_set = True

        while (iter_num < self.max_iter) and ((alpha_pairs_changed > 0) or entire_set): # 遍历整个数据集都alpha也没有更新或者超过最大迭代次数,则退出循环
            alpha_pairs_changed = 0
            if entire_set:
                for i in range(self.m):
                    is_alpha_pairs_changed = self._smo_iter(i)
                    alpha_pairs_changed += is_alpha_pairs_changed
                    print("全样本遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter_num, i, alpha_pairs_changed))
                iter_num += 1
            else:
                non_bound_Is = np.nonzero((self.alphas.A > 0) * (self.alphas.A < self.C))[0]
                for i in non_bound_Is:
                    is_alpha_pairs_changed = self._smo_iter(i)
                    alpha_pairs_changed += is_alpha_pairs_changed
                    print("非边界遍历:第%d次迭代 样本:%d, alpha优化次数:%d" % (iter_num, i, alpha_pairs_changed))
                iter_num += 1
            
            if entire_set:
                entire_set = False
            elif (alpha_pairs_changed == 0):
                entire_set = True
            print("迭代次数: %d" % iter_num)
    
    def eval(self):
        self._predict()

        error_count = 0
        for i in range(self.m):
            kernel_eval = self._kernel_map(self.support_vectors, self.data_mat[i, :])
            predict_ = kernel_eval.T * np.multiply(self.label_support_vectors, self.alphas[self.support_vector_index]) + self.b
            if np.sign(predict_) != np.sign(self.label_mat[i]):
                error_count += 1
        return float(error_count) /self.m
    
    def _predict(self):
        self.support_vector_index = np.nonzero(self.alphas.A > 0)[0]
        self.support_vectors = self.data_mat[self.support_vector_index]
        self.label_support_vectors = self.label_mat[self.support_vector_index]

    def predict(self, data_mat, label_mat):
        self._predict()

        m, n = np.shape(data_mat)
        error_count = 0
        for i in range(m):
            kernel_eval = self._kernel_map(self.support_vectors, data_mat[i, :])
            predict_ = kernel_eval.T * np.multiply(self.label_support_vectors, self.alphas[self.support_vector_index]) + self.b
            if np.sign(predict_) != np.sign(label_mat[i]):
                error_count += 1
        return float(error_count) / m

def load_dataset(filepath):
    data_mat, label_mat= [], []
    f = open(filepath)
    for line in f.readlines():
        line_list = line.split(',')
        data_mat.append([float(line_list[0]), float(line_list[1])])
        label_mat.append(float(line_list[2]))
    return data_mat, label_mat

if __name__ == "__main__":
    train_data, train_label = load_dataset('824_02.txt')
    svc = SVM(train_data, train_label, C = 200, toler = 0.0001, max_iter = 100, kernel = 'rbf', sigma = 1.3)
    svc.train()

    test_data, test_label = load_dataset('824_03.txt')
    data_mat = np.mat(test_data)
    label_mat = np.mat(test_label).transpose()
    
    error_count = svc.eval()
    print("训练集错误率: %.2f%%" % (error_count * 100))

    error_count = svc.predict(data_mat, label_mat)
    print("测试集错误率: %.2f%%" % (error_count * 100))