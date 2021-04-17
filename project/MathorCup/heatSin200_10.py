import numpy as np
from matplotlib import pyplot as plt
import math

#仿真尺寸
L,l = 14,12  # 图的大长，小长
R,r = 1.5,0.5  # 图的大径，小径
d = 0.1  # 分度长度
M,N = int(L/d),int(2*R/d) #横纵切块数
m,n=int(l/d),int(2*r/d) #横纵切块
dt = 100 #仿真时序步长
tfinal=600
step=int(tfinal/dt)

#一些参数设置
Vtotal = l*np.pi*r**2 #总体积
S = 2*np.pi*r*l+2*np.pi*r**2 #总面积
k,c,rho = 0.6,4200,1000  #水传热系数，比热，密度
ka,ca,rhoa=0.023,1005,1.293
K = k/c/rho #折合传热系数
v = 10#洋流速度
h = 44.45e-3 #高
b = 482.6e-3#宽
a = 525e-3 #长
V0 = a*b*h #小体积
Q = 500 #发热量
q = Q/V0 #单位体积发热量
qs0 = q/c/rho #折合发热量
Number = math.floor(Vtotal/V0) #小盒子数量
Number=200
qs = Number*V0/Vtotal*qs0 #总折合发热量
T0 = 273.15 #绝对零度
Tenv=20
Tin=50

def edge(j,i):
    j+=1
    i+=1
    if (M-m)/2<j<(M+m)/2 and (N-n)/2<i<(N+n)/2:
        return 'in'
    elif ((j==(M-m)/2 or j==(M+m)/2) and (N-n)/2<=i<=(N+n)/2):
        return 'on-updown'
    elif ((i==(N-n)/2 or i==(N+n)/2) and  (M-m)/2<=j<=(M+m)/2):
        return 'on-side'
    elif i<(N-n)/2 or i>(N+n)/2:
        return 'side'
    else:
        return 'updown'
    pass

def next_ji(j,i,Tnow):
    Tji = Tnow[j][i]
    Tji1 = Tnow[j-1][i]
    Tji2 = Tnow[j+1][i]
    Tji3 = Tnow[j][i-1]
    Tji4 = Tnow[j][i+1]
    T22=(Tji1+Tji2+Tji3+Tji4-4*Tji)/d**2
    Tz_ = np.abs((Tji2-Tji1)/2/d)
    rho_a=rhoa*T0/Tji
    Ka=ka/ca/rho_a
    if edge(j,i) =='in':
        Tji_next=Tji+dt*(Ka*T22+qs)
        pass
    elif edge(j,i)=='side':
        Tji_next=Tji+dt*(K*T22-v*Tz_/c/rho)
        pass
    elif edge(j,i)=='on-side':
        Tji_next=Tji+dt*(Ka*T22+qs-v*Tz_/c/rho)
        pass
    elif edge(j,i)=='on-updown':
        Tji_next=Tji+dt*(Ka*T22+qs)
        pass
    else:
        Tji_next=Tji+dt*(K*T22+0)
        pass
    return Tji_next
    pass

def next_T(Tnow):
    T_next=np.zeros([M,N])+Tenv+T0
    for j in range(1,M-1):
        for i in range(1,N-1):
            T_next[j][i]=next_ji(j,i,Tnow)
            pass
        pass
    return T_next
    pass

def get_T_init():
    T_init = np.zeros([M,N])
    for j in range(M):
        for i in range(N):
            if edge(j,i) in ['in','on-updown','onside']:
                T_init[j][i]=Tin+T0
                pass
            else:
                T_init[j][i]=Tenv+T0
            pass
        pass
    return T_init