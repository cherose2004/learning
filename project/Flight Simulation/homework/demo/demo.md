# 利用Opencv读取曲线大致想法

首先Opencv是个跨平台的图像处理库，在python上安装可以使用bash：
```bash
pip install opencv-python
```

不过考虑到源有点慢，应当换清华源安装：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
```

整体的思路大概是：

1. 用opencv读取图片，得到一个3\*M\*N的矩阵，其中3表示某一像素点上的RGB色彩
2. 将图片灰度化，得到灰度图，退化为1\*M\*N的矩阵
3. 将灰度图二值化，此时图中只有255和0两种值，为1\*M\*N的矩阵
4. 读取所有位置上$(i,j)$值为0的，存入xi\[i1,i2,i3...\]和yj\[j1,j2,j3...\]矩阵，既有:pic\[ik\]\[jk\]=0,k=1,2,3...
5. 当前读取的$(i,j)$位置会和图像坐标系中的$(x,y)$存在一个关系映射，而且显然这个关系应该是线性的，大致会有：
$$
\left[
    \begin{matrix}
    x\\y
    \end{matrix}
\right]
=
\left[
    \begin{matrix}
    q_{11} & q_{21}\\
    q_{12} & q_{22}
    \end{matrix}
\right]
\left[
    \begin{matrix}
    i\\j
    \end{matrix}
\right]
+
\left[
    \begin{matrix}
    x_0\\y_0
    \end{matrix}
\right]
$$
这些参数的取值和真个坐标系的尺度、以及坐标轴和图片总大小、以及图片裁剪情况都有关。所以每一张图都会有这样一组不同的值。而且感觉似乎这只能人工测算。

6. 最后因为可能面临多个曲线族，所以要对筛选出来的点进行区域划分。比如大致用y=2x和y=x/2两条曲线区分y=x与y=x/3，大概流程如下：
```python
x_line1=[]
y_line2=[]
x_line2=[]
y_line2=[]
for i in range(len(x)):
    if y[i]>2*x[i] and y[i]<x[i]/2:
        x_line1.append(x[i])
        y_line1.append(y[i])
    else:
        x_line2.append(x[i])
        y_line2.append(y[i])
        pass
    pass
# x_line1,y_line1中存储着y=x离散点
# x_line2,y_line2中存储着y=x/3离散点
```
7. 需要注意的一点是：剩下的那些$(x,y)$中，其实存在重复、未排序的现象。因此需要定义一个去重、排序的过程。图中因为一个x可能对应多个y像素点，因此需要对同一个x对应的y做均值处理。从运算代价上看，似乎先排序再去重会好一些。
8. 总结下来，大致是->读图——二值化——定位转换——抠取——排序去重——得到最终的x,y值

## 第五步的特别说明：
既然有：
$$
\left[
    \begin{matrix}
    x\\y
    \end{matrix}
\right]
=
\left[
    \begin{matrix}
    q_{11} & q_{21}\\
    q_{12} & q_{22}
    \end{matrix}
\right]
\left[
    \begin{matrix}
    i\\j
    \end{matrix}
\right]
+
\left[
    \begin{matrix}
    x_0\\y_0
    \end{matrix}
\right]
$$
那么如果点$(i_k,j_k)\rightarrow(x_k,y_k)$，那么有：
$$
\begin{cases}
i_k\cdot q_{11}+j_k\cdot q_{21}+x_0=x_k\\
i_k\cdot q_{12}+j_k\cdot q_{22}+x_0=y_k
\end{cases}
$$
因为刚体在平面上有三个自由度，所以需要$k=1,2,3$三组点到点的映射才能满足：
$$
\begin{cases}
(i_1,j_1)\rightarrow(x_1,y_1)\\
(i_2,j_2)\rightarrow(x_2,y_2)\\
(i_3,j_3)\rightarrow(x_3,y_3)
\end{cases}
$$
因此可以得到：
$$
\left(
    \begin{matrix}
    i_1 & 0 & j_1 & 0 & 1 & 0\\
    0 & i_1 & 0 & j_1 & 0 & 1\\
    i_2 & 0 & j_2 & 0 & 1 & 0\\
    0 & i_2 & 0 & j_2 & 0 & 1\\
    i_3 & 0 & j_3 & 0 & 1 & 0\\
    0 & i_3 & 0 & j_3 & 0 & 1
    \end{matrix}
\right)

\left(
    \begin{matrix}
    q_{11}\\
    q_{12}\\
    q_{21}\\
    q_{22}\\
    x_0\\
    y_0
    \end{matrix}
\right)

=

\left(
    \begin{matrix}
    x_1\\
    y_2\\
    x_2\\
    y_2\\
    x_3\\
    y_3
    \end{matrix}
\right)
\\
\downarrow
\\
\left(
    \begin{matrix}
    q_{11}\\
    q_{12}\\
    q_{21}\\
    q_{22}\\
    x_0\\
    y_0
    \end{matrix}
\right)
=
\left(
    \begin{matrix}
    i_1 & 0 & j_1 & 0 & 1 & 0\\
    0 & i_1 & 0 & j_1 & 0 & 1\\
    i_2 & 0 & j_2 & 0 & 1 & 0\\
    0 & i_2 & 0 & j_2 & 0 & 1\\
    i_3 & 0 & j_3 & 0 & 1 & 0\\
    0 & i_3 & 0 & j_3 & 0 & 1
    \end{matrix}
\right)^{-1}

\left(
    \begin{matrix}
    x_1\\
    y_1\\
    x_2\\
    y_2\\
    x_3\\
    y_3
    \end{matrix}
\right)
$$

当然观察后容易发现可以化简,令：
$$
A=
\left(
    \begin{matrix}
    i_1 & j_1 & 1\\
    i_2 & j_2 & 1\\
    i_3 & j_3 & 1
    \end{matrix}
\right)
$$

则：
$$
A
\left(
    \begin{matrix}
    q_{11}\\
    q_{21}\\
    x_0 
    \end{matrix}
\right)
=
\left(
    \begin{matrix}
    x_1\\
    x_2\\
    x_3 
    \end{matrix}
\right)
\\
\\
A
\left(
    \begin{matrix}
    q_{12}\\
    q_{22}\\
    y_0 
    \end{matrix}
\right)
=
\left(
    \begin{matrix}
    y_1\\
    y_2\\
    y_3 
    \end{matrix}
\right)
$$

所以不难发现:

$$
\left(
    \begin{matrix}
    q_{11}\\
    q_{21}\\
    x_0\\
    q_{12}\\
    q_{22}\\
    y_0
    \end{matrix}
\right)

=

\left(
    \begin{matrix}
    A^{-1} & 0\\
    0 & A^{-1}
    \end{matrix}
\right)
\left(
    \begin{matrix}
    x_1\\
    x_2\\
    x_3\\
    y_1\\
    y_2\\
    y_3
    \end{matrix}
\right)
$$

现在唯一的问题是怎么确定这三个点。这是个很繁琐的问题。