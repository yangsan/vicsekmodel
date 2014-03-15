# -*- coding: utf-8 -*-
#This is simple demo for the Vicsek model. The only rule of the model: at each 
#time step a given particle driven with a constant absolute velocity assumes the#average direction of motion of the particels in its neiborhood of radius r with#some random perturbation added.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



class ScatterAnim(object):
    def __init__(self):
        self.N =100 #the number of the agents
        self.L = 15 #the size of the area the simulation is carried out
        self.r = 1. #the interaction radius
        self.v = 0.03 #the absolute velocity of the agents
        self.eta = 1.0 #the noise
        
        self.fps=10
        
        self.fore = np.random.random((4,self.N)) #to store the x,y cordinates and the directions of every agents
        self.las = np.zeros((4,self.N)) #the store the x,y cordinates and the directions of every agents after the update
        self.extra1 = np.zeros((4,self.N)) #for the agents on the corner of the area
        self.extra2 = np.zeros((4,self.N)) #for the agents on the edge of the area
        self.ran = np.random.random((2,self.N)) #two list of random numbers
        self.zero = np.zeros(self.N)
        
        self.x=np.array([])
        self.y=np.array([])
        
        #give an initial configeration
        
        #give the initial posision
        self.fore[0,:] *= self.L
        self.fore[1,:] *= self.L
       
	#set up the subplots 
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


        #give the initial direction, the directions should be random
        self.fore[2,:] = np.where(self.ran[0,:]>0.5,-self.fore[2,:],self.fore[2,:])
        self.fore[3,:] = np.where(self.ran[1,:]>0.5,-self.fore[3,:],self.fore[3,:])    
#        for i in xrange(self.N):
#            if random.random()>0.5:
#                self.fore[2,i] = - self.fore[2,i]
#            if random.random()<0.5:
#                self.fore[3,i] = - self.fore[3,i]


        #renormolazition
        self.denominator = np.sqrt(self.fore[2,:]**2 + self.fore[3,:]**2)
        self.fore[2,:] /=self.denominator
        self.fore[3,:] /=self.denominator
       
	#To do the animation 
        self.ani1 = animation.FuncAnimation(self.fig1,self.update_scatt,interval =self.fps ,init_func = self.setup_plot,blit=True)
        

    def setup_plot(self):
        self.scat = self.ax1.scatter(self.fore[0,:],self.fore[1,:],c='r',animated=True)
        return self.scat,


	#The core part of the simulation. 
    def update_scatt(self,k):

        #the periodic boundary
        self.extra1[:2,:]=-10
        self.extra2[:2,:]=-10
        self.extra1[2:,:]=0
        self.extra2[2:,:]=0

	#To deal with the periodic boundary, copy the agents on the corner of the area so I can compare the distance between these agents with the choosen one in next step. The same goes to the codes below.
        self.judge1 = np.logical_and(self.fore[0,:]<self.r,self.fore[1,:]<self.r)
        self.extra2[:2,:] = np.where(self.judge1, self.fore[:2,:] + self.L,self.extra2[:2,:])
        self.extra2[2:,:] = np.where(self.judge1, self.fore[2:,:] ,self.extra2[2:,:])
#        for i in xrange(self.N):
#            if self.fore[0,i]<self.r and self.fore[1,i]<self.r:
#                self.extra2[0,i] = self.fore[0,i] + self.L
#                self.extra2[1,i] = self.fore[1,i] + self.L
#                self.extra2[2,i] = self.fore[2,i]
#                self.extra2[3,i] = self.fore[3,i]
        self.judge2 = np.logical_and(self.fore[0,:]<self.r,self.fore[1,:]>(self.L-self.r))
        self.extra2[0,:] = np.where(self.judge2, self.fore[0,:] + self.L,self.extra2[0,:])
        self.extra2[1,:] = np.where(self.judge2, self.fore[1,:] - self.L,self.extra2[1,:])
        self.extra2[2:,:] = np.where(self.judge2, self.fore[2:,:] ,self.extra2[2:,:])  
                  
