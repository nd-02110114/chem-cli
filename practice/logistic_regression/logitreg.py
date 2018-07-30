# -*- coding: <utf-8> -*-
"""Classical Linear Regression."""

import numpy as np
# 仮装環境化で実行なので以下の２行を追加
import matplotlib as mpl
mpl.use('Svg')

from matplotlib import pyplot as plt
import time
import math

from sklearn.linear_model import LogisticRegression


def loaddata(name):
    """Loading learning data."""
    data = np.loadtxt(name, delimiter=",")
    trainY = data[:, 0]
    trainX = data[:, 1:]
    return trainX, trainY


def header(name):
    """Printing header."""
    print("")
    print("##################")
    print(name)
    print("##################")


def plot_fig(trainX, vec, intercept, name):
    """Making figure with plots and projection surface."""
    trainX_0, trainX_1 = trainX[:50], trainX[50:]

    grad = vec[1] / vec[0]
    x = np.array([-0.3, 0.3])
    y = x * grad + intercept

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(trainX_0[:, 0], trainX_0[:, 1], c="blue")
    ax.scatter(trainX_1[:, 0], trainX_1[:, 1], c="red")
    ax.plot(x, y, c="black", linestyle="dashed")
    fig.savefig(name + ".png")


def calcref(trainX, trainY):
    """Calclating reference by sklearn logistic regression."""
    header("sklearn logistic regression")
    timing = time.time()

    lr = LogisticRegression(fit_intercept=True)
    lr.fit(trainX, trainY)
    result = lr.predict(trainX)
    poss = lr.predict_proba(trainX)

    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coefficient:")
    print(lr.coef_)
    print("intercept_")
    print(lr.intercept_)
    print("Decision")
    print(result)
    print("Possibility")
    print(poss[0])
    plot_fig(trainX, lr.coef_[0], lr.intercept_[0], "sklearn_logit_reg")


def my_logit_reg(trainX, trainY):
    """Calculating original logistic regression."""
    header("Original logistic regression")
    timing1 = time.time()

    # 勾配降下法
    gd_lr = MyLogisticRegression(eta=0.0001, epoch=30000)
    gd_lr.fitByGD(trainX, trainY)
    coeff, intercept = gd_lr.result()
    probability = gd_lr.probability(trainX, trainY)
    time1 = time.time()
    gd_lr.loss_plot('gd_')

    # ミニバッチ確率的勾配降下法
    timing2 = time.time()
    msgd_lr = MyLogisticRegression(epoch=32500, batch_size=10)
    msgd_lr.fitByMSGD(trainX, trainY)
    c, i = msgd_lr.result()
    p = msgd_lr.probability(trainX, trainY)
    time2 = time.time()
    msgd_lr.loss_plot('msgd_')

    print("\nGD")
    print("================================================")
    print("CPU time:", (time1 - timing1)*1000, "msecond")
    print("Coefficient:")
    print(coeff)
    print("intercept_")
    print(intercept)
    print("Possibility")
    print(probability)
    print("\nMSGD")
    print("================================================")
    print("CPU time:", (time2 - timing2)*1000, "msecond")
    print("Coefficient:")
    print(c)
    print("intercept_")
    print(i)
    print("Possibility")
    print(p)
    plot_fig(trainX, coeff, intercept, "my_logit_reg")

# コードが長くなる & 調整したいパラメータが多いためclassを作成した
class MyLogisticRegression:

    def __init__ (self, eta=0.01, epoch=10000, batch_size=0):
        self.eta = eta                  # learning_rate
        self.epoch = epoch              # epoch
        self.batch_size = batch_size    # batch_size
        self.w_list = []                # weight list
        self.loss_list = []             # loss function list

    def __shuffle(self, x, t):
        index = np.random.permutation(len(x))
        return x[index], t[index]

    def __predict(self, x, W):
        return 1 / (1 + np.exp(- np.dot(x, W)))

    def __loss(self, activate, t):
        t_reshape = t[:, np.newaxis]
        return - np.sum(t_reshape * np.log(activate) + (1 - t_reshape) * np.log(1 - activate))

    def __gradient(self, x, t, activate):
        return - np.dot(x.T, (t[:, np.newaxis] - activate))

    # x:input t:label
    def fitByGD(self, x, t):
        x = np.insert(x, 0, 1, axis=1)   # バイアス用に全ての行に１を加える
        W = np.ones((3, 1))              # 重みの初期値
        self.w_list = []
        self.loss_list = []
        self.w_list.append(W)

        # 勾配法で学習(全データを毎回計算)
        for i in range(self.epoch):
            activate = self.__predict(x, W)
            loss = self.__loss(activate, t)
            W -= self.eta * self.__gradient(x, t, activate)
            self.w_list.append(W)
            self.loss_list.append(loss)

    def fitByMSGD(self, x, t):
        x = np.insert(x, 0, 1, axis=1)   # バイアス用に全ての行に１を加える
        W = np.ones((3, 1))              # 重みの初期値
        self.w_list = []
        self.loss_list = []
        self.w_list.append(W)

        # ミニバッチ確率的勾配降下法で学習(ランダムで取り出したデータを毎回計算)
        # epoch回数をデータ数で割ってloop回数を算出
        for i in range(math.ceil(self.epoch / t.shape[0])):
            # データをシャッフル
            randx, randt = self.__shuffle(x, t)

            for j in range(math.ceil(x.shape[0] / self.batch_size)):
                # batchごとに, シャッフルのされたリストからデータをとりだす
                tmp_x, tmp_t = randx[j*self.batch_size:(j+1)*self.batch_size - 1], \
                                randt[j*self.batch_size:(j+1)*self.batch_size - 1]
                activate = self.__predict(tmp_x, W)
                loss = self.__loss(activate, tmp_t)
                W -= self.eta * self.__gradient(tmp_x, tmp_t, activate)
                self.w_list.append(W)
                self.loss_list.append(loss)

    # return coeff, intercept
    def result(self):
        w = self.w_list[-1].T[0]
        return w[1:3], w[0]

    # calculate probability
    def probability(self, x, t):
        x = np.insert(x, 0, 1, axis=1)
        w = self.w_list[-1]
        class_1, class_2 = x[t == 0], x[t == 1]
        p1 = np.sum(self.__predict(class_1, w)) / class_1.shape[0]
        p2 = np.sum(self.__predict(class_2, w)) / class_2.shape[0]
        return [p1, p2][::-1]

    def loss_plot(self, name=''):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(np.arange(len(self.loss_list)), self.loss_list)
        fig.savefig(name + "loss.png")



if __name__ == '__main__':
    trainX, trainY = loaddata("3_logitreg_2d_2class.csv")
    trainX = (trainX - trainX.mean(axis=0)) / trainX.std(axis=0)
    calcref(trainX, trainY)

    my_logit_reg(trainX, trainY)
