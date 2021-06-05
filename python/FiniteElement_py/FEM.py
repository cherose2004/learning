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

    def getpartK(self , row , col):
        m = row.size
        n = col.size
        mat = np.zeros([m , n])
        for j in range(m):
            for i in range(n):
                mat[j][i] = self.K[ int(row[j]) ][ int(col[i]) ]
                pass
            pass
        return mat
        pass

    def modifyK(self , pNaN , uvNaN):
        n = pNaN.size
        m = uvNaN.size
        k11 = self.getpartK(uvNaN , pNaN)
        k12 = self.getpartK(uvNaN , uvNaN)
        k21 = self.getpartK(pNaN , pNaN)
        k22 = self.getpartK(pNaN , uvNaN)
        return k11 , k12 , k21 , k22
        pass


    def solve(self):
        
        #提取借点已知信息
        P = np.zeros([self.N , 2])
        UV = np.zeros([self.N , 2])
        for i in range(self.N):
            node = self.NodeList[i]
            P[i] = np.array([node.Px , node.Py])
            UV[i] = np.array([node.u , node.v])
            pass
        #重塑为1*2*N矩阵
        p = P.flatten()
        uv = UV.flatten()
        
        #提取NaN位置信息，知道哪些未知量需要被处理
        pNaN = list()
        uvNaN = list()
        for j in range(2*self.N):
            if np.isnan(p[j]) == True:
                pNaN.append(j)
                pass
            if np.isnan(uv[j]) == True:
                uvNaN.append(j)
                pass
            pass
        pNaN = np.array(pNaN) #存储了力向量未知量的位置，也即位移向量已知量的位置
        uvNaN = np.array(uvNaN) #存储了位移向量未知量的位置，也即力向量已知量的位置
        
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
        p1 = np.array(p1) #存储力已知量列向量
        p2 = np.array(p2) #存储力未知量列向量，NaN
        uv1 = np.array(uv1) #存储位移已知量列向量
        uv2 = np.array(uv2) #存储位移未知量列向量，NaN

        #矩阵分块
        k11 , k12 , k21 , k22 = self.modifyK(pNaN , uvNaN)

        #开始求解
        uv2 = np.linalg.inv(k12).dot(p1 - k11.dot(uv1))
        p2 = k21.dot(uv1) + k22.dot(uv2)
        t1 = 0
        t2 = 0
        for k in range(2*self.N):
            if np.isnan(p[k]) == True:
                p[k] = p2[t1]
                t1 += 1
                pass
            if np.isnan(uv[k]) == True:
                uv[k] = uv2[t2]
                t2 += 1
                pass
            pass
        #求解完毕，p与uv中已存储完毕整个力场与位移场

        #将p于uv写入各个节点
        for k in range(self.N):
            self.NodeList[k].setP(Px = p[2*k] , Py = p[2*k+1])
            self.NodeList[k].setUV(u = uv[2*k] , v = uv[2*k+1])
            pass
        print("successfully update node infomation")
        pass

    def info(self):
        print('Report : Information of Each Node')
        for i in range(20):
            print('*' , end = '*')
            pass
        print('\n\n')
        for k in range(self.N):
            for i in range(10):
                print('-' , end = '-')
                pass
            print('\n')
            node = self.NodeList[k]
            print('Node' + str(k+1) + ':\n')
            print('Externel Load : ')
            print('Horizontal Load Px = ' , node.Px)
            print('Vertical Load Py = ' , node.Py)
            print('\n')
            print('Displacement : ')
            print('Horizontal Displacement u = ' , node.u)
            print('Vertical Displacement v = ' , node.v)
            print('\n')
            pass
        pass

    pass