import numpy as np
import math

def adams_iter(xi,yi,xi_,yi_,f,h=0.01):
    fi=f(xi,yi)
    fi_=f(xi_,yi_)
    x_next=xi+h
    y_next=yi+h/2*(3*fi-fi_)
    return x_next,y_next
    pass

def adams(x0,y0,f,h=0.01,final=5):
    n=math.floor(final/h)
    x=np.zeros(n)
    y=np.zeros(n)
    x[0],y[0]=x0,y0
    x[1]=x0+h
    y[1]=y0+h*f(x0,y0)
    for i in range(2,n):
        x[i],y[i]=adams_iter(x[i-1],y[i-1],x[i-2],y[i-2],f,h)#调用迭代函数
        pass
    return x,y
    pass

def adams_iter_2(xi,yi,y1i,xi_,yi_,y1i_,f,h=0.01):
    fi=f(xi,yi,y1i)
    fi_=f(xi_,yi_,y1i_)
    x_next=xi+h
    y1_next=y1i+h/2*(3*fi-fi_)
    y_next=yi+h/2*(y1_next+y1i)
    return x_next,y_next,y1_next
    pass

def adams_2(x0,y0,y10,f,h=0.01,final=5):
    n=math.floor(final/h)
    x=np.zeros(n)
    y=np.zeros(n)
    y1=np.zeros(n)
    x[0],y[0],y1[0]=x0,y0,y10
    x[1]=x0+h
    y1[1]=y10+f(x0,y0,y10)*h
    y[1]=y0+(y1[1]+y10)*h/2
    for i in range(2,n):
        x[i],y[i],y1[i]=adams_iter_2(x[i-1],y[i-1],y1[i-1],x[i-2],y[i-2],y1[i-2],f,h)
        pass
    return x,y,y1
    pass

