import cv2 as cv
import numpy as np
import sqlite3 as sq




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
二次插值部分begin
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#给出x数列，生成大X矩阵
def getX(x):
    n = x.size
    X = np.zeros([n,n])
    for i in range(n):
        X[i]=x**i
        pass
    return X.T
    pass

#输入对应的一组 x,y ，根据其数据规模，返回对应的稀疏矩阵A
def PnFitted(x,y):
    n = x.size
    X = getX(x)
    A = np.linalg.inv(X).dot(y)
    return A
    pass

def Interpoly(xin,x,y):
    if xin in x:
        k = np.argwhere(x == xin)
        return y[k]
    elif xin < x[1]:
        xx = np.array([
            x[0],x[1],x[2]
        ])
        yy = np.array([
            y[0],y[1],y[2]
        ])
        a=PnFitted(xx,yy)
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
        k = 0
        while x[k] < xin:
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
    pass

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
二次插值部分end
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
图像处理begin
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#人工二值化，控制up为黑白分界点
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
    pass


#转换矩阵函数，给定ij位置以及对应的xy坐标，返回转换矩阵q和转换零点坐标xy0
def Trans(ij,xy):
    i1 , j1 , i2 , j2 , i3 , j3 = ij
    x1 , y1 , x2 , y2 , x3 , y3 = xy
    A=np.array([
        [i1 , j1 , 1],
        [i2 , j2 , 1],
        [i3 , j3 , 1]
    ])
    invA = np.linalg.inv(A)
    q11,q21,x0 = invA.dot(np.array([x1 , x2 , x3]))
    q12,q22,y0 = invA.dot(np.array([y1 , y2 , y3]))
    q=np.array([
        [q11 , q21],
        [q12 , q22]
    ])
    xy0 = np.array([[x0] , [y0]])
    return q , xy0
    pass


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
    return M0 , N0
    pass


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
    pass


'''''''''''''''''''''
两个过滤算法begin
'''''''''''''''''''''

#获取九宫格均值矩阵，传入矩阵，用以均值筛选
def get_mean(mat):
    M , N = np.shape(mat)
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
    pass

#均值过滤，输入矩阵与均值限制limit，一般limit不低于0.34，返回过滤一步后的矩阵
def mean_filter(mat,limit=0.34): #均值过滤函数
    mean = get_mean(mat)
    M , N = np.shape(mat)
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
    mat0 = mat0.T
    for i in range(N):
        if i!= N0:
            mat0[i]= CA(mat.T[i])
            pass
        pass
    return mat0.T

'''''''''''''''''''''
两个过滤算法end
'''''''''''''''''''''


#抠去坐标轴,以 xl 和 yl 为下分界点
def rid_axis(xy,xl=0,yl=0):
    x = []
    y = []
    m , n = xy.shape
    for i in range(n):
        if xy[0][i] > xl and xy[1][i] > yl:
            x.append(xy[0][i])
            y.append(xy[1][i])
            pass
        pass
    x = np.array(x)
    y = np.array(y)
    xy_ = np.c_[x,y]
    return xy_.T
    pass


#二维的冒泡排序
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

#去重操作
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


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
图像处理end
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
数据库交互begin
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#把x,y写入‘DbName’数据库的‘TableName’表格里
def writeSQL(x,y,DbName,TableName):
    con = sq.connect(DbName+'.db')
    cur = con.cursor()
    command = "create table " + TableName + \
        "(x double UNIQUE primary key,y double);"
    cur.execute(command)
    print('successfully create ' + DbName)
    print('successfully create ' + TableName)
    for i in range(x.size):
        data = str(x[i]) + ',' + str(y[i]) #生成行数据
        cur.execute(('INSERT INTO ' + TableName + ' VALUES (%s)')%data) #塞入 INSERT 行的值
        pass
    con.commit() #提交修改
    con.close()
    pass

#从‘DbName’数据库的‘TableName’表格里，读出x,y数据
def readSQL(DbName,TableName):
    con = sq.connect(DbName+'.db')
    cur = con.cursor()
    Data = cur.execute("Select x , y from " + TableName)
    x = []
    y = []
    for row in Data:
        x.append(row[0])
        y.append(row[1])
        pass
    x = np.array(x)
    y = np.array(y)
    con.close()
    return x , y
    pass
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
数据库交互end
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''