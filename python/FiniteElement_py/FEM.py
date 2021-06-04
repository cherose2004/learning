import numpy as np

class Node:

    def __init__(self , x = 0 , y = 0 , id = 0):
        self.x = x
        self.y = y
        self.id = id
        pass

    def setF(self , Fx = 0, Fy = 0):
        self.Fx = Fx
        self.Fy = Fy
        pass

    def setUV(self , u = 0 , v = 0):
        self.u = u
        self.v = v
        pass

    pass

class SysPole:
    def __init__(self , ls):
        self.NodeList = ls
        self.N = len(ls)
        self.NodeConnection = np.zeros([self.N , self.N])
        self.dictK = dict()
        self.K = np.zeros([2 * self.N , 2 * self.N])
        print("successfully build system!")
        pass

    def getK(self , E = 200e9 , A = 0.01 , l = 1):
        mat = np.array([
            [1 , -1],
            [-1 , 1]
        ])
        mat = E * A / l * mat
        return mat
        pass

    def connect(self , j , i , E = 200e9 , A = 0.01):
        self.NodeConnection[j-1][i-1] = 1
        node1 = self.NodeList[j-1]
        node2 = self.NodeList[i-1]
        x = node2.x - node1.x
        y = node2.y - node1.y
        l = np.sqrt(x**2 + y**2)
        lambda1 = x / l
        lambda2 = y / l
        dire = np.array([
            [lambda1 , lambda2 , 0 , 0],
            [0 , 0 , lambda1 , lambda2]
        ])
        k = self.getK(E , A , l)
        K = dire.T.dot( k ).dot( dire )
        self.dictK[str(j) + str(i)] = K
        pass

    def addK(self , j , i):
        Kji = self.dictK[str(j) + str(i)]
        kjj = Kji[0:2 , 0:2]
        kii = Kji[2:4 , 2:4]
        kji = Kji[0:2 , 2:4]
        kij = Kji[2:4 , 0:2]
        self.K[2*(j-1) : 2*j , 2*(j-1) : 2*j] += kjj
        self.K[2*(i-1) : 2*i , 2*(i-1) : 2*i] += kii
        self.K[2*(j-1) : 2*j , 2*(i-1) : 2*i] += kji
        self.K[2*(i-1) : 2*i , 2*(j-1) : 2*j] += kij
        pass

    def generate(self):
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] == 0:
                    continue
                else:
                    self.addK(j+1 , i+1)
                    pass
                pass
            pass
        pass

    pass