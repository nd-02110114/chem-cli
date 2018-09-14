# -*- coding: <utf-8> -*-
"""Classical Linear Regression."""

import numpy as np
import time

# 仮装環境化で実行なので以下の２行を追加
import matplotlib as mpl
mpl.use('Svg')

from matplotlib import pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from copy import deepcopy

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


def plot_fig(trainX, trainY, testX, testY, name):
    """Making figure."""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(trainX, trainY, c="r")
    ax.plot(testX, testY)
    fig.savefig(name + ".png")


def sk_lr_ridge(trainX, trainY):
    """Linear regression by sklearn Ridge."""
    header("sklearn linear Ridge")
    timing = time.time()
    ridge = linear_model.Ridge(alpha=0.02, fit_intercept=True)
    ridge.fit(trainX, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", ridge.coef_)
    print("Intercept:", ridge.intercept_)


def sk_lr_lasso(trainX, trainY):
    """Linear regression by sklearn LASSO."""
    header("sklearn linear LASSO")
    timing = time.time()

    lasso = linear_model.Lasso(alpha=0.01, fit_intercept=True)
    lasso.fit(trainX, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", lasso.coef_)
    print("Intercept:", lasso.intercept_)


def sk_poly_classic(trainX, trainY, degree):
    """Polynomial regression by sk classical linear regression."""
    header("sklearn Poly-classical-linear")
    timing = time.time()
    trainXsave = trainX
    trainX = PolynomialFeatures(degree=degree).fit_transform(trainX)
    lr = linear_model.LinearRegression(fit_intercept=True)
    lr.fit(trainX, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", lr.coef_)
    print("Intercept:", lr.intercept_)

    testX = np.linspace(min(trainXsave), max(trainXsave), 500).reshape(-1, 1)
    testXsave = testX
    testX = PolynomialFeatures(degree=degree).fit_transform(testX)
    testY = lr.predict(testX)
    plot_fig(trainXsave, trainY, testXsave, testY, "sk_nr_classic")


def sk_poly_ridge(trainX, trainY, degree):
    """Polynomial regression by sk Ridge."""
    header("sklearn Poly-Ridge")
    timing = time.time()
    trainXsave = trainX
    trainX = PolynomialFeatures(degree=degree).fit_transform(trainX)
    ridge = linear_model.Ridge(alpha=0.02, fit_intercept=True)
    ridge.fit(trainX, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", ridge.coef_)
    print("Intercept:", ridge.intercept_)

    testX = np.linspace(min(trainXsave), max(trainXsave), 500).reshape(-1, 1)
    testXsave = testX
    testX = PolynomialFeatures(degree=degree).fit_transform(testX)
    testY = ridge.predict(testX)
    plot_fig(trainXsave, trainY, testXsave, testY, "sk_nr_ridge")


def sk_poly_lasso(trainX, trainY, degree):
    """Polynomial regression by sk LASSO."""
    header("sklearn Poly-LASSO")
    timing = time.time()
    trainXsave = trainX
    trainX = PolynomialFeatures(degree=degree).fit_transform(trainX)
    lasso = linear_model.Lasso(alpha=0.003, fit_intercept=True)
    lasso.fit(trainX, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", lasso.coef_)
    print("Intercept:", lasso.intercept_)

    testX = np.linspace(min(trainXsave), max(trainXsave), 500).reshape(-1, 1)
    testXsave = testX
    testX = PolynomialFeatures(degree=degree).fit_transform(testX)
    testY = lasso.predict(testX)
    plot_fig(trainXsave, trainY, testXsave, testY, "sk_nr_lasso")


def my_lr_ridge(trainX, trainY):
    """Original Ridge."""
    header("Original ridge")
    timing = time.time()

    X = np.insert(trainX, 0, 1, axis=1)
    lr = LinearRegression(alpha=0.02)  # scikit learnと同じ値を利用
    W = lr.cal_w_by_ridge(X, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", W[1:])
    print("Intercept:", W[0])


def my_lr_lasso(trainX, trainY):
    """Original LASSO."""
    header("Original lasso")
    timing = time.time()

    my_lasso = LinearRegression(alpha=0.01, epoch=1000)
    my_lasso.cal_w_by_lasso(trainX, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", my_lasso.lasso_coef_)
    print("Intercept:", my_lasso.lasso_intercept_)


def my_poly_classic(trainX, trainY):
    """Your own linear regression for multi variable."""
    header("My own linear regression for multi variable")
    timing = time.time()

    pr = PolynomialRegression(degree=10)  # scikit learnと同じ値を利用
    phi = pr.create_phi(trainX)
    w = pr.cal_w(phi, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", w[1:])
    print("Intercept:", w[0])


def my_poly_ridge(trainX, trainY):
    """Your own linear regression for multi variable."""
    header("My own linear regression for multi variable (in L2 regularization)")
    timing = time.time()

    pr = PolynomialRegression(alpha=0.02, degree=10)  # scikit learnと同じ値を利用
    phi = pr.create_phi(trainX)
    w = pr.cal_w_by_ridge(phi, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", w[1:])
    print("Intercept:", w[0])


def my_poly_lasso(trainX, trainY):
    """Your own linear regression for multi variable."""
    header("My own linear regression for multi variable (in L1 regularization)")
    timing = time.time()

    pr = PolynomialRegression(alpha=0.003, degree=10, epoch=1000) # scikit learnと同じ値を利用
    phi = pr.create_phi(trainX)
    pr.cal_w_by_lasso(phi, trainY)
    print("CPU time:", (time.time() - timing)*1000, "msecond")
    print("Coeff.:", pr.lasso_coef_)
    print("Intercept:", pr.lasso_intercept_)


class LinearRegression:
    def __init__(self, alpha=0, eta=0.0001, epoch=10000):
        self.alpha = alpha              # alpha
        self.eta = eta                  # learning_rate
        self.epoch = epoch              # epoch
        self.lasso_coef_ = None         # lasso coef
        self.lasso_intercept_ = None    # lasso intercept

    def cal_w_by_ridge(self, x, t):
        return np.dot(np.linalg.inv(np.dot(x.T, x) + self.alpha * np.eye(x.shape[1])), np.dot(x.T, t))

    def _soft_thresholding_operator(self, x, lambda_):
        if x > 0 and lambda_ < abs(x):
          return x - lambda_
        elif x < 0 and lambda_ < abs(x):
          return x + lambda_
        else:
          return 0

    def cal_w_by_lasso(self, X, y):
        # https://github.com/satopirka/Lasso/blob/master/lasso.py
        X = np.column_stack((np.ones(len(X)),X))

        beta = np.zeros(X.shape[1])
        beta[0] = np.sum(y - np.dot(X[:, 1:], beta[1:]))/(X.shape[0])
        
        for _ in range(self.epoch):
          for j in range(1, len(beta)):
            tmp_beta = deepcopy(beta)
            tmp_beta[j] = 0.0
            r_j = y - np.dot(X, tmp_beta)
            arg1 = np.dot(X[:, j], r_j)
            arg2 = self.alpha * X.shape[0]
            beta[j] = self._soft_thresholding_operator(arg1, arg2) / (X[:, j] ** 2).sum()
            beta[0] = np.sum(y - np.dot(X[:, 1:], beta[1:])) / (X.shape[0])

        self.lasso_intercept_ = beta[0]
        self.lasso_coef_ = beta[1:]

        return self

class PolynomialRegression(LinearRegression):
    def __init__(self, alpha=0, eta=0.0001, epoch=10000, degree=1):
        super().__init__(alpha, eta, epoch)
        self.degree = degree

    def create_phi(self, train_data):
        phi = lambda x: [x ** i for i in range(self.degree + 1)]
        return np.array([phi(i) for i in train_data]).reshape(len(train_data), -1)

    def cal_w(self, x, t):
        return np.dot(np.linalg.inv(np.dot(x.T, x)), np.dot(x.T, t))

if __name__ == '__main__':
    # Linear regression process
    trainX, trainY = loaddata("4_linear_regularize.csv")
    trainX = (trainX - trainX.mean(axis=0)) / trainX.std(axis=0)
    trainY = (trainY - trainY.mean(axis=0)) / trainY.std(axis=0)
    sk_lr_ridge(trainX, trainY)
    sk_lr_lasso(trainX, trainY)
    my_lr_ridge(trainX, trainY)
    my_lr_lasso(trainX, trainY)

    # Nonlinear regression process
    trainX, trainY = loaddata("4_nonlinear_1d.csv")
    trainX = (trainX - trainX.mean(axis=0)) / trainX.std(axis=0)
    trainY = (trainY - trainY.mean(axis=0)) / trainY.std(axis=0)
    sk_poly_classic(trainX, trainY, 10)
    sk_poly_ridge(trainX, trainY, 10)
    sk_poly_lasso(trainX, trainY, 10)

    my_poly_classic(trainX, trainY)
    my_poly_ridge(trainX, trainY)
    my_poly_lasso(trainX, trainY)
