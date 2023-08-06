import numpy as np
# import cv_final

# A = np.array([[1, 2, 3],
#               [4, 5, 6], 
#               [7, 8, 9]])
# x1 = np.array([4, 6])
# x2 = np.array([12, 9])
# X1 = np.array([2, 2, 4])
# X2 = np.array([9, 6, 2])
# K = cv_final.initial(x1, x2, X1, X2)
# K = K.find_K()
# K_inv = cv_final.initial(K = K)
# K_inv = K_inv.K_inv()
# print(K, K_inv)

a = np.array([4, 6])
a = np.insert(a, 1, [1])
print(6*a)