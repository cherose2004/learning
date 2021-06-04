import numpy as np
NaN = np.NaN

class Node:

    def __init__(self , x = 0 , y = 0 , Px = NaN , Py = NaN , u = NaN , v = NaN):
        self.x = x
        self.y = y
        self.setP(Px , Py)
        self.setUV(u , v)
        pass

    def setP(self , Px = NaN , Py = NaN):
        self.Px = Px
        self.Py = Py
        pass

    def setUV(self , u = NaN , v = NaN):
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
        print("successfully get matrix K")
        pass

    def setP(self , k , Px = NaN , Py = NaN):
        self.NodeList[k-1].setP(Px , Py)
        pass

    def setUV(self , k , u = NaN , v = NaN):
        self.NodeList[k-1].setUV(u , v)
        pass

    def getPart(self , x):
        m = x.size
        mat = np.zeros([m , m])
        for j in range(m):
            for i in range(m):
                tmp = self.K[ int(x[j]) ][ int(x[i]) ]
                mat[j][i] = tmp
                pass
            pass
        return mat

    def solve(self):
        #提取借点已知信息
        P = np.zeros([self.N , 2])
        UV = np.zeros([self.N , 2])
        for i in range(self.N):
            node = self.NodeList[i]
            P[i] = np.array([node.Px , node.Py])
            UV[i] = np.array([node.u , node.v])
            pass
        #重塑为2*N矩阵
        p = P.reshape(1 , 2*self.N)
        uv = P.reshape(1 , 2*self.N)
        #提取NaN位置信息，知道哪些未知量需要被处理
        pNaN = list()
        uvNaN = list()
        for j in range(2*self.N):
            if p[j] == NaN:
                pNaN.append(j)
                pass
            if uv[j] == NaN:
                uvNaN.append(j)
                pass
            pass
        pNaN = np.array(pNaN)
        uvNaN = np.array(uvNaN)
        #处理前分块求解量
        p1 = list()
        p2 = list()
        uv1 = list()
        uv2 = list()
        for j in range(2*self.N):
            if j in pNaN:
                p2.append(p[j])
                pass
            elif j not in pNaN:
                p1.append(p[j])
                pass
            if j in uvNaN:
                uv2.append(uv[j])
                pass
            elif j not in uvNaN:
                uv1.append(uv[j])
                pass
            pass
        p1 = np.array(p1)
        p2 = np.array(p2)
        uv1 = np.array(uv1)
        uv2 = np.array(uv2)
        #矩阵分块
        matp1 = self.getPart(uvNaN)
        matp2 = self.getPart(pNaN)
        matuv1 = self.getPart(pNaN)
        matuv2 = self.getPart(uvNaN)
        #开始求解


        pass

    pass