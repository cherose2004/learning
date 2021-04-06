# 这是一个TeaMilk模块的说明文档
[toc]
- 我定义了一个class用来封装苏苏老师的这个问题。
- 但后来发现其实System的存在已经是用来普适大多数情况了，有一定封装作用。
- 不过有一些游离的函数我看着很不舒服，于是就用class定义了一下，下面是class说明：

## Liquid class类型说明：


### 1.\_\_init\_\_(self,T0,r,volume,T_env=22,t0=0,tf=5,dt=0.1,name='some liquid')

这是用来初始化的
函数
需要给定
- 初始温度：T0
- 下降比例系数：r
- 体积： v

而下面这些有默认值，可以不给：
- 环境温度： T0=22
- 开始时间： t0=0
- 结束时间： tf=5
- 时间间隔： dt
- 液体名称： 'a kind of liquid'

初始化后，将：
- 初始状态设置：self.init=ms.State(T=T0)初始化状态
- Liquid名称：sefl.name=name
- 设置系统参数：self.system=ms.System(init=self.init,para1=value1...)
- 调用self.run_simulation()仿真


### 2.iter_func(self,state)
仿真过程，输入当前状态，返回下一个dt时刻后的状态
状态的数据类型为modsim.State
不过当前函数只是前进欧拉函数


### 3.run_simulation(self)
仿真函数，直接在__init__中调用，构造frame时序表，其中：
将frame初始化成列向量为init中的变量类型
```python
frame=ms.TimeFrame(columns=self.init.index)
```
给定时序中的frame的初状态：
```python
frame.row[self.system.t0]=self.init
```
生成仿真的全部时序：
```python
ts=ms.linrange(self.system.t0,self.system.t_end,self.system.dt)
```
循环开始进行，仿真过程如下：
```python
for ti in ts:
    frame.row[ti+self.system.dt]=self.iter_func(frame.row[ti])
```
然后将结果交还给self
```python
self.frame=frame
self.T_end=ms.get_last_value(self.frame.T)
```


### 4.mix(self,Liquid2,after=True,left_time=30,new_name='mixture')

将个液体混合起来混合起来，如：milk.mix(tea)
返回的是一杯新的液体
可选参数为：

- Liquid2: 混合液体
- after： 混合发生于仿真前还是仿真后，True为仿真后，否则为前
- left_time:剩余用于仿真的冷却时间
- new_name:混合液体的新名称，比如奶茶之类的 


### 5.show()
展示仿真结果，横坐标为时间t0~t_end
纵坐标为T温度