# modyfied by bcynuaa 2021/6/8


import numpy as np
import matplotlib.pyplot as plt
NaN = np.NaN

class Node:

    def __init__(self , x = 0 , y = 0 , Px = NaN , Py = NaN , u = NaN , v = NaN):

        '''
        生成节点类型，需要给出x,y坐标
        Px，Py
        u，v
        约束可以不给出，默认为待求值
        '''

        self.x = x
        self.y = y
        self.setP(Px , Py)
        self.setUV(u , v)
        pass

    def setP(self , Px = NaN , Py = NaN):

        '''
        设置Px和Py约束，默认为未知量，待求
        '''

        self.Px = Px
        self.Py = Py
        pass

    def setUV(self , u = NaN , v = NaN):

        '''
        设置u和v约束，默认为未知量，待求
        '''

        self.u = u
        self.v = v
        pass

    pass

class SysPole:


    def __init__(self , ls):

        '''
        初始化函数，传入一个Node类列表，从而建立系统
        NodeList : 存放着节点顺序表
        N : 为节点个数
        NodeConnection : 为连接矩阵，有向，暂时为全0列
        dictK : 字典类型，用以存放各种名称的部分刚度矩阵
        dictConnection : 字典类型，用以存放某个连接的连接信息
        K : 组装刚度矩阵，暂时全为0
        springList : 弹性元器件列表，存储着弹性元器件存放列表，暂时为空
        report : 生成报告字符串
        '''

        self.NodeList = ls
        self.N = len(ls)
        self.NodeConnection = np.zeros([self.N , self.N])
        self.dictK = dict()
        self.dictConnection = dict()
        self.K = np.zeros([2 * self.N , 2 * self.N])
        self.springList = list()
        self.report = 'Report : Information of Each Node\n\n'
        print("successfully build system !")
        pass


    def __getK(self , E = 200e9 , A = 0.01 , l = 1):

        '''
        根据E，A，l给出杆单元的局部刚度矩阵
        '''
        mat = np.array([
            [1 , -1],
            [-1 , 1]
        ])
        mat = E * A / l * mat
        return mat
        pass

    def connect(self , j , i , E = 200e9 , A = 0.01):

        '''
        根据给定的刚度参数E，A来连接节点j , i，有向
        更新NodeConnection连接矩阵信息
        并且在dictK中附加键名为'ji'的刚度矩阵键值
        '''

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
        k = self.__getK(E , A , l)
        K = dire.T.dot( k ).dot( dire )
        self.dictK[str(j) +  ',' + str(i)] = K
        connect = [E , A , l , dire]
        self.dictConnection[str(j) + ',' +str(i)] = connect
        pass


    def __addK(self , j , i):
        
        '''
        在总体刚度矩阵K中，组装上dictK['ji']这一个刚度矩阵
        分开传入j和i即可
        '''

        Kji = self.dictK[str(j) + ',' + str(i)]
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

        '''
        connect结束后，进行系统生成
        会更新最终的组装刚度矩阵K
        '''

        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] == 0:
                    continue
                else:
                    self.__addK(j+1 , i+1)
                    pass
                pass
            pass
        print("successfully get matrix K !")
        pass


    def setP(self , k , Px = NaN , Py = NaN):

        '''
        设置k号节点上Px和Py约束参数，默认不设置，即为代求量
        '''

        self.NodeList[k-1].setP(Px , Py)
        pass


    def setUV(self , k , u = NaN , v = NaN):

        '''
        设置k号节点上u和v约束参数，默认不设置，即为代求量
        '''

        self.NodeList[k-1].setUV(u , v)
        pass

    def setSpring(self , i , k = 2e9 , dire = 'x'):
        tmp = dict()
        tmp['id'] = i-1
        tmp['k'] = k
        tmp['direction'] = dire
        if dire == 'x':
            self.NodeList[i-1].Px = 0
            self.NodeList[i-1].u = NaN
            self.K[2*(i-1)][2*(i-1)] += k
            pass
        else:
            self.NodeList[i-1].Py = 0
            self.NodeList[i-1].v = NaN
            self.K[2*i-1][2*i-1] += k
            pass
        self.springList.append(tmp)
        pass


    def __getpartK(self , row , col):
        
        '''
        得到刚度矩阵row和col所控制的切片矩阵
        返回刚度矩阵K，在row中序号、以及col序号所相交形成的矩阵
        '''

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


    def __modifyK(self , pNaN , uvNaN):
        
        '''
        将K刚度矩阵调整，分割为4块
        让已知约束力和已知约束位移对应在一起
        生成：m*n , m*m , n*n , n*m的四块分块矩阵并返回
        '''

        n = pNaN.size
        m = uvNaN.size
        k11 = self.__getpartK(uvNaN , pNaN)
        k12 = self.__getpartK(uvNaN , uvNaN)
        k21 = self.__getpartK(pNaN , pNaN)
        k22 = self.__getpartK(pNaN , uvNaN)
        return k11 , k12 , k21 , k22
        pass

    def __getSolve(self):

        '''
        用于solve的预处理
        分解还得代求量
        返回：
        p , uv , pNaN , uvNaN , p1 , p2 , uv1 , uv2
        '''

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

        return p , uv , pNaN , uvNaN , p1 , p2 , uv1 , uv2
        pass


    def solve(self):

        '''
        在约束给定以后，求解整个系统情形
        方法为分块矩阵求解，调整对应已知量关系求解
        更新信息进入NodeList中的每一个节点
        并且在连接矩阵的索引下，生成内力矩阵
        '''
        p , uv , pNaN , uvNaN , p1 , p2 , uv1 , uv2 = self.__getSolve()

        #矩阵分块
        k11 , k12 , k21 , k22 = self.__modifyK(pNaN , uvNaN)

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

        #将p和uv写入各个节点
        for k in range(self.N):
            self.NodeList[k].setP(Px = p[2*k] , Py = p[2*k+1])
            self.NodeList[k].setUV(u = uv[2*k] , v = uv[2*k+1])
            pass
        #对弹性元器件作用的节点上，进行原先置0力的更新
        for spring in self.springList:
            i = spring['id']
            k = spring['k']
            if spring['direction'] == 'x':
                self.NodeList[i].Px = k * self.NodeList[i].u
                pass
            else:
                self.NodeList[i].Py = k * self.NodeList[i].v
                pass
            pass
        print("successfully update node infomation !")

        #生成各个节点杆力,存入Npole矩阵中
        self.Npole = np.zeros([self.N , self.N])
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] == 0:
                    continue
                else:
                    connect = self.dictConnection[str(j+1) + ',' +str(i+1)]
                    e = connect[0]
                    a = connect[1]
                    l = connect[2]
                    ke = self.__getK(e , a , l)
                    lam = connect[3]
                    nodej = self.NodeList[j]
                    nodei = self.NodeList[i]
                    delta = np.array([
                        nodej.u , nodej.v , nodei.u , nodei.v
                    ])
                    s = ke.dot(lam).dot(delta)
                    self.Npole[j][i] = s[1]
                    pass
                pass
            pass

        #生成报告文本
        self.__getreport()
        self.getpic()
        pass


    def __getreport(self):

        '''
        将solve完的结果更新到report字符串中
        '''

        for i in range(40):
            self.report += '*'
            pass
        self.report += '\n'
        self.report += '\nConnection Matrix : \n'
        self.report += str(self.NodeConnection) + '\n'
        self.report += '\nInternel Force Matrix : \n'
        self.report += str(self.Npole) + '\n\n\n'
        for k in range(self.N):
            for i in range(30):
                self.report += '-'
                pass
            node = self.NodeList[k]
            self.report += '\n Node' + str(k+1) + ':\n Position : ( '
            self.report += str(node.x) + ' , ' + str(node.y) + ' )\n\n'
            self.report += 'Externel Load : \n'
            self.report += 'Horizontal Load Px = ' + str(node.Px) + '\n'
            self.report += 'Vertical Load Py = ' + str(node.Py) + '\n\n'
            self.report += 'Displacement : \n'
            self.report += 'Horizontal Displacement u = ' + str(node.u) + '\n'
            self.report += 'Vertical Displacement v = ' + str(node.v) +'\n\n'
            pass
        for i in range(40):
            self.report += '*'
            pass
        pass


    def getpic(self , precision = 6 , size = 40 , ftsize = 50):
        
        '''
        绘制整个图像存储入self.pic中
        precision : 控制显示精度
        size : 控制图片大小
        ftsize : 控制字体大小
        '''

        self.pic = plt.figure(facecolor = 'white' , figsize = (size , size) )
        for i in range(self.N):
            node = self.NodeList[i]
            px = node.x
            py = node.y
            plt.scatter(px , py , s = 40*size , alpha = 0.7 , color = 'r')
            plt.text(px , py , '(' + str(round(node.u , precision)) + ' , ' + str(round(node.v , precision)) + ')' , fontsize = ftsize , color = 'b')
            plt.text(px , py , str(i+1) , fontsize = ftsize+30 , color = 'gray' , alpha = 0.8)
            pass
        for j in range(self.N):
            for i in range(self.N):
                if self.NodeConnection[j][i] == 0:
                    continue
                else:
                    nodej = self.NodeList[j]
                    nodei = self.NodeList[i]
                    plt.plot([nodej.x , nodei.x] , [nodej.y , nodei.y] , linewidth = size/4 , alpha = 0.7 , color = 'g')
                    px = 0.4*nodej.x + 0.6*nodei.x
                    py = 0.4*nodej.y + 0.6*nodei.y
                    plt.text(px , py , str(self.Npole[j][i].round(precision)) , fontsize = ftsize , color = 'k')
                    pass
                pass
            pass
        plt.axis('off')
        plt.title('Whole Information' , fontsize = ftsize+10)
        pass


    def info(self , precision = 5):
        
        '''
        打印报告信息
        '''

        print(self.report)
        self.pic.show()

        pass


    def export(self , filename = 'report.txt' , picname = 'pic.png' , precision = 5):
        
        '''
        将报告写入filename文件中
        画图
        给出精度格式
        '''

        f = open(filename , mode = 'w' , encoding = 'utf-8')
        f.write(self.report)
        f.close()
        print("successfully write to file " + filename + ' !')

        self.pic.savefig(picname)

        pass


    pass