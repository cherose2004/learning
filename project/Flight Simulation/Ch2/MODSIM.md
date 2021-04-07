# modsim文档

*完全形而上学的学习*

[toc]

## 1.Syetem()函数

设置系统的各类参数的值

``` python
import modsim as ms
ms.System(init=init,para1=value1,para2=value2...)#设置初状态以及各个参数值
```

## 2.State()函数

用来表示状态值的函数

```python
init=ms.State(T=90)#设置初始状态init,其中T=90
```

## 3.TimeFrame()函数

用来构造时间框架的函数，这个框架下可以存放某一个变量的值

```python
frame=ms.TimeFrame(columns=init.index)#构造一个列向量，其沿着时序推进，并且其列向量存放着温度T的函数
```

## 4.linrange(t_0,t_end,dt)/linspace(t_0,t_end,n)

用来初始化整个仿真时序的一个方法

## 5.plot(frame.u)

传入某一个构造好的序列，自带上时间，以t为横轴，序列u值为纵轴做出一条仿真曲线

```python
ms.plot(frame.u)
ms.decorate(xlabel='',ylabel='')
```

## 6.get_last_value(frame.u)/get_first_value(frame.u)

获得仿真末/初时刻的值

```python
u_final=get_last_value(frame.u)
```

## 7.root_bisect(f,[a,b])

用以搜寻$f(x)=0$在区间$[a,b]$上的根

```python
def f(x):
    return x
res=ms.root_bisect(f,[0,1])
res.root
```

## 8.SweepSeries()
混合扫描序列？
总之是初始化一个TimeFrame()类似的时间序列

## 9.UNITS模块
这个模块是用来给定单位的。用法大概如下吧：
```python
m=ms.UNITS.meter #长度米
s=ms.UNITS.second #时间秒
g=9.8*m/s**2 #设置重力加速度值
```
我疑心这是用sympy符号计算库实现的，但是没有证据。总之这个库得装上用于符号计算，客观的说这个库没有mathematica强大。