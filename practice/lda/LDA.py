# -*- coding: <utf-8> -*-
"""Classical Linear Regression."""

import numpy as np

# 仮装環境化で実行なので以下の２行を追加
import matplotlib as mpl
mpl.use('Svg')

from matplotlib import pyplot as plt
import time

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


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


def plot_fig_decision(trainX, vec, name):
    """Making figure with plots and decision surface."""
    trainX_0, trainX_1 = trainX[:50], trainX[50:]

    centre = (trainX_0.mean(axis=0) + trainX_1.mean(axis=0)) / 2
    x = np.array([min(trainX[:, 0]), max(trainX[:, 0])])
    grad = -vec[0] / vec[1]
    y = (x - centre[0]) * grad + centre[1]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(trainX_0[:, 0], trainX_0[:, 1], c="blue")
    ax.scatter(trainX_1[:, 0], trainX_1[:, 1], c="red")
    ax.plot(x, y, c="black")
    fig.savefig(name + ".png")


def plot_fig_projection(trainX, vec, name):
    """Making figure with plots and projection surface."""
    trainX_0, trainX_1 = trainX[:50], trainX[50:]

    centre = (trainX_0.mean(axis=0) + trainX_1.mean(axis=0)) / 2
    x = np.array([centre[0]-0.3, centre[0]+0.3])
    grad = vec[1] / vec[0]
    y = (x - centre[0]) * grad + centre[1]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(trainX_0[:, 0], trainX_0[:, 1], c="blue")
    ax.scatter(trainX_1[:, 0], trainX_1[:, 1], c="red")
    ax.plot(x, y, c="black", linestyle="dashed")
    fig.savefig(name + ".png")


def calcref(trainX, trainY):
    """Calclating reference by sklearn LDA."""
    header("sklearn LDA")
    timing = time.time()

    lda = LDA(n_components=2)
    lda.fit(trainX, trainY)

    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coefficient:")
    print(lda.coef_)
    plot_fig_decision(trainX, lda.coef_[0], "sklearn_lda_decision")
    plot_fig_projection(trainX, lda.coef_[0], "sklearn_lda_projection")


def my_LDA(trainX, trainY):
    """Calculating original LDA."""
    header("Original LDA")
    timing = time.time()
    #
    # Please code your LDA here

    # 1.fisher線形分別法による解法
    # まずクラスを分ける
    class_a = trainX[np.where(trainY==0)]
    # class_a = trainX[trainY==0] // これの方がスマート
    class_b = trainX[np.where(trainY==1)]
    # 平均を算出
    class_a_ave = np.mean(class_a, axis=0)
    class_b_ave = np.mean(class_b, axis=0)
    # 総クラス内分散を求める
    a = class_a - class_a_ave
    b = class_b - class_b_ave
    # 以下の方がスマート
    # a_var = np.conv(a, rowvar=0, bias=0)
    a_var = np.sum(np.array([np.dot(np.reshape(a[i], [2,1]), np.reshape(a[i], [2,1]).T) for i in range(a.shape[0])]), axis=0)
    b_var = np.sum(np.array([np.dot(np.reshape(b[i], [2,1]), np.reshape(b[i], [2,1]).T) for i in range(b.shape[0])]), axis=0)
    sw = a_var + b_var
    # coeffの算出
    my_fisher_coeff = np.dot(np.linalg.inv(sw), class_a_ave-class_b_ave)

    # 2.特異値分解による解法(あってないかもしれないです...)
    U, s, V = np.linalg.svd(trainX, full_matrices=True)
    # sに対する直行ベクトル(90度回転させる)
    my_svd_coeff = np.dot(np.array([[0, -1],[1, 0]]), s)

    # 3.scikit-learn (SVD以外)
    lda_eigen = LDA(solver='eigen', n_components=2)
    lda_eigen.fit(trainX, trainY)
    lda_lsqr = LDA(solver='lsqr', n_components=2)
    lda_lsqr.fit(trainX, trainY)

    coeff = my_fisher_coeff   # fisherの方がsklearnの値に近いのでこっちを採用
    #
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coefficient:")
    print("Fisher: ", my_fisher_coeff)
    print("SVD: ", my_svd_coeff)
    print("Sklearn Eigen: ", lda_eigen.coef_[0])
    print("Sklearn lsqr: ", lda_lsqr.coef_[0])
    plot_fig_decision(trainX, coeff, "my_lda_decision")
    plot_fig_projection(trainX, coeff, "my_lda_projection")


if __name__ == '__main__':
    trainX, trainY = loaddata("2_PCALDA_2d_2class_lin.csv")
    trainX = (trainX - trainX.mean(axis=0)) / trainX.std(axis=0)

    calcref(trainX, trainY)
    my_LDA(trainX, trainY)
