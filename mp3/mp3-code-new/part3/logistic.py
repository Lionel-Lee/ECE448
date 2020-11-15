import numpy as np

def logistic(X, y):
    '''
    LR Logistic Regression.

    INPUT:  X: training sample features, P-by-N matrix.
            y: training sample labels, 1-by-N row vector.

    OUTPUT: w: learned parameters, (P+1)-by-1 column vector.
    '''
    P, N = X.shape
    X=np.mat(X)
    w = np.zeros((P + 1, 1))
    # print(w)
    iters = 0
    # YOUR CODE HERE
    # begin answer
    # TODO
#print(X)
    while iters < 100:
        iters += 1
        # print(iters)
        # flag=0
        for i in range(N):
            x=X[:,i].transpose()
            x=np.c_[x, np.array([1])]
            result=np.dot(x,w)
            result=1/(1 + np.exp(-result))
            e = np.array((y[:,i] - result))
            # print(result)
            w += np.multiply(np.multiply(np.multiply((1/iters)*e, result), 1-result),x.transpose())   
    # end answer
    # print(w)
    temp = w[2]
    w = np.delete(w,2)
    w = np.r_[temp, w]
    w = np.array([[w[0]],[w[1]],[w[2]]])
    # print(w)
    
    return w
