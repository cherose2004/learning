import modsim as ms
import numpy as np
import matplotlib.pyplot as plt

class Liquid:
    def __init__(self,T0,r,volume,T_env=22,t0=0,tf=5,dt=0.1,name='some liquid'):
        self.init=ms.State(T=T0)
        self.name=name
        self.system=ms.System(
            init=self.init,
            V=volume,
            r=r,
            T_env=T_env,
            t0=t0,
            t_end=tf,
            dt=dt
            )
        self.run_simulation()
        pass

    def iter_func(self,state):
        r,T_env,dt=self.system.r,self.system.T_env,self.system.dt
        T=state.T
        T_next=T-r*(T-T_env)*dt
        return ms.State(T=T_next)
        pass

    def run_simulation(self):
        frame=ms.TimeFrame(columns=self.init.index)
        frame.row[self.system.t0]=self.init
        ts=ms.linrange(self.system.t0,self.system.t_end,self.system.dt)
        for ti in ts:
            frame.row[ti+self.system.dt]=self.iter_func(frame.row[ti])
            pass
        self.frame=frame
        self.T_end=ms.get_last_value(self.frame.T)
        pass

    def show(self):
        ms.plot(self.frame.T,label=self.name)
        ms.decorate(xlabel='Time (minutes)',ylabel='Temperature (C)')
        plt.grid(True)
        plt.show()
        pass

    def mix(self,Liquid2,after=True,left_time=30,new_name='mixture'):
        v1=self.system.V
        v2=Liquid2.system.V
        if after!=True:
            T10=ms.get_first_value(self.system.init)
            T20=ms.get_first_value(Liquid2.system.init)
            pass
        else:
            T10=self.T_end
            T20=Liquid2.T_end
        v=v1+v2
        T0=(T10*v1+T20*v2)/v
        new=Liquid(T0,self.system.r,v,self.system.T_env,\
            self.system.t0,left_time,self.system.dt,\
                new_name)
        return new
    pass