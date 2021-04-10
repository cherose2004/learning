import numpy as np
a=input().split()
a=[int(item) for item in a]
n=a[0]
m=a[1]
hx=a[2]+2
hy=a[3]+2
Map=np.zeros([m+5,n+5])
Weight=1+Map
for j in [-1,1]:
    for i in [-1,1]:
        Weight[hy+2*j][hx+i]=0
        Weight[hy+j][hx+2*i]=0
        pass
    pass
Weight[hy][hx]=0
Map[2][3],Map[3][2]=1*Weight[2][3],1*Weight[3][2]
for i in range(4,n+3):
    Map[2][i]=Map[2][i-1]*Weight[2][i-1]
    pass
for j in range(4,m+3):
    Map[j][2]=Map[j-1][2]*Weight[j-1][2]
    pass
for j in range(3,m+3):
    for i in range(3,n+3):
        Map[j][i]=Map[j-1][i]*Weight[j-1][i]+Map[j][i-1]*Weight[j][i-1]
        pass
    pass
print(int(Map[m+2][n+2]))