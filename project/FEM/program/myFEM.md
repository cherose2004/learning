[toc]

---

# myFEM有限元杆系求解架构说明文档

---


---
# 1. Node 节点 类型

## 1.1. 变量

- x : 节点x坐标，默认为0
- y : 节点y坐标位置，默认为0
- u : 节点x方向位移，默认为np.NaN即待求量
- v : 节点y方向位移，默认为np.NaN即待求量
- Px : 节点x方向外载，默认为np.NaN即待求量
- Py : 节点y方向外载荷，默认为np.NaN即待求量

## 1.2. 函数

### 1.2.1. \_\_init\_\_(self , x = 0 , y = 0 , Px = NaN , Py = NaN , u = NaN , v = NaN) 初始化函数

一般而言，对于某个节点只需要给出x和y坐标即可；剩下的参数属于可选参数；建议使用如下命令创建节点：

```python
import myFEM as fem

node = fem.Node(position_x , position_y)
```

若该点为支座点，则可以在创建的时候直接给定约束：

```python
node_support = fem.Node(position_x , position_y , u = 0 , v = 0)
```

若该点为自由节点，则也可以在创建的时候直接给定约束：

```python
node_free = fem.Node(position_x , postion_y , Px = 0 , Py = 0)
```

### 1.2.2. setP(self , Px = NaN , Py = NaN) 力约束函数

例如对某个节点node，将其设置外载约束：

- Px = 10kN
- Py = -10kN

则只需要：

```python
node.setP(Px = 10e3 , Py = -10e3)
# 或者直接按给定顺序输入，如：
# node.setP(10e3 , -10e3)也可以
```

即可


### 1.2.3. setUV(self , u = NaN , v = NaN) 位移约束函数

例如对某个节点node，将其设置位移约束：

- u = 1e-4
- v = 2e-4

则只需要:

```python
node.setUV( u = 1e-4 , v= 2e-4)
# 或者直接按给定顺序输入，如：
# node.setUV(1e-4 , 2e-4)也可以
```

即可




# 2. SysPole 杆系统 类型

## 2.1. 变量

- NodeList : list()列表类型，存放着一连串的节点，暗含标号
- N ： int类型，节点总个数
- NodeConnection : numpy数组类型，由 1 和 0 构成；其 j 行 i 列为 1 ，则表示有 j 号节点指向 i 号节点的杆单元连接；其概念类似dijsktra和floyd算法中的有向邻接矩阵
- dictK : dict()字典类型，存放着局部刚度矩阵$k_{ji}$，调用时应按照dictK['j,i']的格式调用，即$k_{ji}=$dcitK['j,i']
- dictConnection : dict()字典类型，其中存放列表，每个列表['j,i']表示连接 j 和 i 节点的连接信息，包括[0] : 弹性模量E，[1] : 横截面积A ， [2] : 长度l
- K : numpy数组类型，表示系统的整体刚度矩阵，但可能会被弹性元器件更新
- springList : list()列表类型，存放着一系列弹性元器件的字典，每个字典中都有['k']刚度系数，['direction']方向(为'x'或者'y')，以及['id']支撑在数字为'id'的节点上
- Npole ： numpy数组类型，j 行 i 列上记录着 j 连接 i 的杆上轴力
- report : 字符串类型，为最终打印生成的报告
- pic : matplotlib图片类型，为最终根据计算结果绘制的轴力、节点位移图

## 2.2. 公有函数

### 2.2.1. \_\_init\_\_(self , ls) 初始化函数

初始化函数，传入一个全是Node的list列表，从而初始化系统，生成如下变量：

- NodeList : 存放着节点顺序表
- N : 为节点个数
- NodeConnection : 为连接矩阵，有向，暂时全为0
- dictK : 字典类型，用以存放各种名称的部分刚度矩阵，暂时为空
- dictConnection : 字典类型，用以存放某个连接的连接信息，暂时为空
- K : 组装刚度矩阵，暂时全为0
- springList : 弹性元器件列表，存储着弹性元器件存放列表，暂时为空
- report : 生成报告字符串，暂时只有标题

使用方法大致如下：

```python
nodeList = [node1 , node2 , node3...nodeN]
system = fem.SysPole(nodeList)
```

运行结束后，会打印输出提醒:

```bash
successfully build system !
```


### 2.2.2. connect(self , j , i , E = 200e9 , A = 0.01) 连接节点函数

连接系统中的节点，需要对给定：

- j : 连接起点
- i : 连接终点
- E ： 连接杆的弹性模量
- A ： 横截面积

在这个函数中，会进行如下操作：

- 将NodeConnection的 j 行 i 列置为 1 ，表明有 j 向 i 的杆连接
- 对dictConnection连接信息字典中的，['j,i']键值内添加列表[E,A,l]，其中l为杆长，根据节点相对位置计算而得
- 对dictK局部刚度矩阵，['j,i']键值设为计算而得的局部刚度矩阵，调用了__getK()私有函数

具体用法如下：

```python
system.connect(j , i , E , A)
```

即完成了对节点间的杆连接


### 2.2.3. generate() 刚度矩阵生成函数

在连接结束系统之后，可以获取系统的整体刚度矩阵；把dictK中所有的局部刚度矩阵叠加到总体刚度矩阵K中，就获得了最终的刚度矩阵；过程中用到了__addK()私有函数

