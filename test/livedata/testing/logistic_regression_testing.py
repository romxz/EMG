import numpy as np
import math
# 
# matrix = np.array([0,1,2,3,4])
def sigmoid(z):
    return 1/(1 + np.exp(-z));

print(sigmoid(np.mat([[0,1,3,2]])))

# theta = np.mat([[0.1],[0.1],[0.1],[0.1]])
# x_mat = np.mat([[1,2,3,4],[2,3,4,5],[3,4,5,6],[4,5,6,7],[5,6,7,8]])
# y_vec = np.mat([[0],[1],[0],[0],[1]])
# lamb = 0.1
# 
# def lrcost_function(theta, x_mat, y_vec, lamb):
#     m = len(y_vec)
#     hx = sigmoid(x_mat*theta)
#     print(hx)
#     J = np.multiply(-1,y_vec)* np.log(hx) 
#     K = np.transpose(1-y_vec) #* np.log(1-hx)
#     print(K)
#     J = np.divide(J,m)
#     # grad = (np.transpose(x_mat) * (hx-y_vec))/m
#     # last = np.size(theta,1)
#     # J += ((lamb)*(np.transpose(theta[2:last])*theta[2:last]))/(2*m)
#     # grad[2:last] += ((lamb)*(theta[2:last,1]))/m;
#     # return [J, grad]
# 
# lrcost_function(theta, x_mat, y_vec, lamb)



