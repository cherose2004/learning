import numpy as np
import math

def RK4_iter(x,y,f,h=0.01):
    k1=f(x,y)
    k2=f(x+h/2,y+k1*h/2)
    k3=f(x+h/2,y+k2*h/2)
    k4=f(x+h,y+k3*h)
    x_next=x+h
    y_next=y+h*(k1+2*k2+2*k3+k4)/6
    return x_next,y_next
    pass

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