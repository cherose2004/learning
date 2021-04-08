# 这是一个用于说明龙格库塔（Runge-Kutta）方法的的文档
[toc]

## 1.一阶微分的四阶精度Runge-Kutta

对于这样的方程：
$$
\frac{dy}{dx}=f(x,y)
$$

我们可以选取一定的步长$h$求解。在已知$x_i,y_i$的情况下：我们通过这样的方式得到$x_{i+1},y_{i+1}$。

$$
\begin{aligned}
&\begin{cases}

k_1=f(x_i,y_i)\\

k_2=f(x_i+\frac{h}{2},y_i+k_1\cdot\frac{h}{2})\\

k_3=f(x_i+\frac{h}{2},y_i+k_2\cdot\frac{h}{2})\\

k_4=f(x_i+h,y_i+k_3\cdot h)

\end{cases}\\
&\begin{cases}
x_{i+1}=x_i+h\\
y_{i+1}=y_i+\frac{h}{6}\cdot(k_1+2k_2+2k_3+k_4)
\end{cases}
\end{aligned}
$$

为了实现这个迭代步骤，我定义了**RK4_iter(x,y,f,h=0.01)**函数，其中,x表示当前的x值，y表示当前的y值，f表示$y'=f(x,y)$中的f函数，步长有默认值0.01。

返回值为下一步的x和y，其函数展示如下：

```python
def RK4_iter(x,y,f,h=0.01):
    k1=f(x,y)
    k2=f(x+h/2,y+k1*h/2)
    k3=f(x+h/2,y+k2*h/2)
    k4=f(x+h,y+k3*h)
    x_next=x+h
    y_next=y+h*(k1+2*k2+2*k3+k4)/6
    return x_next,y_next
    pass
```

将迭代步骤置于整个求解过程中，我定义了函数**RK4(x0,y0,f,h=0.01,final=5)**，其给定了初值x0和y0，指定了函数f，计算步长与计算总长度。

返回值为x和y的一串numpy的数组，函数展示如下。

```python
def RK4(x0,y0,f,h=0.01,final=5):
    n=math.floor(final/h)
    x=np.zeros(n)
    y=np.zeros(n)
    x[0],y[0]=x0,y0
    for i in range(1,n):
        x[i],y[i]=RK4_iter(x[i-1],y[i-1],f,h)#调用迭代函数
        pass
    return x,y
    pass
```


## 二阶微分的四阶精度Runge-Kutta

对于这样的方程：
$$
\frac{d^2y}{dt^2}=f(x,y,y')
$$

我们同样可以选择一定的步长$h$求解，在给定了$x_i,y_i,y'_i$的情况下我们可以用如下的迭代格式得到下一步的$x_{i+1},y_{i+1},y'_{i+1}$。

$$
\begin{aligned}
&\begin{cases}

k_1=f(x_i,y_i,y'_i)\\

k_2=f(x_i+\frac{h}{2},y_i+y'_i\cdot\frac{h}{2},y'_i+k_1\cdot\frac{h}{2})\\

k_3=f(x_i+\frac{h}{2},y_i+y'_i\cdot\frac{h}{2}+k_1\cdot\frac{h^2}{4},y_i+k_2\cdot\frac{h}{2})\\

k_4=f(x_i+h,y_i+y'_i\cdot\frac{h}{2}+k_2\cdot\frac{h^2}{2},y'_i+k_3\cdot h)

\end{cases}\\


&\begin{cases}
x_{i+1}=x_i+h\\
y_{i+1}=y_i+h\cdot y_{i+1}+\frac{h^2}{6}\cdot(k_1+k_2+k_3)\\
y'_{i+1}=y_i+\frac{h}{6}\cdot(k_1+2k_2+2k_3+k_4)
\end{cases}
\end{aligned}
$$

为了实现这个迭代步骤，我定义了**RK4_iter_2(x,y,y1,f,h=0.01)**函数，其中,x表示当前的x值，y表示当前的y值，y1表示当前的y的一阶导数值，f表示$y'=f(x,y)$中的f函数，步长有默认值0.01。

返回值为下一步的x，y和y1，其函数展示如下：
```python
def RK4_iter_2(x,y,y1,f,h=0.01):
    L1=f(x,y,y1)
    L2=f(x+h/2,y+h*y1/2,y1+h*L1/2)
    L3=f(x+h/2,y+h*y1/2+h**2*L1/4,y1+h*L2/2)
    L4=f(x+h,y+h*y1+h**2*L2/2,y1+h*L3)
    x_next=x+h
    y1_next=y1+h*(L1+2*L2+2*L3+L4)/6
    y_next=y+h*y1+(L1+L2+L3)*h**2/6
    return x_next,y_next,y1_next
    pass
```

将迭代步骤置于整个求解过程中，我定义了函数**RK4_2(x0,y0,y01,f,h=0.01,final=5)**，其给定了初值x0,y0和y01，即一阶导数初值，指定了函数f，计算步长与计算总长度。

返回值为x，y和y1的一串numpy的数组，函数展示如下。

```python
def RK4_2(x0,y0,y01,f,h=0.01,final=5):
    n=math.floor(final/h)
    x=np.zeros(n)
    y=np.zeros(n)
    y1=np.zeros(n)
    x[0],y[0],y1[0]=x0,y0,y01
    for i in range(1,n):
        x[i],y[i],y1[i]=RK4_iter_2(x[i-1],y[i-1],y1[i-1],f,h)
        pass
    return x,y,y1
    pass
```