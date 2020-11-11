import numpy as np
import scipy
import matplotlib.pyplot as plt
from mkdata import mkdata
from plotdata import plotdata
from plotdata_log_reg import plotdata_log_reg
from perceptron import perceptron
from logistic import logistic


nRep = 1000 # number of replicates
nTrain = 10 # number of training data
nTest = 10000
avgIter = 0
E_train = 0
E_test = 0

##################### Part 3.1: try our perceptron model ###################
for i in range(nRep):
    X, y, w_f = mkdata(nTrain)
    w_g, iters = perceptron(X, y)
    # Compute training, testing error
    P, N = X.shape
    # training error
    predict_train = np.sign(np.matmul(w_g.T, np.vstack((np.ones((1, N)), X))))
    err_rate_train = np.sum(predict_train != y) / N
    E_train = E_train + err_rate_train / nRep
    # testing error
    # generate test data
    data_range = np.array([-1, 1])
    X_test = np.random.random((P, nTest)) * (data_range[1] - data_range[0]) + data_range[0]
    y_test = np.sign(np.matmul(w_f.T, np.vstack((np.ones((1, nTest)), X_test))))
    predict_test = np.sign(np.matmul(w_g.T, np.vstack((np.ones((1, nTest)), X_test))))
    err_rate_test = np.sum(predict_test != y_test) / nTest
    E_test = E_test + err_rate_test / nRep
    # Sum up number of iterations
    avgIter = avgIter + iters / nRep
print('Perceptron: ')
print('E_train is {}, E_test is {}'.format(E_train, E_test))
print('Average number of iterations is {}.'.format(avgIter))
plotdata(X, y, w_f, w_g, 'Pecertron')


##################### Part 3.2: try our logistic model ###################
nRep = 100 # number of replicates
nTrain = 100 # number of training data
nTest = 10000
avgIter = 0
E_train = 0
E_test = 0
for i in range(nRep):
    X, y, w_f = mkdata(nTrain)
    P, N = X.shape
    # change lables of y
    y = np.maximum(np.zeros((1, N)), y)
    w_g = logistic(X, y)

    # Compute training, testing error
    P, N = X.shape
    # training error
    predict_train = np.matmul(w_g.T, np.vstack((np.ones((1, N)), X)))
    for i in range(N):
        if predict_train[0][i] >= 0.5:
            predict_train[0][i] = 1
        else:
            predict_train[0][i] = 0
    err_rate_train = np.sum(predict_train != y) / N
    E_train = E_train + err_rate_train / nRep
    # testing error
    # generate test data
    data_range = np.array([-1, 1])
    X_test = np.random.random((P, nTest)) * (data_range[1] - data_range[0]) + data_range[0]
    y_test = np.sign(np.matmul(w_f.T, np.vstack((np.ones((1, nTest)), X_test))))
    y_test = np.maximum(np.zeros((1, nTest)), y_test)
    predict_test = np.matmul(w_g.T, np.vstack((np.ones((1, nTest)), X_test)))
    for i in range(nTest):
        if predict_test[0][i] >= 0.5:
            predict_test[0][i] = 1
        else:
            predict_test[0][i] = 0
    err_rate_test = np.sum(predict_test != y_test) / nTest
    E_test = E_test + err_rate_test / nRep
    # Sum up number of iterations
    avgIter = avgIter + iters / nRep

print('Logistic: ')
print('E_train is {}, E_test is {}'.format(E_train, E_test))
plotdata_log_reg(X, y, w_f, w_g, 'Logistic Regression')