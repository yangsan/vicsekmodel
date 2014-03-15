# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class ScatterAnim(object):
    def __init__(self):

        self.fps = 20

        self.N = 10
        self.L = 15

        self.x=np.array([])
        self.y=np.array([])

        self.fig1 = plt.figure(figsize = (6,16))
        self.ax1 = plt.subplot2grid((3,2),(1,0),colspan=2,rowspan=2)
        self.ax1.set_xlim([0,self.L])
        self.ax1.set_ylim([0,self.L])
        self.ax1.set_xlabel('Simulation')

        self.ax2 = plt.subplot2grid((3,2),(0,0),colspan=2)
        self.ax2.set_xlim([0,10])
        self.ax2.set_ylim([0,1.1])
        self.ax2.set_xlabel('Time',labelpad=-15)
        self.ax2.set_ylabel('$\phi$',fontsize=20)
        self.line, = self.ax2.plot([],[])

        #To do the animation
        self.ani1 = animation.FuncAnimation(self.fig1,self.update_scatt,interval =self.fps ,init_func = self.setup_plot,blit=True)


    def setup_plot(self):
        firstframe = np.loadtxt("./data/0.out").T
        self.scat = self.ax1.scatter(firstframe[0,:],firstframe[1,:],c='r',animated=True)
        return self.scat,

	#The core part of the simulation.
    def update_scatt(self,k):

        filename = "./data/%i.out" % k
        frame = np.loadtxt(filename).T
	    #calculate the sum velocity of all agents
        self.sumx = np.sum(frame[2,:])/float(self.N)
        self.sumy = np.sum(frame[3.:])/float(self.N)

        self.x=np.append(self.x,k*0.01)
        self.y=np.append(self.y,np.sqrt((self.sumx)**2+(self.sumy)**2))

        self.xmin, self.xmax = self.ax2.get_xlim()
        if k*0.01>self.xmax:
            self.ax2.set_xlim(self.xmin, 2*self.xmax)

        self.scat = self.ax1.scatter(frame[0,:],frame[1,:],animated=True)
        self.line.set_data(self.x,self.y)


        return self.scat,self.line,


if __name__ == "__main__":
    a = ScatterAnim()
    plt.show()
