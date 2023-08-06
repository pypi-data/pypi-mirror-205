# 僅適用於簡單的相機 (1. without skew parameter, 2. camera coordinate = world ccordinate )
# initial: 最初需要利用兩筆已知的座標來找出K，並找出K_inv
# mid: 當圖像經過網路做完分割後得到物件在圖像上的分割，利用圖像上資訊獲得現實中的X, Y, Z其中一者資訊 (這裡選擇X)。
# final: 將圖像上物件的座標乘上K_inv 得到一個向量b，b[0] 跟sec 得到的X 差Z 倍，相除得到Z後在整個向量乘Z 即可得到現實生活中的座標。

import numpy as np
import cv2

class initial:
    def __init__(self, dd_x1=[], dd_x2=[], ddd_x1=[], ddd_x2=[], K=[]):
       self.dd_x1 = dd_x1
       self.ddd_x1 = ddd_x1
       self.dd_x2 = dd_x2
       self.ddd_x2 = ddd_x2
       self.K = K
    
    def find_K(self):
        # [Z1x2, Z1y1, Z2x2] = [[X1, Z1, 0], [Y1, 0, Z1], [X2, Z2, 0]].dot([f, x0, y0])
        # b = Ax ===> A-1b = x
        A  = np.zeros((3, 3))
        A[0, 0] = self.ddd_x1[0]
        A[0, 1] = self.ddd_x1[2]
        A[1, 0] = self.ddd_x1[1]
        A[1, 2] = self.ddd_x1[2]
        A[2, 0] = self.ddd_x2[0]
        A[2, 1] = self.ddd_x2[2]
        A_inv = np.linalg.inv(A)
        x = np.array([self.ddd_x1[2] * self.dd_x1[0], self.ddd_x1[2] * self.dd_x1[1], self.ddd_x2[2] * self.dd_x2[0]])
        f, x0, y0 = A_inv.dot(x)
        K = np.zeros((3, 3))
        K[0, 0], K[1, 1], K[2, 2] = f, f, 1
        K[0, 2], K[1, 2] = x0, y0
        return(K)
    
    def K_inv(self):
        K_inv = np.linalg.inv(self.K)
        return(K_inv)
    


class final:
    def __init__(self, dd_x=[], X=0, K_inv=[]):
        self.dd_x = dd_x
        self.X = X
        self.K_inv = K_inv
    
    def dd2ddd(self):
        self.dd_x = np.insert(self.dd_x, 2, [1])
        b = self.K_inv.dot(self.dd_x)
        Z = self.X / b[0]
        ddd_x = Z * b
        return(ddd_x)
