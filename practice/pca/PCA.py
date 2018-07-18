# -*- coding: <utf-8> -*-
"""Classical Linear Regression."""

import numpy as np

# 仮装環境化で実行なので以下の２行を追加
import matplotlib as mpl
mpl.use('Svg')

from matplotlib import pyplot as plt
import time

from sklearn import decomposition


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


def plot_fig(trainX, vec, name):
    """Making figure with plots and projection surface."""
    trainX_0, trainX_1 = trainX[:50], trainX[50:]

    centre = (trainX_0.mean(axis=0) + trainX_1.mean(axis=0)) / 2
    grad = vec[1] / vec[0]
    x = np.array([min(trainX[:, 0]), max(trainX[:, 0])])
    y = (x - centre[0]) * grad + centre[1]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(trainX_0[:, 0], trainX_0[:, 1], c="blue")
    ax.scatter(trainX_1[:, 0], trainX_1[:, 1], c="red")
    ax.plot(x, y, c="black", linestyle="dashed")
    fig.savefig(name + ".png")


def calcref(trainX):
    """Calclating reference by sklearn PCA."""
    header("sklearn PCA")
    timing = time.time()

    pca = decomposition.PCA(n_components=2)
    pca.fit(trainX)
    transformed = pca.transform(trainX)

    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Components:")
    print(pca.components_)
    print("Explained ratio:")
    print(pca.explained_variance_ratio_)
    print("Transformed data:")
    print(transformed[0:2])
    plot_fig(trainX, pca.components_[0], "sklearn_pca_projection")


def my_PCA(trainX):
    """Calculating original PCA."""
    header("Original PCA")
    timing = time.time()
    #
    # Please code your PCA here

    # np.convを使用する
    # w,v = np.linalg.eig(np.cov(trainX, rowvar=False))

    # np.convを使用しない
    # npは整数同士を割ると整数を返すので, floatを挟む
    w,v = np.linalg.eig(np.dot(trainX.T, trainX)/float(trainX.shape[0]-1))
    # 固有値の降順でindexを取得 
    w_index = np.argsort(w)[::-1]
    # 寄与率の計算
    explaned_ratio = w[w_index]/np.sum(w)
    # 固有ベクトルをindexを元にソート
    my_components = v[:, w_index]
    # 逆写像後のデータ
    trainX_inverse = np.dot(trainX, my_components)

    components = my_components[0]  # Please replace by your components
    #
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Components:")
    print(my_components)
    print("Explained ratio:")
    print(explaned_ratio)
    print("Transformed data:")
    print(trainX_inverse[0:2])
    plot_fig(trainX, components, "my_pca_projection")


if __name__ == '__main__':
    trainX, trainY = loaddata("2_PCALDA_2d_2class_lin.csv")
    trainX = (trainX - trainX.mean(axis=0))
    calcref(trainX)

    my_PCA(trainX)
