# -*- coding: <utf-8> -*-
"""Classical Linear Regression."""

import numpy as np

# 仮装環境化で実行なので以下の２行を追加
import matplotlib as mpl
mpl.use('Svg')

from matplotlib import pyplot as plt
import time

from sklearn.cluster import KMeans


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


def plot_fig(trainX, result, name):
    """Making figure."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(trainX[result == 0, 0], trainX[result == 0, 1], c="r")
    ax.scatter(trainX[result == 1, 0], trainX[result == 1, 1], c="g")
    ax.scatter(trainX[result == 2, 0], trainX[result == 2, 1], c="b")
    fig.savefig(name + ".png")


def calcref(trainX):
    """Calclating reference by sklearn KMeans."""
    header("sklearn KMeans")
    timing = time.time()

    km = KMeans(n_clusters=3)
    km.fit(trainX)
    result = km.predict(trainX)
    cent = km.cluster_centers_

    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Center:")
    print(cent)
    print("Result:")
    print(result)
    plot_fig(trainX, result, "sklearn_kmeans")


def my_kmeans(trainX):
    """Calculating original kmeans."""
    header("Original kmeans")
    timing = time.time()

    # 自分の実装
    kmeans = MyKmeans(itertion=150)
    kmeans.fit(trainX)
    label, center = kmeans.result()
    result = label
    cent = center

    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Center:")
    print(cent)
    print("Result:")
    print(result)
    plot_fig(trainX, result, "my_kmeans")

class MyKmeans:

    def __init__(self, clusters=3, itertion=100):
        self.clusters = clusters
        self.iteration = itertion
        self.center = []
        self.label = []

    def __cal_label(self, x_col, center):
        return np.argmin(np.apply_along_axis(np.linalg.norm, 1, center - x_col))

    def __assign(self, x, center):
        return np.apply_along_axis(self.__cal_label, 1, x, center)

    def __update_center(self, x, label):
        center_0 = np.mean(x[label == 0], axis=0).tolist()
        center_1 = np.mean(x[label == 1], axis=0).tolist()
        center_2 = np.mean(x[label == 2], axis=0).tolist()
        return [center_0, center_1, center_2]

    def fit(self, x):
        # 各初期値
        label = np.zeros(x.shape[0])
        center = x[np.random.randint(0, x.shape[0], 3)]

        for i in range(self.iteration):
            label = self.__assign(x, center)
            center = self.__update_center(x, label)

        self.label = label
        self.center = center

    def result(self):
        return self.label, self.center


if __name__ == '__main__':
    trainX, trainY = loaddata("3_kmeans_2d_3class.csv")
    trainX = (trainX - trainX.mean(axis=0)) / trainX.std(axis=0)
    calcref(trainX)

    my_kmeans(trainX)
