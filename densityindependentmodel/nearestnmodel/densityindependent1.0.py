# -*- coding: utf-8 -*-
#This is simple demo for a simple denstiy independent Vicsek model. The only rule of the model: at each
#time step a given particle driven with a constant absolute velocity assumes the
#average direction of motion of the n nearest particels in its neiborhood with
#some random perturbation added.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



class ScatterAnim(object):
    def __init__(self):
        self.N =100 #the number of the agents
        self.L = 15 #the size of the area the simulation is carried out
#        self.r = 1. #the interaction radius
        self.v = 0.03 #the absolute velocity of the agents
        self.eta = 1.0 #the noise
        self.nc = 6 #the nearest nc neighbors

        self.fps=20

        self.pause = False
        self.t = 0

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
        self.fig1 = plt.figure(figsize = (8,16))
        self.ax1 = plt.subplot2grid((3,2),(1,0),colspan=2,rowspan=2) #where the simulation is carried out
        self.ax1.set_xlim([0,self.L])
        self.ax1.set_ylim([0,self.L])
        self.ax1.set_xlabel('Simulation')

        self.ax2 = plt.subplot2grid((3,2),(0,0),colspan=2) #show how the order parameter varies with time
        self.ax2.set_xlim([0,10])
        self.ax2.set_ylim([0,1.1])
        self.ax2.set_xlabel('Time',labelpad=-15)
        self.ax2.set_ylabel('$\phi$',fontsize=20)
        self.line, = self.ax2.plot([],[])

        self.cid = self.fig1.canvas.mpl_connect('button_press_event',self.click)

        #give the initial direction, the directions should be random
        self.fore[2,:] = np.where(self.ran[0,:]>0.5,-self.fore[2,:],self.fore[2,:])
        self.fore[3,:] = np.where(self.ran[1,:]>0.5,-self.fore[3,:],self.fore[3,:])


        #renormolazition
        self.denominator = np.sqrt(self.fore[2,:]**2 + self.fore[3,:]**2)
        self.fore[2,:] /=self.denominator
        self.fore[3,:] /=self.denominator

	#To do the animation
        self.ani1 = animation.FuncAnimation(self.fig1,self.update_scatt,interval =self.fps ,init_func = self.setup_plot,blit=True)

    def click(self,event):
        self.pause ^= True

    def setup_plot(self):
        self.scat = self.ax1.scatter(self.fore[0,:],self.fore[1,:],c='r',animated=True)
        return self.scat,


    #The core part of the simulation.
    def update_scatt(self,k):

        if not self.pause:

            #to simulate the perodic boundry, copy the pattern of all the agents and put them around the original one
            self.compare = np.zeros((9,2,self.N))
            self.compare[0,0,:] = self.fore[0,:]-self.L
            self.compare[0,1,:] = self.fore[1,:]+self.L

            self.compare[1,0,:] = self.fore[0,:]
            self.compare[1,1,:] = self.fore[1,:]+self.L

            self.compare[2,0,:] = self.fore[0,:]+self.L
            self.compare[2,1,:] = self.fore[1,:]+self.L

            self.compare[3,0,:] = self.fore[0,:]-self.L
            self.compare[3,1,:] = self.fore[1,:]

            self.compare[4,0,:] = self.fore[0,:]
            self.compare[4,1,:] = self.fore[1,:]

            self.compare[5,0,:] = self.fore[0,:]+self.L
            self.compare[5,1,:] = self.fore[1,:]

            self.compare[6,0,:] = self.fore[0,:]-self.L
            self.compare[6,1,:] = self.fore[1,:]-self.L

            self.compare[7,0,:] = self.fore[0,:]
            self.compare[7,1,:] = self.fore[1,:]-self.L

            self.compare[8,0,:] = self.fore[0,:]+self.L
            self.compare[8,1,:] = self.fore[1,:]-self.L


   	#the simulation

   	#move the agents
            self.las[0,:] = self.fore[0,:] + self.v*self.fore[2,:]
            self.las[1,:] = self.fore[1,:] + self.v*self.fore[3,:]

   	#the periodic boundary, move the agents who go out of the area back.
            self.las[:2,:] = np.where(self.las[:2,:]>self.L,self.las[:2,:]-self.L,self.las[:2,:])
            self.las[:2,:] = np.where(self.las[:2,:]<0,self.las[:2,:]+self.L,self.las[:2,:])


            #the direction
            self.las[2:,:] = 0

            #pick up an agent each time
            for i in xrange(self.N):
                #calculate the distance between the choosen one with all the others
                self.distance = np.sqrt((self.fore[0,i] - self.compare[:,0,:])**2+(self.fore[1,i] - self.compare[:,1,:])**2)
                #find the nearest one of all the copies
                self.distancemin = self.distance.min(axis=0)

                #sort the agents acording to the distance
                self.fx = self.fore[2,self.distancemin.argsort()]
                self.fy = self.fore[3,self.distancemin.argsort()]

                #only the nc nearest agents are needed
                self.las[2,i] = np.sum(self.fx[:self.nc])
                self.las[3,i] = np.sum(self.fy[:self.nc])

            self.denominator = np.sqrt(self.las[2,:]**2 + self.las[3,:]**2)
            self.las[2:,:] /=self.denominator



            #the perturbation
            self.ran = np.random.random((2,self.N))

            self.theta1 = self.ran[0,:]*self.eta-self.eta/2.
            self.theta2 = self.ran[1,:]*self.eta-self.eta/2.

            self.sintemp = np.copy(self.las[2,:])
            self.costemp = np.copy(self.las[3,:])

            self.las[2,:] = self.sintemp*np.cos(self.theta1)+self.costemp*np.sin(self.theta1)
            self.las[3,:] = self.costemp*np.cos(self.theta1)-self.sintemp*np.sin(self.theta1)




        #######################

            self.fore = np.copy(self.las)
	#calculate the sum velocity of all agents
            self.sumx = np.sum(self.las[2,:])/float(self.N)
            self.sumy = np.sum(self.las[3.:])/float(self.N)

            self.t += 1
            self.x=np.append(self.x,self.t*0.01)
            self.y=np.append(self.y,np.sqrt((self.sumx)**2+(self.sumy)**2))

            self.xmin, self.xmax = self.ax2.get_xlim()
            if self.t*0.01>self.xmax:
                self.ax2.set_xlim(self.xmin, 2*self.xmax)

        self.scat = self.ax1.scatter(self.las[0,:],self.las[1,:],animated=True)
        self.line.set_data(self.x,self.y)


        return self.scat,self.line,


a = ScatterAnim()

plt.show()