#            if self.fore[0,i]<self.r and self.fore[1,i]>(self.L-self.r):
#                self.extra2[0,i] = self.fore[0,i] + self.L
#                self.extra2[1,i] = self.fore[1,i] - self.L
#                self.extra2[2,i] = self.fore[2,i]
#                self.extra2[3,i] = self.fore[3,i]

        self.judge3 = np.logical_and(self.fore[0,:]>(self.L-self.r),self.fore[1,:]<self.r)
        self.extra2[0,:] = np.where(self.judge3, self.fore[0,:] - self.L,self.extra2[0,:])
        self.extra2[1,:] = np.where(self.judge3, self.fore[1,:] + self.L,self.extra2[1,:])
        self.extra2[2:,:] = np.where(self.judge3, self.fore[2:,:] ,self.extra2[2:,:])  
                       
#            if self.fore[0,i]>(self.L-self.r) and self.fore[1,i]<self.r:
#                self.extra2[0,i] = self.fore[0,i] - self.L
#                self.extra2[1,i] = self.fore[1,i] + self.L
#                self.extra2[2,i] = self.fore[2,i]
#                self.extra2[3,i] = self.fore[3,i]

        self.judge4 = np.logical_and(self.fore[0,:]>(self.L-self.r),self.fore[1,:]>(self.L-self.r))
        self.extra2[:2,:] = np.where(self.judge4, self.fore[:2,:] - self.L,self.extra2[:2,:])
        self.extra2[2:,:] = np.where(self.judge4, self.fore[2:,:] ,self.extra2[2:,:])   
                     
#            if self.fore[0,i]>(self.L-self.r) and self.fore[1,i]>(self.L-self.r):
#                self.extra2[0,i] = self.fore[0,i] - self.L
#                self.extra2[1,i] = self.fore[1,i] - self.L
#                self.extra2[2,i] = self.fore[2,i]
#                self.extra2[3,i] = self.fore[3,i]
        self.judge5 = self.fore[0,:]<self.r
        self.extra1[0,:] = np.where(self.judge5, self.fore[0,:] + self.L, self.extra1[0,:])
        self.extra1[1:,:] = np.where(self.judge5, self.fore[1:,:], self.extra1[1:,:])
                        
#            if self.fore[0,i]<self.r :
#                self.extra1[0,i] = self.fore[0,i] + self.L
#                self.extra1[1,i] = self.fore[1,i]
#                self.extra1[2,i] = self.fore[2,i]
#                self.extra1[3,i] = self.fore[3,i]

        self.judge6 = self.fore[1,:]<self.r
        self.extra1[0,:] = np.where(self.judge6, self.fore[0,:],self.extra1[0,:])
        self.extra1[1,:] = np.where(self.judge6, self.fore[1,:] + self.L , self.extra1[1,:])
        self.extra1[2:,:] = np.where(self.judge6, self.fore[2:,:],self.extra1[2:,:])
        
#            if self.fore[1,i]<self.r:
#                self.extra1[0,i] = self.fore[0,i]
#                self.extra1[1,i] = self.fore[1,i] + self.L
#                self.extra1[2,i] = self.fore[2,i]
#                self.extra1[3,i] = self.fore[3,i]
                
        self.judge7 = self.fore[0,:]>(self.L-self.r)
        self.extra1[0,:] = np.where(self.judge7, self.fore[0,:] - self.L,self.extra1[0,:])
        self.extra1[1:,:] = np.where(self.judge7, self.fore[1:,:],self.extra1[1:,:])
        
