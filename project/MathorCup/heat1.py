import numpy as np
from matplotlib import pyplot as plt
import math

L,l = 30,12  # 图的大长，小长
R,r = 3,0.5  # 图的大径，小径
d = 0.1  # 分度长度
M,N = int(L/d),int(2*R/d) #横纵切块书
m,n=int(l/d),int(2*r/d) #横纵切块
Vtotal = l*np.pi*r**2 #总体积
S = 2*np.pi*r*l+2*np.pi*r**2 #总面积
k,c,rho = 0.6,4200,1000  #水传热系数，比热，密度
K = k/c/rho #折合传热系数
v = 0.1 #洋流速度
dt = 1 #仿真时序步长
tfinal=600
step=int(tfinal/dt)
h = 44.45e-3 #高
b = 482.6e-3#宽
a = 525e-3 #长
V0 = a*b*h #小体积
Q = 500 #发热量
q = Q/(h*b*a) #单位体积发热量
qs0 = q/c/rho #折合发热量
Number = math.floor(Vtotal/V0) #小盒子数量
qs = Number*V0/Vtotal * qs0 #总折合发热量
T0 = 273.15 #绝对零度
Tenv=20
Tin=50

def edge(j,i):
    j+=1
    i+=1
    if (M-m)/2<j<(M+m)/2 and (N-n)/2<i<(N+n)/2:
        return 'in'
    elif ((j==(M-m)/2 or j==(M+m)/2) and (N-n)/2<=i<=(N+n)/2)\
        or ((i==(N-n)/2 or i==(N+n)/2) and  (M-m)/2<=j<=(M+m)/2):
        return 'on'
    elif i<(N-n)/2 or i>(N+n)/2:
        return 'side'
    else:
        return 'out'
    pass

def next_ji(j,i,Tnow):
    if edge(j,i) =='in':
        Tji = Tnow[j][i]
        Tji1 = Tnow[j-1][i]
        Tji2 = Tnow[j+1][i]
        Tji3 = Tnow[j][i-1]
        Tji4 = Tnow[j][i+1]
        T22=(Tji1+Tji2+Tji3+Tji4-4*Tji)/d**2
        Tz_ = (Tji2-Tji1)/2/d
        Tji_next=Tji+dt*(K*T22+qs)
        return Tji_next
    elif j==0 or j==M-1 or i==0 or i==N-1:
        return Tenv+T0
    elif edge(j,i)=='side':
        pass
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