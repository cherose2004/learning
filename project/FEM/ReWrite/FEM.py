# modified by bcynuaa 2021/10/03

import numpy as np
import matplotlib.pyplot as plt
#import xlrd
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


class Spring:
    '''
    定义一个弹簧约束类别
    包括：
    作用点标号：
    作用方向：'x','y','z'
    劲度系数K
    '''

    def __init__(self , ID = 0 , direction = 'x' , k = 1e5):
        self.ID = ID
        self.direction = direction
        self.k = k
        pass
    pass


class Sheet:
    '''
    定义一个板约束
    包括：
    i,j,l,m四点标号
    以及局部刚度矩阵ke
    '''
    
    def __init__(self , i , j , l , m , G , t , F , a , ke = np.zeros([8 , 8])):
        self.i = i
        self.j = j
        self.l = l
        self.m = m
        self.G = G
        self.t = t
        self.F = F
        self.a = a
        self.ke = ke
        pass

    def Setke(self , ke):
        '''
        设置局部刚度矩阵
        '''
        self.ke = ke
        pass

    def SetQ(self , q):
        '''
        设置剪流
        '''
        self.q = q
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
        self.SetP(Px , Py)
        self.SetUV(u , v)
        pass
    
    def SetP(self , Px = NaN , Py = NaN):
        '''
        给定力约束
        默认为无约束
        '''
        self.Px = Px
        self.Py = Py
        pass
    
    def SetUV(self , u = NaN , v = NaN):
        '''
        给定位移约束
        默认为无约束
        '''
        self.u = u
        self.v = v
        pass

    def SetBound(self , Px = NaN , Py = NaN , u = NaN , v = NaN):
        '''
        给定广义约束
        默认为无约束
        '''
        self.Px = Px
        self.Py = Py
        self.u = u
        self.v = v
        pass

    def Distance(self , node2):
        '''
        返回两节点距离（平面）
        '''
        lx = self.x - node2.x
        ly = self.y - node2.y
        return np.sqrt(lx**2 + ly**2)
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
        NodeConnection : 为连接矩阵，有向，暂时为全0
        InternalForce ： 内力矩阵，有向，暂时全为0
        PartK : 字典类型，用以存放各种名称的局部刚度矩阵
        InfoConnection : 字典类型，用以存放某个连接的连接信息
        K : 组装的整体刚度矩阵，暂时全为0
        SpringList : 弹性元器件列表，存储着弹性元器件存放列表，暂时为空
        SheetList : 薄板约束设置列表，存储着薄板约束信息的列表，暂时为空
        Report : 生成报告字符串
        '''
        self.NodeList0 = copy.deepcopy(nodelist)
        self.NodeList = copy.deepcopy(nodelist)
        self.N = len(nodelist)
        self.NodeConnection = np.zeros([self.N , self.N])
        self.InternalForce = np.zeros([self.N , self.N])
        self.PartK = dict()
        self.InfoConnection = dict()
        self.K = np.zeros([2*self.N , 2*self.N])
        self.SpringList = list()
        self.SheetList = list()
        self.Report = "Reprort : Information of This Truss System\n\n"
        print("Successfully Build The Truss System!")
        pass

    def Connect(self , j , i , E = 200e9 , A = 0.01):
        '''
        用于连接节点j和i
        更新连接矩阵NodeConnection信息
        并且在PartK中键值为'j,i'的更新连接信息
        '''
        j = j-1
        i = i-1
        self.NodeConnection[j][i] = 1
        node1 = self.NodeList[j]
        node2 = self.NodeList[i]
        x = node2.x - node1.x
        y = node2.y - node1.y
        l = node1.Distance(node2)
        lam1 = x/l
        lam2 = y/l
        ke = GetPartK_Truss(E , A , l)
        lam = GetLambda_Truss(lam1 , lam2)
        k = (lam.T).dot(ke).dot(lam)
        self.PartK[str(j) + ',' + str(i)] = k
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

    def SetSpring(self , j , direction = 'x' , k = 1e5):
        '''
        设置弹性约束，再j号位置
        direction方向
        设置劲度系数为k的约束
        '''
        j = j-1
        spr = Spring(j , direction , k)
        self.SpringList.append(spr)
        pass

    def SetSheet(self , i , j , l , m , G = 100e9 , t = 0.01):
        '''
        设定i,j,l,m四块板上的约束

        '''
        i , j , l , m = i-1 , j-1 , l-1 , m-1
        nodei , nodej , nodel , nodem = self.NodeList[i] , self.NodeList[j] , self.NodeList[l] , self.NodeList[m]
        xil = nodel.x - nodei.x
        yil = nodel.y - nodei.y
        xjm = nodem.x - nodej.x
        yjm = nodem.y - nodej.y
        F = np.abs(xil*yjm - xjm*yil)/2
        a = np.array([
            -xil , -yil , xjm , yjm , xil , yil , -xjm , -yjm
        ])
        a = np.matrix(a)
        ke = (a.T).dot(a) * G*t/F/4
        sheet = Sheet(i , j , l , m , G , t , F , a , ke)
        self.SheetList.append(sheet)
        pass

    def Generate(self):
        '''
        拼装总体刚度矩阵K
        先拼装桁架结构的部分
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
        '''
        再修正因弹性元器件存在
        而需要修正的约束条件
        '''
        for spr in self.SpringList:
            if spr.direction == 'x':
                self.NodeList[spr.ID].Px = 0
                self.NodeList[spr.ID].u = NaN
                self.K[2*spr.ID][2*spr.ID] += spr.k
                pass
            elif spr.direction == 'y':
                self.NodeList[spr.ID].Py = 0
                self.NodeList[spr.ID].v = NaN
                self.K[2*spr.ID+1][2*spr.ID+1] += spr.k
                pass
            else:
                print("Error of Spring Bound at Node : " + str(spr.ID))
                pass
            pass
        '''
        需要添加薄板约束
        更新总体刚度矩阵
        '''
        for sheet in self.SheetList:
            i = sheet.i
            j = sheet.j
            l = sheet.l
            m = sheet.m
            ke = sheet.ke
            ls = [i , j , l , m]
            for jj in range(4):
                for ii in range(4):
                    self.K[2*ls[jj] : 2*(ls[jj]+1) , 2*ls[ii] : 2*(ls[ii]+1)] += ke[2*jj : 2*(jj+1) , 2*ii : 2*(ii+1)]
                    pass
                pass
            pass
        print("Successfully Generate Matrix K!")
        pass

    def SetBound(self , j , Px = NaN , Py = NaN , u = NaN , v = NaN):
        '''
        设定全部约束
        '''
        j = j-1
        self.NodeList[j].SetBound(Px , Py , u , v)
        pass

    def SetP(self , j , Px = NaN , Py = NaN):
        '''
        设定力约束
        '''
        j = j-1
        self.NodeList[j].SetP(Px , Py)
        pass

    def SetUV(self , j , u = NaN , v = NaN):
        '''
        设定位移约束
        '''
        j = j-1
        self.NodeList[j].SetUV(u , v)
        pass

    def Solve(self):
        '''
        用于求解整个桁架结构
        使用分块矩阵求解
        更新信息至NodeList中的每一个节点
        生成内力矩阵InternalForce
        '''
        x0 = np.zeros(2*self.N)
        y0 = np.zeros(2*self.N)
        for j in range(self.N):
            x0[2*j] = self.NodeList[j].u
            x0[2*j+1] = self.NodeList[j].v
            y0[2*j] = self.NodeList[j].Px
            y0[2*j+1] = self.NodeList[j].Py
            pass
        xn , yn = LinearSolve(self.K , x0 , y0)
        '''
        将结果写入NodeList中的每个节点内
        '''
        for j in range(self.N):
            self.NodeList[j].u = xn[2*j]
            self.NodeList[j].v = xn[2*j+1]
            self.NodeList[j].Px = yn[2*j]
            self.NodeList[j].Py = yn[2*j+1]
            pass
        '''
        对弹性元器件部分进行修正
        '''
        for spr in self.SpringList:
            if spr.direction == 'x':
                self.NodeList[spr.ID].Px = -spr.k * self.NodeList[spr.ID].u
                pass
            elif spr.direction == 'y':
                self.NodeList[spr.ID].Py = -spr.k * self.NodeList[spr.ID].v
                pass
            else:
                print("Error of Spring Bound at Node : " + str(spr.ID))
                pass
            pass
        '''
        更新InternalForce内力矩阵
        '''
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] != 1:
                    continue
                else:
                    info = self.InfoConnection[str(j) + ',' + str(i)]
                    E = info[0]
                    A = info[1]
                    l = info[2]
                    lam = info[3]
                    nodej = self.NodeList[j]
                    nodei = self.NodeList[i]
                    delta = np.array([
                        nodej.u , nodej.v , nodei.u , nodei.v
                    ])
                    S = GetPartK_Truss(E , A , l).dot(lam).dot(delta)
                    self.InternalForce[j][i] = -S[0]
                    self.InternalForce[i][j] = S[1]
                    pass
                pass
            pass
        '''
        根据薄板受力理论
        重新更新内力矩阵
        '''
        for k in range(len(self.SheetList)):
            sheet = self.SheetList[k]
            i = sheet.i
            j = sheet.j
            l = sheet.l
            m = sheet.m
            nodei , nodej , nodel , nodem = self.NodeList[i] , self.NodeList[j] , self.NodeList[l] , self.NodeList[m]
            delta = np.array([
                nodei.u , nodei.v , nodej.u , nodej.v , nodel.u , nodel.v , nodem.u , nodem.v
            ])
            q = float(sheet.G*sheet.t/2/sheet.F * np.array(sheet.a).dot(delta))
            self.SheetList[k].SetQ(q)
            Lij = nodei.Distance(nodej)
            Ljl = nodej.Distance(nodel)
            Llm = nodel.Distance(nodem)
            Lmi = nodem.Distance(nodei)
            #修正ij
            self.InternalForce[i][j] += q/2 * Llm
            self.InternalForce[j][i] += -q/2 * Llm
            #修正jl
            self.InternalForce[j][l] += -q*Ljl/2
            self.InternalForce[l][j] += q*Ljl/2
            #修正lm
            self.InternalForce[l][m] += q/2 * Lij
            self.InternalForce[m][l] += -q/2 * Lij
            #修正mi
            self.InternalForce[m][i] += -q*Lmi/2
            self.InternalForce[i][m] += q*Lmi/2
            pass
        print("Successfully Solve the Truss System!")
        self.__GetReport()
        #self.__GetFigure()
        pass

    def __GetReport(self):
        '''
        用于书写报告至Report字符串
        '''
        for i in range(60):
            self.Report += '*'
            pass
        self.Report += '\n'
        '''
        self.Report += '\nConnection Matrix :\n' + str(self.NodeConnection)
        for i in range(60):
            self.Report += '*'
            pass
        self.Report += '\nInternal Force Matrix :\n' + str(self.InternalForce)
        for i in range(60):
            self.Report += '*'
            pass
        '''
        for sheet in self.SheetList:
            self.Report += 'q of '+ str(sheet.i+1) + ',' + str(sheet.j+1) + ',' + str(sheet.l+1) + ',' + str(sheet.m+1) + ':\n'
            self.Report += str(sheet.q) + ' N/m\n\n'
        for k in range(self.N):
            for i in range(60):
                self.Report += '-'
                pass
            self.Report += '\nNode' + str(k+1) + ' :\n Position :\n'
            self.Report += '(' + str(self.NodeList[k].x) + ',' + str(self.NodeList[k].y) + ')\n'
            self.Report += 'External Load :\nHorizontal Load Px = ' + str(self.NodeList[k].Px) + ' N\n'
            self.Report += 'Vertical Load Py = ' + str(self.NodeList[k].Py) + ' N\n'
            self.Report += 'Displacement :\nHorizontal Displacement u = ' + str(self.NodeList[k].u) + ' m\n'
            self.Report += 'Vertical Displacement v = ' + str(self.NodeList[k].v) + ' m\n'
            pass
        for i in range(60):
            self.Report += '*'
            pass
        pass

    def __GetFigure(self , size = 40 , ftsize = NaN , sizex = NaN , sizey = NaN , PointSize = NaN , LineSize = NaN):
        '''
        绘制图片
        有各种参数可选择
        '''
        if np.isnan(sizex) == True:
            sizex = size
            pass
        if np.isnan(sizey) == True:
            sizey = size
            pass
        if np.isnan(PointSize) == True:
            PointSize = 40*size
            pass
        if np.isnan(ftsize) == True:
            ftsize = 1.3*size
            pass
        if np.isnan(LineSize) == True:
            LineSize = size/3
        '''开始绘图'''
        pic = plt.figure(facecolor = 'white' , figsize = (sizex , sizey))
        '''
        先绘制各个节点
        '''
        for k in range(self.N):
            node = self.NodeList[k]
            x = node.x
            y = node.y
            plt.scatter(x , y , s = PointSize , alpha = 0.7 , color = 'r')
            plt.text(x , y , str(k+1) , fontsize = 3*ftsize , color = 'gray' , alpha = 0.8)
            plt.text(x , y , 'u = '+str(node.u)+'\nv = '+str(node.v) , fontsize = ftsize , color = 'b')
            pass
        '''
        再绘制连接以及
        各端轴力
        '''
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] != 1:
                    continue
                else:
                    nodej = self.NodeList[j]
                    nodei = self.NodeList[i]
                    plt.plot([nodej.x , nodei.x] , [nodej.y , nodei.y] , linewidth = LineSize , alpha = 0.7 , color = 'g')
                    x1 = 0.8*nodej.x + 0.2*nodei.x
                    x2 = 0.2*nodej.x + 0.8*nodei.x
                    y1 = 0.8*nodej.y + 0.2*nodei.y
                    y2 = 0.2*nodej.y + 0.8*nodei.y
                    plt.text(x1 , y1 , self.InternalForce[j][i] , fontsize = ftsize , color = 'k')
                    plt.text(x2 , y2 , self.InternalForce[i][j] , fontsize = ftsize , color = 'k')
                    pass
                pass
            pass
        '''
        再绘制薄板约束件
        '''
        for sheet in self.SheetList:
            nodei = self.NodeList[sheet.i]
            nodej = self.NodeList[sheet.j]
            nodel = self.NodeList[sheet.l]
            nodem = self.NodeList[sheet.m]
            fillx = np.array([nodei.x , nodej.x , nodel.x , nodem.x])
            filly = np.array([nodei.y , nodej.y , nodel.y , nodem.y])
            plt.fill(fillx , filly , facecolor = 'y' , alpha = 0.3)
            plt.text(np.mean(fillx) , np.mean(filly) , 'q = ' + str(sheet.q) + '\n' + str(sheet.j+1) + '->' + str(sheet.i+1) , fontsize = ftsize , color = 'k')
            pass
        plt.axis('off')
        plt.title("Truss System" , fontsize = 1.5*ftsize)
        plt.show()
        self.pic = pic
        pass

    def SetPrecison(self , dec = 6):
        '''
        更新：
        self.InternalForce内力矩阵，保留dec精度
        各节点信息，保留dec
        重写Report
        '''
        self.InternalForce = np.around(self.InternalForce , decimals = dec)
        for j in range(self.N):
            self.NodeList[j].Px = np.around(self.NodeList[j].Px , decimals = dec)
            self.NodeList[j].Py = np.around(self.NodeList[j].Py , decimals = dec)
            self.NodeList[j].u = np.around(self.NodeList[j].u , decimals = dec)
            self.NodeList[j].v = np.around(self.NodeList[j].v , decimals = dec)
            pass
        for k in range( len(self.SheetList) ):
            self.SheetList[k].q = np.around(self.SheetList[k].q , decimals = dec)
            pass
        self.Report = "Reprort : Information of This Truss System\n\n"
        self.__GetReport()
        #self.__GetFigure()
        pass

    def ExportReport(self , filename = 'Report_of_Truss_System.txt'):
        '''
        导出self.Report计算报告
        至指定filename 的 txt文本文件中
        '''
        f = open(filename , mode = 'w' , encoding = 'utf-8')
        f.write(self.Report)
        f.close()
        print("Successfully Write to File " + filename + ' !')
        pass

    def ExportExcel(self , filename = 'Excel_of_Truss_System.xls'):
        '''
        导出系统整体信息至filename的
        excel表格中
        有多张表格用以说明桁架类信息
        '''
        workbook = xlwt.Workbook(encoding = 'utf-8')
        '''
        1.先写入各个节点的信息
        '''
        sheet1 = workbook.add_sheet('Node 节点信息')
        sheet1.write(0 , 0 , '节点编号ID')
        sheet1.write(0 , 1 , '横向x坐标')
        sheet1.write(0 , 2 , '纵向y坐标')
        sheet1.write(0 , 3 , '横向外载Px')
        sheet1.write(0 , 4 , '纵向外载Py')
        sheet1.write(0 , 5 , '横向位移u')
        sheet1.write(0 , 6 , '纵向位移v')
        for j in range(self.N):
            sheet1.write(j+1 , 0 , j+1)
            sheet1.write(j+1 , 1 , self.NodeList[j].x)
            sheet1.write(j+1 , 2 , self.NodeList[j].y)
            sheet1.write(j+1 , 3 , self.NodeList[j].Px)
            sheet1.write(j+1 , 4 , self.NodeList[j].Py)
            sheet1.write(j+1 , 5 , self.NodeList[j].u)
            sheet1.write(j+1 , 6 , self.NodeList[j].v)
            pass
        '''
        2.再写入连接信息
        '''
        sheet2 = workbook.add_sheet('连接以及内力信息')
        sheet2.write(0 , 0 , '连接编号')
        sheet2.write(0 , 1 , '起点编号')
        sheet2.write(0 , 2 , '终点编号')
        sheet2.write(0 , 3 , '弹性模量')
        sheet2.write(0 , 4 , '横截面积')
        sheet2.write(0 , 5 , '桁架长度')
        sheet2.write(0 , 6 , '桁架内力')
        k = 1
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] != 1:
                    continue
                else:
                    sheet2.write(k , 0 , (k+1)/2)
                    sheet2.write(k , 1 , j+1)
                    sheet2.write(k , 2 , i+1)
                    sheet2.write(k , 3 , self.InfoConnection[str(j) + ',' +str(i)][0])
                    sheet2.write(k , 4 , self.InfoConnection[str(j) + ',' +str(i)][1])
                    sheet2.write(k , 5 , self.InfoConnection[str(j) + ',' +str(i)][2])
                    sheet2.write(k , 6 , self.InternalForce[j][i])
                    '''写入另一侧信息'''
                    k += 1
                    sheet2.write(k , 1 , i+1)
                    sheet2.write(k , 2 , j+1)
                    sheet2.write(k , 3 , self.InfoConnection[str(j) + ',' +str(i)][0])
                    sheet2.write(k , 4 , self.InfoConnection[str(j) + ',' +str(i)][1])
                    sheet2.write(k , 5 , self.InfoConnection[str(j) + ',' +str(i)][2])
                    sheet2.write(k , 6 , self.InternalForce[i][j])
                    k += 1
                    pass
                pass
            pass
        '''
        3.写入剪流信息
        '''
        if len(self.SheetList) == 0:
            pass
        else:
            sheet3 = workbook.add_sheet('剪流信息')
            sheet3.write(0 , 0 , '剪流q编号')
            sheet3.write(0 , 1 , '剪流节点1')
            sheet3.write(0 , 2 , '剪流节点2')
            sheet3.write(0 , 3 , '剪流节点3')
            sheet3.write(0 , 4 , '剪流节点4')
            sheet3.write(0 , 5 , '受剪板剪切模量G')
            sheet3.write(0 , 6 , '受剪板厚t')
            sheet3.write(0 , 7 , '受剪板面积')
            sheet3.write(0 , 8 , '剪流大小')
            for k in range( len(self.SheetList) ):
                sheet3.write(k+1 , 0 , k+1)
                sheet3.write(k+1 , 1 , self.SheetList[k].i)
                sheet3.write(k+1 , 2 , self.SheetList[k].j)
                sheet3.write(k+1 , 3 , self.SheetList[k].l)
                sheet3.write(k+1 , 4 , self.SheetList[k].m)
                sheet3.write(k+1 , 5 , self.SheetList[k].G)
                sheet3.write(k+1 , 6 , self.SheetList[k].t)
                sheet3.write(k+1 , 7 , self.SheetList[k].F)
                sheet3.write(k+1 , 8 , self.SheetList[k].q)
                pass
            pass
        '''
        4.写入整体刚度矩阵
        '''
        sheet4 = workbook.add_sheet('整体刚度矩阵')
        for j in range(2*self.N):
            for i in range(2*self.N):
                sheet4.write(j , i , self.K[j][i])
                pass
            pass
        '''
        5.写入内力矩阵
        '''
        sheet5 = workbook.add_sheet('内力矩阵')
        for j in range(self.N):
            for i in range(self.N):
                sheet5.write(j , i , self.InternalForce[j][i])
                pass
            pass
        '''
        6.写入弹性约束
        '''
        if len(self.SpringList) == 0:
            pass
        else:
            sheet6 = workbook.add_sheet()
            sheet6.write(0 , 0 , '弹性约束编号')
            sheet6.write(0 , 1 , '约束作用点')
            sheet6.write(0 , 2 , '约束方向')
            sheet6.write(0 , 3 , '劲度系数k')
            for k in range( len(self.SpringList) ):
                sheet6.write(k+1 , 0 , k+1)
                sheet6.write(k+1 , 1 , self.SpringList[k].ID)
                sheet6.write(k+1 , 2 , self.SpringList[k].direction)
                sheet6.write(k+1 , 3 , self.SpringList[k].k)
                pass
            pass
        '''
        保存至filename
        '''
        workbook.save(filename)
        print("Successfully Export Truss System to " + filename + '!')
        pass

    def ExportFigure(self , filename = 'Figure_of_Truss_System.png' ,  size = 40 , ftsize = NaN , sizex = NaN , sizey = NaN , PointSize = NaN , LineSize = NaN):
        '''
        写入filename图片文件
        有诸多参数可选择
        '''
        self.__GetFigure(size , ftsize , sizex , sizey , PointSize , LineSize)
        self.pic.savefig(filename)
        print("Successfully Save Figure to " + filename + '!')
        pass

    pass