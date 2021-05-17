import cv2 as cv
import numpy as np





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
二次插值部分begin
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#输入x数列，获得大X矩阵
def getX(x):
    n = x.size
    X = np.zeros([n,n])
    for i in range(n):
        X[i] = x**i
        pass
    return X.T

#输入x和与之对应的y，多项式拟合，返回系数数列a
def PnFitted(x,y):
    n = x.size
    X = getX(x)
    A = np.linalg.inv(X).dot(y)
    return A

#根据已有的x,y插值拟合输入量xin，选取二次插值
def Interpoly(xin,x,y):
    if xin in x:
        k = np.argwhere(x==xin)
        return y[k]
    elif xin < x[1]:
        xx = np.array([
            x[0],x[1],x[2]
        ])
        yy = np.array([
            y[0],y[1],y[2]
        ])
        a = PnFitted(xx,yy)
        return a[0] + a[1] * xin + a[2] * xin**2
    elif xin > x[-2]:
        xx = np.array([
            x[-1],x[-2],x[-3]
        ])
        yy = np.array([
            y[-1],y[-2],y[-3]
        ])
        a = PnFitted(xx,yy)
        return a[0] + a[1] * xin + a[2] * xin**2
    else:
        k=0
        while x[k]<xin:
            k+= 1
            pass
        xx = np.array([
            x[k-1],x[k],x[k+1]
        ])
        yy = np.array([
            y[k-1],y[k],y[k+1]
        ])
        a = PnFitted(xx,yy)
        return a[0] + a[1] * xin + a[2] * xin**2

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
二次插值部分end
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
图像处理begin
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#人工二值化，传入值为矩阵，以及上界点up（默认5），超出up置为0，否则置为1
def get_filter0(mat,up=5):
    M,N = np.shape(mat)
    filter0 = np.zeros([M,N])
    for j in range(M):
        for i in range(N):
            if mat[j][i] < up: #这里的5就为初始筛选值
                filter0[j][i] = 1 #有颜色的地方设置为1
                pass
            pass
        pass
    return filter0

#自动筛选原点，传入灰度矩阵，返回M0，N0，和Sum矩阵
def get0(mat):
    M,N = np.shape(mat)
    Sum=np.zeros([M , N])
    for j in range(1,M-1):
        for i in range(1,N-1):
            Sum[j][i] = 0
            Sum[j][i]+= mat[j-1].sum()
            Sum[j][i]+= mat[j].sum()
            Sum[j][i]+= mat[j+1].sum()
            Sum[j][i]+= mat.T[i-1].sum()
            Sum[j][i]+= mat.T[i].sum()
            Sum[j][i]+= mat.T[i+1].sum()
            pass
        pass
    pos = np.argmax(Sum)
    M0 = int(pos / N)
    N0 = pos-N*M0
    return M0 , N0 , Sum

#获取九宫格均值矩阵，传入矩阵，用以均值筛选
def get_mean(mat):
    M,N = np.shape(mat)
    mean = np.zeros([M , N])
    for j in range(1,M-1):
        for i in range(1,N-1):
            tmp = 0
            tmp = mat[j-1][i-1] + mat[j-1][i] + mat[j-1][i+1]\
                + mat[j][i-1] + mat[j][i] + mat[j][i+1]\
                    + mat[j+1][i-1] + mat[j+1][i] + mat[j+1][i+1]
            mean[j][i] = tmp / 9
            pass
        pass
    return mean

#均值过滤，输入矩阵与均值限制limit，一般limit不低于0.34，返回过滤一步后的矩阵
def mean_filter(mat,limit=0.34): #均值过滤函数
    mean = get_mean(mat)
    M,N = np.shape(mat)
    for j in range(1,M-1):
        for i in range(1,N-1):
            if mean[j][i] < limit:
                mean[j][i] = 0
                pass
            else:
                mean[j][i] = 1
                pass
            pass
        pass
    return mean

#提取点,将矩阵中所有的有效点位置坐标（i，j）提取并返回一个2*n的数组
def get_xiyj(mat):
    xi = []
    yj = []
    M , N = np.shape(mat)
    for j in range(M):
        for i in range(N):
            if mat[j][i] > 0:
                xi.append(i)
                yj.append(j)
                pass
            pass
        pass
    xi = np.array(xi)
    yj = np.array(yj)
    xiyj = np.c_[xi,yj]
    xiyj = xiyj.T
    return xiyj

#转换矩阵函数，给定ij位置以及对应的xy坐标，返回转换矩阵q和不动点xy0
def Trans(ij,xy):
    i1,j1,i2,j2,i3,j3 = ij
    x1,y1,x2,y2,x3,y3 = xy
    A=np.array([
        [i1,j1,1],
        [i2,j2,1],
        [i3,j3,1]
    ])
    invA = np.linalg.inv(A)
    q11,q21,x0 = invA.dot(np.array([x1,x2,x3]))
    q12,q22,y0 = invA.dot(np.array([y1,y2,y3]))
    q=np.array([
        [q11,q21],
        [q12,q22]
    ])
    xy0 = np.array([[x0],[y0]])
    return q , xy0
    pass 

