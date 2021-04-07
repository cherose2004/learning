import numpy as np
import math
def RK4_iter(x,y,f,h=0.01):
    '''
    Used for iteration of Runge-Kutta method
    given current x,y
    f means the function in:
    y'=f(x,y)
    h means dx
    return next x and y
    '''
    k1=f(x,y)
    k2=f(x+h/2,y+k1/2*h)
    k3=f(x+h/2,y+k2*h/2)
    k4=f(x+h,y+k3*h)
    x_next=x+h
    y_next=y+h*(k1+2*k2+2*k3+k4)/6
    return x_next,y_next

def RK4(x0,y0,f,h=0.01,final=5):
    '''
    Used for RungeKutta method
    given x0 and y0
    f means the function in:
    y'=f(x,y)
    h means dx
    return a series x and y in array form
    '''
    n=math.floor(final/h)
    x=np.zeros(n)
    y=np.zeros(n)
    x[0],y[0]=x0,y0
    for i in range(1,n):
        x[i],y[i]=RK4_iter(x[i-1],y[i-1],f,h)
        pass
    return x,y