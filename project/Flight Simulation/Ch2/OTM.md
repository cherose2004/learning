# 斜抛运动
[toc]
## 概述

考虑一个斜抛的物体以初速度$V_0$被抛出，抛出方向为斜向上$\theta$角度。

由于空气阻力对于物体会有阻力作用，因此可以认为存在这样的关系：
$$
D=k V^2\tag{1}
$$

方向作用于速度的反方向。

不妨对速度进行水平和垂直方向的分解，各向受力如下：
$$
\begin{aligned}
D_x=-k\cdot V\cdot V_x\\
D_y=-k\cdot V\cdot V_y\\
V=\sqrt{V_x^2+V_y^2}
\end{aligned}\tag{2}
$$

假设物体质量为一个常数，那么各项因为阻力产生的加速度也与$D$成正比。假设最终的折合系数为$K=\frac{k}{m}$。构造如下迭代格式：

$$
\begin{aligned}
\begin{cases}
V_x(i)-V_x(i-1)&=&-K\cdot V(i-1)\cdot V_x(i-1)\cdot dt\\
V_y(i)-V_y(i-1)&=&-g-K \cdot V(i-1)\cdot V_x(i-1)\cdot dt\\
x(i)-x(i-1)&=&V_x(i)\cdot dt\\
y(i)-y(i-1)&=&V_y(i)\cdot dt
\end{cases}
\end{aligned}\tag{3}
$$

其中初始值：
$$
V_x(0)=V_0 \cos(\theta)\\
V_y(0)=V_0 \sin(\theta)\tag{4}
$$

为此编写了一个对象OTM(Oblicque-Throw-Motion)用以仿真此过程，支持自定义初速度、角度、仿真时间以及仿真步长，并最终将仿真的斜抛曲线绘制出来,并且可视化各个参数。其各个函数定义如下：

## 1.__init__(self,x0=0,y0=0,V0=1,theta=np.pi/4,drag_k=0.01,t=5,dt=0.1)

初始化这个类别，其中每一个值都有默认值。
默认情况下是从$(0,0)$出发，以$V_0=1$为初速度，$\theta=\frac{\pi}{4}$为角度，空气阻力为0，步长为0.1s仿真5s内的运动情况。

- 给定系统初始状态：
```python
init=ms.State(x=x0*m,y=y0*m,vx=vx0*m/s,vy=vy0*m/s)
self.init=init
```
- 设置系统参数：
```python
self.sys=ms.System(init=init,g=g,theta=theta,k=drag_k/m,t_end=t,dt=dt)
```
- 系统仿真开始
```python
self.run_simulation()
```
**一定一定注意单位量纲！特别是$k$单位为$m^{-1}$**

## 2.iter_func(self,state)

步进过程，采用欧拉法，对于上面的(3)式子进行迭代仿真。因为$x,y$方向存在耦合，暂时还没想明白怎么使用四阶龙格库塔仿真，后续可能会补上。

输入当前state,返回下一个状态的state。注意这里有个坑：
```python
vx0=int(Vx*s/m)
vy0=int(Vy*s/m)
V=np.sqrt(vx0**2+vy0**2)*m/s
```
因为变量自带单位，在进行非+-*/运算时，需要先转化为纯数字再进行运算。这里调试代码被卡了很久。

## 3.run_simulation(self):

仿真代码，在__init__()中即调用。返回整个frame，包括$x,y,V_x,V_y$的各个时刻的值，并且将frame和仿真末尾的各个值，交还给self。

## 4.Show_xy_t(self):

绘制$x,y$随时间$t$变化的全过程曲线

## 5.Show_Vxy_t(self):

绘制$V_x,V_y$随时间$t$变化的全过程曲线

## SHow_position(self):

展示整个过程的轨迹，横坐标为$x/m$，纵坐标为$y/m$