import numpy as np
def LifeGame2(mat):
    [m,n]=mat.shape
    mat_next=np.zeros([m,n])
    mat_expand=np.zeros([m+2,n+2])
    mat_expand[0]=np.concatenate((np.array([mat[-1][-1]]),mat[-1],np.array([mat[-1][0]])))
    mat_expand[-1]=np.concatenate((np.array([mat[0][-1]]),mat[0],np.array([mat[0][0]])))
    for j in range(m):
        mat_expand[j+1]=np.concatenate((np.array([mat[j][-1]]),mat[j],np.array([mat[j][0]])))
        pass
    for j in range(m):
        for i in range(n):
            value_ji=mat_expand[j+1][i+1]
            value=mat_expand[j][i]+mat_expand[j][i+1]+mat_expand[j][i+2]\
                +mat_expand[j+1][i]+mat_expand[j+1][i+2]\
                    +mat_expand[j+2][i]+mat_expand[j+2][i+1]+mat_expand[j+2][i+2]
            if value==2:
                mat_next[j][i]=value_ji
                pass
            elif value==3:
                mat_next[j][i]=1
                pass
            else:
                mat_next[j][i]=0
                pass
            pass
        pass
    return mat_next
    pass

import random as rd
import matplotlib.pyplot as plt
init=np.zeros([100,100])
[m,n]=init.shape
for j in range(m):
    for i in range(n):
        init[j][i]=rd.randint(0,1)
        pass
    pass
Final=1000
plt.figure()
for i in range(Final):
    plt.imshow(init)
    plt.pause(0.1)
    plt.cla()
    init=LifeGame2(init)
    pass