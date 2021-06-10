import numpy as np # numpy计算库
import matplotlib.pyplot as plt # matplotlib绘图库
import myFEM as fem # 导入我写的有限元方法计算库



P = 10e3 #外载荷
a = 100e-2 #边长
f = 20e-4 #横截面积
E = 7e6 * 10**4 #弹性模量
mu = 0.3 #泊松比，似乎没有用到



nodeList = list() #节点列表，预设为空

for i in range(4): #1-8节点加入
    tmp1 = fem.Node(0 , i * a , Px = 0 , Py = 0)
    tmp2 = fem.Node(a , i * a , Px = 0 , Py = 0)
    nodeList.append(tmp1)
    nodeList.append(tmp2)
    pass

nodeList.append( fem.Node(a , 4*a , Px = 0 , Py = 0) ) #9节点

for i in range(5): #10-19节点
    tmp1 = fem.Node( (2 + i) * a , 3 * a , Px = 0 , Py = 0)
    tmp2 = fem.Node( (2+i) * a , 4 * a , Px = 0 , Py = 0)
    nodeList.append(tmp1)
    nodeList.append(tmp2)
    pass

nodeList.append( fem.Node(7 * a , 3 * a , Px = 0 , Py = 0) ) #20节点

for i in range(3): #剩余节点
    tmp1 = fem.Node( 6 * a , (2 - i) * a , Px = 0 , Py = 0)
    tmp2 = fem.Node( 7*a , (2 - i) * a , Px = 0 , Py = 0)
    nodeList.append(tmp1)
    nodeList.append(tmp2)
    pass

sys = fem.SysPole(nodeList) #系统生成

for i in [1 , 2 , 25 , 26]: #支座的约束生成
    sys.setUV(i , u = 0 , v = 0)
    sys.setP(i , Px = np.NaN , Py = np.NaN)
    pass

for i in [13 , 15]: #给定的外载荷约束
    sys.setP(i , Px = 0 , Py = - P)
    pass

del i , tmp1 , tmp2



for i in [1 , 3 , 5 , 8 , 10 , 12 , 14 , 16]: # 连接 5 根杆节点
    sys.connect(i , i+2 , E , f)
    sys.connect(i , i+3 , E , f)
    sys.connect(i+1 , i+2 , E , f)
    sys.connect(i+1 , i+3 , E , f)
    sys.connect(i+2 , i+3 , E , f)
    pass

for i in [26 , 24]: # 连接 5 根杆节点
    sys.connect(i-2 , i , E , f)
    sys.connect(i-3 , i , E , f)
    sys.connect(i-2 , i-1 , E , f)
    sys.connect(i-3 , i-1 , E , f)
    sys.connect(i-3 , i-2 , E , f)
    pass

# 连接剩下的节点
sys.connect(7 , 9 , E , f)
sys.connect(8 , 9 , E , f)
sys.connect(19 , 20 , E , f)
sys.connect(18 , 20 ,E , f)
sys.connect(18 , 22 , E , f)
sys.connect(18 , 21 , E , f)
sys.connect(20 , 22 , E , f)
sys.connect(20 , 21 , E , f)

del i

# 系统生成
sys.generate()



sys.solve() # 系统求解
sys.getpic(ftsize = 15) # 得到系统图片
sys.export('hw.txt' , 'hw.png') # 导出报告以及图片


#导出信息报告
import xlwt

excel = xlwt.Workbook(encoding = 'utf-8')
sheet1 = excel.add_sheet('轴力信息表')
sheet2 = excel.add_sheet('节点信息表')


#轴力信息录入
sheet1.write(0 , 0 , '轴编号')
sheet1.write(0 , 1 , '轴起点编号')
sheet1.write(0 , 2 , '轴终点编号')
sheet1.write(0 , 3 , '轴力大小/N')

k = 1
for j in range(sys.N):
    for i in range(sys.N):
        if sys.NodeConnection[j][i] == 0:
            continue
            pass
        else:
            sheet1.write(k , 0 , k)
            sheet1.write(k , 1 , j+1)
            sheet1.write(k , 2 , i+1)
            sheet1.write(k , 3 , sys.Npole[j][i])
            k += 1
            pass
        pass
    pass


#节点信息录入
sheet2.write(0 , 0 , '节点编号')
sheet2.write(0 , 1 , '节点x坐标')
sheet2.write(0 , 2 , '节点y坐标')
sheet2.write(0 , 3 , '节点水平位移u')
sheet2.write(0 , 4 , '节点垂直位移v')
sheet2.write(0 , 5 , '节点水平受载Px')
sheet2.write(0 , 6 , '节点垂直受载Py')

for j in range(sys.N):
    node = sys.NodeList[j]
    sheet2.write(j+1 , 0 , j+1)
    sheet2.write(j+1 , 1 , node.x)
    sheet2.write(j+1 , 2 , node.y)
    sheet2.write(j+1 , 3 , node.u)
    sheet2.write(j+1 , 4 , node.v)
    sheet2.write(j+1 , 5 , node.Px)
    sheet2.write(j+1 , 6 , node.Py)
    pass


excel.save('hw.xlsx')