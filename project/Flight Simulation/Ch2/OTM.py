import modsim as ms
import matplotlib.pyplot as plt
import numpy as np

m=ms.UNITS.meter
s=ms.UNITS.second
g=9.8*m/s**2

class OTM:
    global m,s,g
    #x斜抛运动中各个方向运动存在耦合，不能单纯地用运动分解处理

    def __init__(self,x0=0,y0=0,V0=1,theta=np.pi/4,drag_k=0,t=5,dt=0.1):
        vx0=V0*np.cos(theta)
        vy0=V0*np.sin(theta)
        init=ms.State(x=x0*m,y=y0*m,vx=vx0*m/s,vy=vy0*m/s)
        self.init=init
        self.sys=ms.System(init=init,g=g,theta=theta,k=drag_k/m,t_end=t,dt=dt)
        self.run_simulation()
        pass

    def iter_func(self,state):
        g,k,dt=self.sys.g,self.sys.k,self.sys.dt
        Vx=state.vx
        Vy=state.vy
        X=state.x
        Y=state.y
        vx0=int(Vx*s/m)
        vy0=int(Vy*s/m)
        V=np.sqrt(vx0**2+vy0**2)*m/s
        Vx_next=Vx-k*Vx*V*dt*s
        Vy_next=Vy-(g+k*Vy*V)*dt*s
        X_next=X+Vx*dt*s
        Y_next=Y+Vy*dt*s
        State_next=ms.State(x=X_next,y=Y_next,vx=Vx_next,vy=Vy_next)
        return State_next
        pass

    def run_simulation(self):
        frame=ms.TimeFrame(columns=self.init.index)
        frame.row[0]=self.init
        ts=ms.linrange(0,self.sys.t_end,self.sys.dt)
        for ti in ts:
            frame.row[ti+self.sys.dt]=self.iter_func(frame.row[ti])
            pass
        self.frame=frame
        self.x_end=ms.get_last_value(self.frame.x)
        self.y_end=ms.get_last_value(self.frame.y)
        self.vx_end=ms.get_last_value(self.frame.vx)
        self.vy_end=ms.get_last_value(self.frame.vy)
        pass

    def Show_xy_t(self):
        ms.plot(self.frame.x,label='x-t')
        ms.plot(self.frame.y,label='y-t')
        ms.decorate(xlabel='Time(s)',ylabel='Length(m)')
        plt.grid(True)
        plt.show()
        pass

    def Show_Vxy_t(self):
        ms.plot(self.frame.vx,label='$V_x$-t')
        ms.plot(self.frame.vy,label='$V_y$-t')
        ms.decorate(xlabel='Time(s)',ylabel='Speed(m/s)')
        plt.grid(True)
        plt.show()
        pass

    def Show_position(self):
        ms.plot(self.frame.x,self.frame.y,label='x-y')
        ms.decorate(xlabel='x/m',ylabel='y/m')
        plt.grid(True)
        plt.show()