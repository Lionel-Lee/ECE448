import numpy as np

"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):

    #IMPLEMENT HERE
    #algorithm in the document
    N = len(x_train)
    n = 200
    num_batches = int(N/n)
    losses = epoch*[None]
    #no need to initialize weights and bias

    for epoch_i in range(epoch):
        print("starting epoch ", epoch_i+1)
        total_L = 0.0
        if shuffle:
            # tempx = np.random.permutation(x_train)      #deep copy, no change on the original data
            # tempy = np.random.permutation(y_train)

            shuffle_idx = np.random.choice(N, N, False)
            tempx = x_train[shuffle_idx]
            tempy = y_train[shuffle_idx]
        else:
            tempx = x_train.copy()      #deep copy, no change on the original data
            tempy = y_train.copy()
        
        for i in range(num_batches):
            x_test_batch = tempx[i*n : (i+1)*n]
            y_test_batch = tempy[i*n : (i+1)*n]
            total_L += four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test_batch, y_test_batch, num_classes, False)
        losses[epoch_i] = total_L

        print("total loss in epoch ", epoch_i+1, "is", total_L)

    return w1, w2, w3, w4, b1, b2, b3, b4, losses

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):

    class_rate_per_class = [0.0] * num_classes
    predicts = four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes, True)
    avg_class_rate = np.sum(y_test == predicts)/len(y_test)

    for c in range(num_classes):
        class_idxs = np.argwhere(y_test == c)
        total_num_c = len(class_idxs)
        num_corrects_c = np.sum(predicts[class_idxs] == c)
        class_rate_per_class[c] = num_corrects_c / total_num_c

    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes, test):

    #build the forward net work
    z1, cache_a1 = affine_forward(x_test, w1, b1)
    a1, cache_r1 = relu_forward(z1)
    z2, cache_a2 = affine_forward(a1, w2, b2)
    a2, cache_r2 = relu_forward(z2)
    z3, cache_a3 = affine_forward(a2, w2, b2)
    a3, cache_r3 = relu_forward(z3)
    F, cache_a4 = affine_forward(a3, w4, b4)
    if test:
        return np.argmax(F, axis=1)
    else:
        eta = 0.1
        #training, build the backward net work
        L, dF = cross_entropy(F, y_test)
        dA3, dW4, db4 = affine_backward(dF, cache_a4)
        dZ3 = relu_backward(dA3, cache_r3)
        dA2, dW3, db3 = affine_backward(dZ3, cache_a3)
        dZ2 = relu_backward(dA2, cache_r2)
        dA1, dW2, db2 = affine_backward(dZ2, cache_a2)
        dZ1 = relu_backward(dA1, cache_r1)
        dX, dW1, db1 = affine_backward(dZ1, cache_a1)
        w1 -= eta*dW1
        w2 -= eta*dW2
        w3 -= eta*dW3
        w4 -= eta*dW4
        b1 -= eta*db1
        b2 -= eta*db2
        b3 -= eta*db3
        b4 -= eta*db4
        return L

"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    return np.matmul(A,W)+b, (A, W)

def affine_backward(dZ, cache):
    dA = np.matmul(dZ, cache[1].T)
    dW = np.matmul(cache[0].T, dZ)
    db = np.sum(dZ, axis=0)
    return dA, dW, db

def relu_forward(Z):
    temp = Z.copy()
    temp[temp < 0] = 0
    return temp, Z

def relu_backward(dA, cache):
    Z = cache
    dZ = dA.copy()
    dZ[np.where(Z<0)] = 0
    return dZ

def cross_entropy(F, y):
    n = len(F)
    exp_F = np.exp(F)
    sum_exp_F = np.sum(exp_F, axis=1)
    Fiyi = F[np.arange(n), y.astype(int)]
    log_sum_exp_F = np.log(sum_exp_F)
    L = -(1/n)*np.sum(Fiyi-log_sum_exp_F)
    one_hot_label = np.zeros(F.shape)
    one_hot_label[np.arange(n), y.astype(int)] = 1  #one hot
    exp_F_DIV_sum_exp_F = exp_F / sum_exp_F.reshape((-1, 1)) #reshape into one column
    dF = -(1/n)*(one_hot_label-exp_F_DIV_sum_exp_F)
    return L, dF