#            if self.fore[0,i]>(self.L-self.r):
#                self.extra1[0,i] = self.fore[0,i] - self.L
#                self.extra1[1,i] = self.fore[1,i]
#                self.extra1[2,i] = self.fore[2,i]
#                self.extra1[3,i] = self.fore[3,i]
        self.judge8 = self.fore[1,:]>(self.L-self.r)
        self.extra1[0,:] = np.where(self.judge8, self.fore[0,:],self.extra1[0,:])
        self.extra1[1,:] = np.where(self.judge8, self.fore[1,:] - self.L , self.extra1[1,:])
        self.extra1[2:,:] = np.where(self.judge8, self.fore[2:,:],self.extra1[2:,:])  
             
#            if self.fore[1,i]>(self.L-self.r):
#                self.extra1[0,i] = self.fore[0,i]
#                self.extra1[1,i] = self.fore[1,i] - self.L
#                self.extra1[2,i] = self.fore[2,i]
#                self.extra1[3,i] = self.fore[3,i] 
            ##############################
            
           


 
	#the simulation

	#move the agents
        self.las[0,:] = self.fore[0,:] + self.v*self.fore[2,:]
        self.las[1,:] = self.fore[1,:] + self.v*self.fore[3,:]
            
	#the periodic boundary, move the agents who go out of the area back.
        self.las[:2,:] = np.where(self.las[:2,:]>self.L,self.las[:2,:]-self.L,self.las[:2,:])
        self.las[:2,:] = np.where(self.las[:2,:]<0,self.las[:2,:]+self.L,self.las[:2,:])
        
#        for i in xrange(self.N):
#            if self.las[0,i]>self.L:
#                self.las[0,i] = self.las[0,i]-self.L
#            if self.las[0,i]<0:
#                self.las[0,i] = self.las[0,i]+self.L
#            if self.las[1,i]>self.L:
#                self.las[1,i] = self.las[1,i]-self.L
#            if self.las[1,i]<0:
#                self.las[1,i] = self.las[1,i]+self.L
        ###########################
            
        #the direction

        self.las[2:,:] = 0
                    
        for i in xrange(self.N):

            self.distance1 = np.sqrt((self.fore[0,i]-self.fore[0,:])**2+(self.fore[1,i]-self.fore[1,:])**2)
            self.las[2,i] += np.sum(np.where(self.distance1<self.r ,self.fore[2,:],self.zero))
            self.las[3,i] += np.sum(np.where(self.distance1<self.r ,self.fore[3,:],self.zero))

            self.distance2 = np.sqrt((self.fore[0,i]-self.extra1[0,:])**2+(self.fore[1,i]-self.extra1[1,:])**2)
            self.las[2,i] += np.sum(np.where(self.distance2<self.r ,self.extra1[2,:],self.zero))
            self.las[3,i] += np.sum(np.where(self.distance2<self.r ,self.extra1[3,:],self.zero))  
            
            self.distance3 = np.sqrt((self.fore[0,i]-self.extra2[0,:])**2+(self.fore[1,i]-self.extra2[1,:])**2)
            self.las[2,i] += np.sum(np.where(self.distance3<self.r ,self.extra2[2,:],self.zero))
            self.las[3,i] += np.sum(np.where(self.distance3<self.r ,self.extra2[3,:],self.zero)) 
           
            '''                    
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
           '''                     
        self.denominator = np.sqrt(self.las[2,:]**2 + self.las[3,:]**2)
        self.las[2:,:] /=self.denominator
        
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
	#calculate the sum velocity of all agents        
        self.sumx = np.sum(self.las[2,:])/float(self.N)
        self.sumy = np.sum(self.las[3.:])/float(self.N)
        
        self.x=np.append(self.x,k*0.01)
        self.y=np.append(self.y,np.sqrt((self.sumx)**2+(self.sumy)**2))
        
        self.xmin, self.xmax = self.ax2.get_xlim()
        if k*0.01>self.xmax:
            self.ax2.set_xlim(self.xmin, 2*self.xmax)
        
        self.scat = self.ax1.scatter(self.las[0,:],self.las[1,:],animated=True) 
        self.line.set_data(self.x,self.y)
          
        
        return self.scat,self.line,
        

a = ScatterAnim()

plt.show()

