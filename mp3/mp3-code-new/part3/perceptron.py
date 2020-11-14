import numpy as np

def perceptron(X, y):
    '''
    PERCEPTRON Perceptron Learning Algorithm.

       INPUT:  X: training sample features, P-by-N matrix.
               y: training sample labels, 1-by-N row vector.

       OUTPUT: w:    learned perceptron parameters, (P+1)-by-1 column vector.
               iter: number of iterations

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
    while True:
        iters += 1
        flag=0
        for i in range(N):
            x=X[:,i].transpose()
            x=np.c_[x, np.array([1])]
            result=np.dot(x,w)
            result=np.sign(result)
            # print(result)
            if result != y[:,i]:
                w += np.multiply(((1/(iters))) * np.array(y[:, i]) , x.transpose())
                flag=1
        if flag==0:
            break      
    # end answer
    # print(w)
    temp = w[2]
    w = np.delete(w,2)
    w = np.r_[temp, w]
    # print(w)
    return w, iters