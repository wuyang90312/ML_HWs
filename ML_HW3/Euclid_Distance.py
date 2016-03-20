'''
Calculate the Squared Euclidean Distance b/t 
pairs of points by the vectorized tensorflow,
Without utilization of loop
'''

import numpy as np
import tensorflow as tf


class Euclid_Distance:
    def __init__(self, X, Y, K, B):
        self.X = X
        self.Y = Y
        self.K = K
        self.B = B
        
    def cal_Euclid_dis(self):
        x2 = self.cal_square(self.X, self.B,self.K)
        y2 = self.cal_square(self.Y, self.K, self.B)
        xy = self.cal_XY(self.X,self.Y)
        
        Euclid_dist = x2 + tf.transpose(y2) - 2*xy
        #print Euclid_dist.eval()
        return Euclid_dist
        '''
        The format of the return value(solution):
        |  D(x1, y1) D(x1, y2) ... D(x1, yK)   |
        |  D(x2, y1) D(x2, y2) ... D(x2, yK)   |
        |  ...          ...    ...    ...      |   
        |  D(xB, y1) D(xB, y2) ... D(xB, yK)   |
        '''
        

    def cal_square(self, X, size_X, size_Y):
        # square = tf.matmul(X, X, False, True)
        # sqr_2_diag = tf.pack([square[i,i] for i in range(size_X)])
        square = tf.square(X)
        sqr_2_diag = tf.reduce_sum(square, 1)
        diagonal = tf.diag(sqr_2_diag)
        diagonal = tf.reshape(diagonal, [size_X,size_X])
        ones = tf.ones(shape = [size_X, size_Y])
        result = tf.matmul(diagonal, ones, True)
        return result

    def cal_XY(self, X, Y):
        result = tf.matmul(X,Y, False, True)
        #print result.eval()
        return result


X= np.array([[1,2], [2,3], [3,4]], dtype = np.float32)
Y= np.array([[0,1], [1,2]], dtype = np.float32)

# with tf.Session():
#     ED = Euclid_Distance(X, Y, 2, 3)
#     print ED.cal_Euclid_dis().eval()


