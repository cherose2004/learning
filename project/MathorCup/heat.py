import numpy as np
from matplotlib import pyplot as plt
import math

L,l = 30,12  # m
R,r = 3,0.5  # m
d = 0.1  # step m
M,N = int(L/d),int(2*R/d)
m,n=int(l/d),int(2*r/d)
Vtotal = l*np.pi*r**2
S = 2*np.pi*r*l+2*np.pi*r**2
k,c,rho = 0.6,4200,1000  
K = k/c/rho
v = 1
dt = 10
h = 44.45e-3
b = 482.6e-3
a = 525e-3
V0 = a*b*h
Q = 500
q = Q/(h*b*a)
qs0 = q/c/rho
Number = math.floor(Vtotal/V0)
qs = Number*V0/S/d * qs0
T0 = 273.15

def edge(j,i):
    j+=1
    i+=1
    if (M-m)/2<j<(M+m)/2 and (N-n)/2<i<(N+n)/2:
        return 'in'
    elif ((j==(M-m)/2 or j==(M+m)/2) and (N-n)/2<=i<=(N+n)/2)\
        or ((i==(N-n)/2 or i==(N+n)/2) and  (M-m)/2<=j<=(M+m)/2):
        return 'on'
    else:
        return 'out'
    pass

def next_ji(j,i,Tnow):
    if edge(j,i) =='in':
        return 80+T0
    elif j==0 or j==M-1 or i==0 or i==N-1:
        return 20+T0
    else:
        Tji = Tnow[j][i]
        Tji1 = Tnow[j-1][i]
        Tji2 = Tnow[j+1][i]
        Tji3 = Tnow[j][i-1]
        Tji4 = Tnow[j][i+1]
        T22=(Tji1+Tji2+Tji3+Tji4-4*Tji)/d**2
        Tz_ = (Tji2-Tji1)/2/d
        if edge(j,i)=='on':
            qe = -v*Tz_ /c/rho+ qs
            pass
        else:
            qe=-v*Tz_/c/rho
            pass
        Tji_next=Tji + dt*(K * T22 +qe)
        return Tji_next
    pass

def next_T(Tnow):
    T_next=np.zeros([M,N])
    for j in range(M):
        for i in range(N):
            T_next[j][i]=next_ji(j,i,Tnow)
            pass
        pass
    return T_next
    pass