具体用法如下:

```python
system.generate()
```

运行成功后，会打印输出提醒：

```bash
successfully get matrix K !
```


### 2.2.4. setP(self , k , Px = NaN , Py = NaN) 力约束函数

对 k 节点进行力约束，用法同Node类型中的setP()函数，只是现在需要指定节点编号 k

具体用法如下：

```python
system.setP(i , Px = 1e4 , Py = -1e4)
```

### 2.2.5. setUV(self , k , u = NaN , v = NaN) 位移约束函数

用法同上，类似，不赘述


### 2.2.6. setSpring(self , i , k = 2e9 , dire = 'x') 弹性约束函数

对 i 节点的dire方向进行刚度系数为k的弹性约束，其会做如下操作：

- 在springList中，加入一个字典，该字典为['id':i , 'k':k , 'direction':dire]，记录了弹簧的连接信息
- 在 i 节点对应的dire方向上，在刚度矩阵主对角线上对应元素+k，并设置该节点约束为dire方向上外载荷为0；在后续求解过程中，求出的位移乘-k即获得该节点的弹性支承载荷

比如在3号节点的y方向，施加劲度系数为1e8的弹簧支座，则：

```python
system.setSpring(3 , k = 1e8 , dire = 'y')
```

### 2.2.7. solve() 系统求解函数

在连接结束、约束给足、刚度矩阵生成之后，最终求解该矩阵；求解方式是分块矩阵求解；大致理论阐述如下：

位移和力的总共未知数量应该为节点数的两倍，已知数量等于未知数量——通过矩阵的分块求解，调整，可以得到如下的分块矩阵:

$$
\begin{bmatrix}
P_{1(m\times 1)}\\
P_{2(n\times 1)}
\end{bmatrix}

=

\begin{bmatrix}
A_{(m\times n)} & B_{(m\times m)}\\
C_{(n\times n)} & D_{(n\times m)}
\end{bmatrix}

\begin{bmatrix}
uv_{1(n\times 1)}\\
uv_{2(m\times 1)}
\end{bmatrix}
$$

其中$A,B,C,D,P_1,uv_1$均已知，所以可以分块得到：

$$
\begin{aligned}
uv_2 &= B^{-1}(P_1-A uv_1)\\
P_2 &= C uv_1 + D uv_2
\end{aligned}
$$

求解过程相当复杂，步骤大约如下：

- 调用__getSolve()私有函数，获取待求解的一系列值p , uv , pNaN , uvNaN , p1 , p2 , uv1 , uv2
- 调用__modifyK()私有函数，分块切片刚度矩阵获得k11 , k12 , k21 , k22
- 按照上述流程求解
- 将求解过程返还到NodeList中各个节点上，若有弹性支承力给定为-kx
- 更新Npole的各个轴力信息，获得杆的轴力矩阵
- 调用__getreport()私有函数，将报告存入report字符串
- 调用getpic()函数，绘制轴力图、节点位移图，更新pic变量

具体用法如下：

```python
system.solve()
```

运行成功后，打印输出信息：

```bash
successfully update node infomation !
```

### 2.2.8. info(self) 信息打印函数

将report字符串打印到控制台上

具体用法如下：

```python
system.info()
```

会在控制台(bash)中打印出report报告


### 2.2.9. export(self , filename = 'report.txt' , picname = 'pic.png') 导出计算结果函数

- 导出report至filename中
- 导出pic至picname中

具体用法如下：

```python
system.export('demo.txt' , 'demo.png')
```

即在同目录下生成报告文件'dem.txt'和图片文件'demo.png'


### 2.2.10. getpic(self , precision = 6 , size = 40 , ftsize = 50) 绘图函数

更新pic变量，重绘

- precision 绘图标注的数据精度
- 图像大小
- 字体大小

具体用法如下：

```python
system.getpic(precision = 8 , size = 50 , ftsize = 90)
```



## 2.3. 私有函数

因为私有函数是在类内部调用，所以这里从简说明

### 2.3.1. __getK(self , E = 200e9 , A = 0.01 , l = 1) 获取局部刚度矩阵函数

即：

$$
\frac{EA}{l}
\begin{bmatrix}
1 & -1\\
-1 & 1 
\end{bmatrix}
$$

返回该矩阵


### 2.3.2. __addK(self , j , i) 组装矩阵函数

把dictK['j.i']加入K中，也即将$k_{ji}$加入总体刚度矩阵$K$中


### 2.3.3. __getpartK(self , row , col) 矩阵提取函数

将总体刚度矩阵K中的row行编号，和col列编号，相交获得的局部矩阵提取出来，并返回


### 2.3.4. __modifyK(self , pNaN , uvNaN) 矩阵分块函数

pNaN记录着未知力编号，uvNaN记录着位移未知编号，以此控制分块总体刚度矩阵，获得四块矩阵k11 , k12 , k21 , k22并返回


### 2.3.5. __getSolve(self) 求解预处理函数

获取：
- p : 力向量，包含代求值
- uv ：位移向量，包含代求值
- pNaN ：未知力编号
- uvNaN ：未知位移编号
- p1 ：已知力向量 
- p2 ：未知力向量
- uv1 ：已知位移向量
- uv2 ：未知位移向量


### 2.3.6. __getreport(self) 生成报告字符串函数

把计算结果写入report字符串内，并存储