# 单步元胞自动拣选机作用，输入行向量处理
def CAiter(x):
    a = np.zeros(x.size)
    for i in range(1,x.size-1):
        if x[i] == 1 and x[i-1] == 0 and x[i+1] == 0:
            a[i] = 1
            pass
        elif x[i] == 1 and x[i-1] == 1 and x[i+1] == 0:
            a[i] = 0
            a[i-1] = 1
            pass
        elif x[i] == 1 and x[i-1] == 0 and x[i+1] == 1:
            a[i] = 0
            a[i+1] = 1
            pass
        elif x[i]*x[i-1]*x[i+1] == 1:
            a[i] = 1
            pass
        else:
            a[i] = 0
            pass
        pass
    return a
    pass

#多步元胞自动拣选机作用，迭代到收敛解并返回
def CA(x):
    while x.sum()!= CAiter(x).sum():
        x = CAiter(x)
        pass
    return x
    pass

#对于矩阵整体行、列进行元胞自动机拣选作用，需要制定M0和N0避免对坐标轴作用
def CAfilter(mat,M0,N0):
    M,N = mat.shape
    mat0 = np.zeros([M,N])
    for j in range(M):
        if j!= M0:
            mat0[j] = CA(mat[j])
            pass
        pass
    for i in range(N):
        if i!= N0:
            mat0.T[i]= CA(mat.T[i])
            pass
        pass
    return mat0

#排序与去重
def sort2(x,y):
    N = x.size
    for i in range(N):
        for j in range(1,N-i):
            if x[j] < x[j-1]:
                x[j-1],x[j] = x[j],x[j-1]
                y[j-1],y[j] = y[j],y[j-1]
                pass
            else:
                pass
            pass
        pass
    pass

def dup2(x,y):
    xd = list()
    yd = list()
    N = x.size
    for i in range(N):
        item = x[i]
        if item in xd:
            continue
        else:
            tmp = list()
            for j in range(i,N):
                if item == x[j]:
                    tmp.append(y[j])
                    pass
                pass
            tmp = np.array(tmp)
            xd.append(item)
            yd.append(np.mean(tmp))
            pass
        pass
    xd = np.array(xd)
    yd = np.array(yd)
    return xd , yd
    pass

#图象类别
class Pic:
    def __init__(self,name,up=4,limit=0.34):
        self.name = name
        self.pic = cv.imread(name)
        self.gray = cv.cvtColor(self.pic,cv.COLOR_BGR2GRAY)
        self.mat = np.array(self.gray)
        self.M , self.N = np.shape(self.mat)
        self.filter0 = get_filter0(self.mat,up)
        self.M0 , self.N0 , self.Sum = get0(self.filter0)
        filter1 = CAfilter(self.filter0)
        filter1 = mean_filter(self.filter0,limit)
        self.filter1 = mean_filter(filter1,limit)
        self.filter2 = CAfilter(self.filter1,self.M0,self.N0)
        self.xiyj = get_xiyj(self.filter2)
        pass

#扫描图像类别
class OCR:
    
    def __init__(self,name,up=4,limit=0.34):
        self.name = name
        self.pic = cv.imread(name)
        self.gray = cv.cvtColor(self.pic,cv.COLOR_BGR2GRAY)
        self.mat = np.array(self.gray)
        self.M , self.N = np.shape(self.mat)
        self.filter0 = get_filter0(self.mat,up)
        self.M0 , self.N0 , self.Sum = get0(self.filter0)
        filter1 = CAfilter(self.filter0,self.M0,self.N0)
        filter1 = mean_filter(self.filter0,limit)
        self.filter1 = mean_filter(filter1,limit)
        self.filter2 = CAfilter(self.filter1,self.M0,self.N0)
        self.xiyj = get_xiyj(self.filter2)
        pass
    
    def set_p1(self,x1,y1):
        self.x1 = x1
        self.y1 = y1
        self.i1 = self.N0
        self.j1 = self.M0
        pass
    
    def set_p2(self,x2,y2,j2,i2):
        self.x2 = x2
        self.y2 = y2
        self.j2 = j2
        self.i2 = i2
        pass
    
    def set_p3(self,x3,y3,j3,i3):
        self.x3 = x3
        self.y3 = y3
        self.j3 = j3
        self.i3 = i3
        pass
    
    def process(self,xu=0,yu=0):
        self.tij = np.array([self.i1 , self.j1 , self.i2 , \
            self.j2 , self.i3 , self.j3])
        self.txy = np.array([self.x1 , self.y1 , self.x2 , \
            self.y2 , self.x3 , self.y3])
        self.q,self.xy0 = Trans(self.tij,self.txy)
        xy = self.q.dot(self.xiyj) + self.xy0
        self.xy_init = xy
        x = xy[0]
        y = xy[1]
        xx = []
        yy = []
        for k in range(np.shape(xy)[1]):
            if x[k] > xu and y[k] > yu:
                xx.append(x[k])
                yy.append(y[k])
                pass
            pass
        xx = np.array(xx)
        yy = np.array(yy)
        sort2(xx,yy)
        xx,yy = dup2(xx,yy)
        xxyy = np.c_[xx,yy]
        self.xy = xxyy.T
        pass

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
图像处理end
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''