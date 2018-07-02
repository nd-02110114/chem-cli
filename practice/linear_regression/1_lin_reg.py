# -*- coding: <utf-8> -*-
"""Classical Linear Regression."""

import numpy as np
import time

from sklearn import linear_model


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


def calcref(trainX, trainY):
    """Calclating reference by sklearn LinearRegression."""
    header("sklearn linear regression")
    timing = time.time()

    sklr = linear_model.LinearRegression(fit_intercept=True)
    sklr.fit(trainX, trainY)

    print("CPU time:", (time.time() - timing)*1000, "msec.")
    print("Coeff.:", sklr.coef_)
    print("Intercept:", sklr.intercept_)

def my_linear_regression(trainX, trainY):
    """Calculating original linear regression."""
    header("Original linear regression")
    timing = time.time()
    print("標準偏差：", np.sqrt(np.var(trainX)))
    print("平均", np.average(trainX))

    trainX_T = trainX.T
    W = (np.linalg.inv(trainX_T.dot(trainX)).dot(trainX_T)).dot(trainY)
    trainX_ave = np.average(trainX, axis=0)
    trainY_ave = np.average(trainY)
    intercept = trainY_ave - W.dot(trainX_ave)

    print("CPU time:", (time.time() - timing)*1000, "msec.")
    print("Coeff.:", W)
    print("Intercept:",  intercept)
    return (time.time() - timing)*1000

if __name__ == '__main__':
    file_name = "lin_reg_100.csv"
    trainX, trainY = loaddata(file_name)

    # メモ
    # 説明変数：Y
    # 目的変数：X
    calcref(trainX, trainY)
    my_linear_regression(trainX, trainY)

    # データの扱い (以下の性質を利用)
    # 全てのデータにAを加える => 平均：+A 分散：変化なし
    # データをA倍する　=> 平均：A倍　分散：Aの２乗倍

    # 平均を変える
    trainX_ave_change = trainX + 10
    print("=============================================")
    calcref(trainX_ave_change, trainY)
    my_linear_regression(trainX_ave_change, trainY)

    # 標準偏差のみを変える
    trainX_dispersion_change = trainX*2 - np.average(trainX)
    print("=============================================")
    calcref(trainX_dispersion_change, trainY)
    my_linear_regression(trainX_dispersion_change, trainY)

