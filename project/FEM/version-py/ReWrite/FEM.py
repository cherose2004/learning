# modified by bcynuaa 2021/9/29

import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt
import copy

NaN = np.nan

def GetPartK_Truss(E = 200e9 , A = 0.01 , l = 1):
    '''
    给出杆的局部刚度矩阵
    '''
    mat = np.array([
        [1 , -1],
        [-1 , 1]
    ])
    mat = E*A/l * mat
    return mat
    pass

def GetLambda_Truss(l1 , l2):
    '''
    获取方向矩阵
    '''
    mat = np.array([
        [l1 , l2 , 0 , 0],
        [0 , 0 , l1 , l2]
    ])
    return mat
    pass

def CutArray(a , pos):
    '''
    辅助用于求解的过程
    用于提取数组a中
    pos所列举的位置
    '''
    arr = np.zeros(pos.size)
    for i in range(arr.size):
        arr[i] = a[ pos[i] ]
        pass
    return arr
    pass

def CutMatrix(mat , row , col):
    '''
    辅助用于求解的过程
    用于提取矩阵K中
    row列举的行号
    col列举的列号
    '''
    M = row.size  #
    N = col.size
    cm = np.zeros([M , N])
    for j in range(M):
        for i in range(N):
            cm[j][i] = mat[ row[j] ][ col[i] ]
            pass
        pass
    return cm
    pass

def LinearSolve(K , x , y):
    '''
    用于求解：
    y= Kx的线性方程组
    '''
    if x.size != y.size:
        print("Error of the bounds")
        pass
    N = x.size
    '''
    用于提取NaN数据
    '''
    PosNum_x = list()
    PosNan_x = list()
    for i in range(N):
        if np.isnan(x[i]) == np.isnan(y[i]):
            print("Error of the bounds maybe at pos " + str(i))
            pass
        else:
            if np.isnan(x[i]) == True:
                PosNan_x.append(i)
                pass
            else:
                PosNum_x.append(i)
                pass
            pass
        pass
    PosNum_y = np.array(PosNan_x)
    PosNan_y = np.array(PosNum_x)
    PosNan_x = np.array(PosNan_x)
    PosNum_x = np.array(PosNum_x)
    '''
    用于分块矩阵求解方程
    '''
    x1 = CutArray(x , PosNum_x)
    x2 = CutArray(x , PosNan_x)
    y1 = CutArray(y , PosNum_y)
    y2 = CutArray(y , PosNan_y)
    mat1 = CutMatrix(K , PosNum_y , PosNum_x)
    mat2 = CutMatrix(K , PosNum_y , PosNan_x)
    mat3 = CutMatrix(K , PosNan_y , PosNum_x)
    mat4 = CutMatrix(K , PosNan_y , PosNan_x)
    x2 = np.linalg.inv(mat2).dot( y1 - mat1.dot(x1) )
    y2 = mat3.dot(x1) + mat4.dot(x2)
    '''
    将结果重新写入xn,yn数列
    '''
    xn = np.zeros(N)
    yn = np.zeros(N)
    for i in range(x1.size):
        xn[ int(PosNum_x[i]) ] = x1[i]
        pass
    for i in range(x2.size):
        xn[ int(PosNan_x[i]) ] = x2[i]
        pass
    for i in range(y1.size):
        yn[ int(PosNum_y[i]) ] = y1[i]
        pass
    for i in range(y2.size):
        yn[ int(PosNan_y[i]) ] = y2[i]
        pass
    return xn , yn
    pass


class Node:
    '''
    定义二维节点类、
    暂时用于二维桁架
    '''
    
    def __init__(self , x = 0 , y = 0 , Px = NaN , Py = NaN , u = NaN , v = NaN):
        '''
        初始化函数
        在二维平面(x,y)处的点
        可以给定约束
        包括力约束Px,Py
        和位移约束u,v
        '''
        self.x = x
        self.y = y
        self.setP(Px , Py)
        self.setuv(u , v)
        pass
    
    def setP(self , Px = NaN , Py = NaN):
        '''
        给定力约束
        默认为无约束
        '''
        self.Px = Px
        self.Py = Py
        pass
    
    def setuv(self , u = NaN , v = NaN):
        '''
        给定位移约束
        默认为无约束
        '''
        self.u = u
        self.v = v
        pass

    def set(self , Px = NaN , Py = NaN , u = NaN , v = NaN):
        '''
        给定广义约束
        默认为无约束
        '''
        self.Px = Px
        self.Py = Py
        self.u = u
        self.v = v
        pass

    pass


class SystemTruss:
    '''
    建立二维桁架系统
    用于求解二维桁架系统
    '''

    def __init__(self , nodelist):
        '''
        初始化函数，传入一个Node类列表，从而建立系统
        NodeList/NodeList0 : 存放着节点顺序表
        N : 为节点个数
        NodeConnection : 为连接矩阵，有向，暂时为全0列
        PartK : 字典类型，用以存放各种名称的局部刚度矩阵
        InfoConnection : 字典类型，用以存放某个连接的连接信息
        K : 组装的整体刚度矩阵，暂时全为0
        SpringList : 弹性元器件列表，存储着弹性元器件存放列表，暂时为空
        Report : 生成报告字符串
        '''
        self.NodeList0 = copy.deepcopy(nodelist)
        self.NodeList = copy.deepcopy(nodelist)
        self.N = len(nodelist)
        self.NodeConnection = np.zeros([self.N , self.N])
        self.PartK = dict()
        self.InfoConnection = dict()
        self.K = np.zeros([2*self.N , 2*self.N])
        self.SpringList = list()
        self.Report = "Reprort : Information of This Truss System\n\n"
        print("Successfully Build The Truss System!")
        pass

    def connect(self , j , i , E = 200e9 , A = 0.01):
        '''
        用于连接节点j和i
        更新连接矩阵NodeConnection信息
        并且在PartK中键值为'j,i'的更新连接信息
        '''
        j = j-1
        i = i-1
        self.NodeConnection[j][i] = 1
        node1 = self.NodeList0[j]
        node2 = self.NodeList[i]
        x = node2.x - node1.x
        y = node2.y - node1.y
        l = np.sqrt(x**2 + y**2)
        lam1 = x/l
        lam2 = y/l
        ke = GetPartK_Truss(E , A , l)
        lam = GetLambda_Truss(lam1 , lam2)
        k = (lam.T).dot(ke).dot(lam)
        self.PartK[str(j) + ',' + str(i)]
        info = [E , A , l , lam]
        self.InfoConnection[str(j) + ',' + str(i)] = info
        pass

    def __AddToK(self , j , i):
        '''
        在总体刚度矩阵K中
        加入PartK['j,i']这个矩阵
        传入j和i即可
        '''
        Kji = self.PartK[str(j) + ',' + str(i)]
        kjj = Kji[0:2 , 0:2]
        kii = Kji[2:4 , 2:4]
        kji = Kji[0:2 , 2:4]
        kij = Kji[2:4 , 0:2]
        self.K[2*j : 2*(j+1) , 2*j : 2*(j+1)] += kjj
        self.K[2*i : 2*(i+1) , 2*i : 2*(i+1)] += kii
        self.K[2*j : 2*(j+1) , 2*i : 2*(i+1)] += kji
        self.K[2*i : 2*(i+1) , 2*j : 2*(j+1)] += kij
        pass

    def generate(self):
        '''
        拼装总体刚度矩阵K
        '''
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] == 1:
                    self.__AddToK(j , i)
                    pass
                else:
                    continue
                pass
            pass
        print("Successfully Generate Matrix K!")
        pass