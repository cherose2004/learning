import numpy as np
#定义蚂蚁类
class ant:
    def __init__(self,x,y,dire):
        self.x=x
        self.y=y
        self.dire=dire
        pass
    def get_x(self):
        return self.x
        pass
    def get_y(self):
        return self.y
        pass
    def black(self):
        if self.dire=='U':
            self.dire='R'
            self.x=self.x+1
            pass
        elif self.dire=='R':
            self.dire='D'
            self.y=self.y+1
            pass
        elif self.dire=='D':
            self.dire='L'
            self.x=self.x-1
            pass
        elif self.dire=='L':
            self.dire='U'
            self.y=self.y-1
            pass
        pass
    def white(self):
        if self.dire=='U':
            self.dire='L'
            self.x=self.x-1
            pass
        elif self.dire=='L':
            self.dire='D'
            self.y=self.y+1
            pass
        elif self.dire=='D':
            self.dire='R'
            self.x=self.x+1
            pass
        elif self.dire=='R':
            self.dire='U'
            self.y=self.y-1
            pass
        pass
    def set_x(self,n):
        self.x=self.x%n
        pass
    def set_y(self,m):
        self.y=self.y%m
        pass
    pass
#定义运算
def LongtonsAnts(mat_cur,ant_cur):
    [m,n]=mat_cur.shape
    mat_next=mat_cur
    ant_next=ant_cur
    i=ant_next.get_x()
    j=ant_next.get_y()
    if mat_cur[j][i]==1:
        mat_next[j][i]=0
        ant_next.black()
        pass
    else:
        mat_next[j][i]=1
        ant_next.white()
        pass
    ant_next.set_x(n)
    ant_next.set_y(m)
    return mat_next,ant_next
    pass

#开始做可视化
import random as rd
import matplotlib.pyplot as plt
mat=np.zeros([50,50])
[m,n]=mat.shape
for j in range(m):
    for i in range(n):
        mat[j][i]=rd.randint(0,1)
        pass
    pass
x_init=rd.randint(0,n-1)
y_init=rd.randint(0,m-1)
list_dir=['U','R','D','L']
dir_init=list_dir[rd.randint(0,3)]
Ant=ant(x_init,y_init,dir_init)
Final=1000
plt.figure()
for i in range(Final):
    plt.imshow(mat,cmap=plt.cm.winter)
    plt.pause(0.01)
    plt.cla()
    mat,Ant=LongtonsAnts(mat,Ant)
    pass