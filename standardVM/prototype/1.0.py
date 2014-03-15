import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

class ScatterAnim(object):
    def __init__(self):
        self.N =100 #the number of the agents
        self.L = 7 #the size of the plane
        self.r = 1. #the interaction radius
        self.v = 0.03 #the velocity of the agents
        self.eta = 2.0
        self.fore = np.random.random((4,self.N))
        self.las = np.zeros((4,self.N))
        self.extra1 = np.zeros((4,self.N))
        self.extra2 = np.zeros((4,self.N))
        self.T = 0
        #give an initial configeration
        
        #give the initial posision
        self.fore[0,:] *= self.L
        self.fore[1,:] *= self.L
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0,self.L])
        self.ax.set_ylim([0,self.L])

        #give the initial direction
        for i in xrange(self.N):
            if random.random()>0.5:
                self.fore[2,i] = - self.fore[2,i]
            if random.random()<0.5:
                self.fore[3,i] = - self.fore[3,i]
	
        #renormolazition
        self.denominator = np.sqrt(self.fore[2,:]**2 + self.fore[3,:]**2)
        self.fore[2,:] /=self.denominator
        self.fore[3,:] /=self.denominator
        
        self.ani = animation.FuncAnimation(self.fig,self.update_scatt,interval =10,init_func = self.setup_plot,blit=True)
        
        


    def setup_plot(self):
        self.scat = self.ax.scatter(self.fore[0,:],self.fore[1,:],c='r',animated=True)
        return self.scat,

###############################


    def update_scatt(self,k):
        
        print time.clock() - self.T
        self.T = time.clock()

        #the periodic boundary
        self.extra1[:2,:]=-10
        self.extra2[:2,:]=-10
        self.extra1[2:,:]=0
        self.extra2[2:,:]=0
        for i in xrange(self.N):
            if self.fore[0,i]<self.r and self.fore[1,i]<self.r:
                self.extra2[0,i] = self.fore[0,i] + self.L
                self.extra2[1,i] = self.fore[1,i] + self.L
                self.extra2[2,i] = self.fore[2,i]
                self.extra2[3,i] = self.fore[3,i]
            
            if self.fore[0,i]<self.r and self.fore[1,i]>(self.L-self.r):
                self.extra2[0,i] = self.fore[0,i] + self.L
                self.extra2[1,i] = self.fore[1,i] - self.L
                self.extra2[2,i] = self.fore[2,i]
                self.extra2[3,i] = self.fore[3,i]
                
            if self.fore[0,i]>(self.L-self.r) and self.fore[1,i]<self.r:
                self.extra2[0,i] = self.fore[0,i] - self.L
                self.extra2[1,i] = self.fore[1,i] + self.L
                self.extra2[2,i] = self.fore[2,i]
                self.extra2[3,i] = self.fore[3,i]
                
            if self.fore[0,i]>(self.L-self.r) and self.fore[1,i]>(self.L-self.r):
                self.extra2[0,i] = self.fore[0,i] - self.L
                self.extra2[1,i] = self.fore[1,i] - self.L
                self.extra2[2,i] = self.fore[2,i]
                self.extra2[3,i] = self.fore[3,i]
                
            if self.fore[0,i]<self.r :
                self.extra1[0,i] = self.fore[0,i] + self.L
                self.extra1[1,i] = self.fore[1,i]
                self.extra1[2,i] = self.fore[2,i]
                self.extra1[3,i] = self.fore[3,i]
            
            if self.fore[1,i]<self.r:
                self.extra1[0,i] = self.fore[0,i]
                self.extra1[1,i] = self.fore[1,i] + self.L
                self.extra1[2,i] = self.fore[2,i]
                self.extra1[3,i] = self.fore[3,i]

            if self.fore[0,i]>(self.L-self.r):
                self.extra1[0,i] = self.fore[0,i] - self.L
                self.extra1[1,i] = self.fore[1,i]
                self.extra1[2,i] = self.fore[2,i]
                self.extra1[3,i] = self.fore[3,i]
                
            if self.fore[1,i]>(self.L-self.r):
                self.extra1[0,i] = self.fore[0,i]
                self.extra1[1,i] = self.fore[1,i] - self.L
                self.extra1[2,i] = self.fore[2,i]
                self.extra1[3,i] = self.fore[3,i] 
            ##############################
            
            #the simulation
        self.las[0,:] = self.fore[0,:] + self.v*self.fore[2,:]
        self.las[1,:] = self.fore[1,:] + self.v*self.fore[3,:]
            
            #the periodic boundary
        for i in xrange(self.N):
            if self.las[0,i]>self.L:
                self.las[0,i] = self.las[0,i]-self.L
            if self.las[0,i]<0:
                self.las[0,i] = self.las[0,i]+self.L
            if self.las[1,i]>self.L:
                self.las[1,i] = self.las[1,i]-self.L
            if self.las[1,i]<0:
                self.las[1,i] = self.las[1,i]+self.L
        ###########################
            
        #the direction
            
        self.las[2:,:] = 0
            
        for i in xrange(self.N):
            for j in xrange(self.N):
                self.distance = np.sqrt((self.fore[0,i]-self.fore[0,j])**2+(self.fore[1,i]-self.fore[1,j])**2)
                if self.distance<self.r:
                    self.las[2,i] = self.las[2,i]+self.fore[2,j]
                    self.las[3,i] = self.las[3,i]+self.fore[3,j]
                        
                self.distance = np.sqrt((self.fore[0,i]-self.extra1[0,j])**2+(self.fore[1,i]-self.extra1[1,j])**2)
                if self.distance<self.r:
                    self.las[2,i] = self.las[2,i]+self.extra1[2,j]
                    self.las[3,i] = self.las[3,i]+self.extra1[3,j]
                        
                self.distance = np.sqrt((self.fore[0,i]-self.extra2[0,j])**2+(self.fore[1,i]-self.extra2[1,j])**2)
                if self.distance<self.r:
                    self.las[2,i] = self.las[2,i]+self.extra2[2,j]
                    self.las[3,i] = self.las[3,i]+self.extra2[3,j]
                        
        self.denominator = np.sqrt(self.las[2,:]**2 + self.las[3,:]**2)
        self.las[2,:] /=self.denominator
        self.las[3,:] /=self.denominator
        
        #the perturbation
        self.ran = np.random.random((2,self.N))
        
        self.theta1 = self.ran[0,:]*self.eta-self.eta/2.
        self.theta2 = self.ran[1,:]*self.eta-self.eta/2.
        
        self.sintemp = np.copy(self.las[2,:])
        self.costemp = np.copy(self.las[3,:])
        
        self.las[2,:] = self.sintemp*np.cos(self.theta1)+self.costemp*np.sin(self.theta1)
        self.las[3,:] = self.costemp*np.cos(self.theta2)-self.sintemp*np.sin(self.theta2)
        #######################
            
        self.fore = np.copy(self.las)
            
        self.scat = self.ax.scatter(self.las[0,:],self.las[1,:],animated=True)
            
            
        return self.scat,
        
#    def showplot(self):
#            plt.show()
            

a = ScatterAnim()

plt.show()

