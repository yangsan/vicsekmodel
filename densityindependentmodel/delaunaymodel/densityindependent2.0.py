# -*- coding: utf-8 -*-
#This is simple demo for a simple denstiy independent Vicsek model. The only rule of the model: at each
#time step a given particle driven with a constant absolute velocity assumes the
#average direction of motion of the neighbors in terms of Voronoi diagram  with
#some random perturbation added.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial import Delaunay



class ScatterAnim(object):
    def __init__(self):
        self.N =40 #the number of the agents
        self.L = 15 #the size of the area the simulation is carried out
#        self.r = 1. #the interaction radius
        self.v = 0.03 #the absolute velocity of the agents
        self.eta = 2.0 #the noise
        self.nc = 7 #the nearest nc neighbors

        self.fps=25

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

        #to simulate the perodic boundry, copy the pattern of all the agents and put them around the original one
        self.compare = np.zeros((9,2,self.N))
        self.compare[0,0,:] = self.fore[0,:]
        self.compare[0,1,:] = self.fore[1,:]

        self.compare[1,0,:] = self.fore[0,:]
        self.compare[1,1,:] = self.fore[1,:]+self.L

        self.compare[2,0,:] = self.fore[0,:]+self.L
        self.compare[2,1,:] = self.fore[1,:]+self.L

        self.compare[3,0,:] = self.fore[0,:]-self.L
        self.compare[3,1,:] = self.fore[1,:]

        self.compare[4,0,:] = self.fore[0,:]-self.L
        self.compare[4,1,:] = self.fore[1,:]+self.L

        self.compare[5,0,:] = self.fore[0,:]+self.L
        self.compare[5,1,:] = self.fore[1,:]

        self.compare[6,0,:] = self.fore[0,:]-self.L
        self.compare[6,1,:] = self.fore[1,:]-self.L

        self.compare[7,0,:] = self.fore[0,:]
        self.compare[7,1,:] = self.fore[1,:]-self.L

        self.compare[8,0,:] = self.fore[0,:]+self.L
        self.compare[8,1,:] = self.fore[1,:]-self.L


	#the simulation
        self.transposec = np.zeros((self.N*9,2))
	#move the agents
        self.las[0,:] = self.fore[0,:] + self.v*self.fore[2,:]
        self.las[1,:] = self.fore[1,:] + self.v*self.fore[3,:]

	#the periodic boundary, move the agents who go out of the area back.
        self.las[:2,:] = np.where(self.las[:2,:]>self.L,self.las[:2,:]-self.L,self.las[:2,:])
        self.las[:2,:] = np.where(self.las[:2,:]<0,self.las[:2,:]+self.L,self.las[:2,:])



        self.transposec[:,0] = self.compare[:,0,:].reshape(1,-1)
        self.transposec[:,1] = self.compare[:,1,:].reshape(1,-1)


        #the direction
	#use the Delauany package to find the neighbors of the chosen agent
        self.tri = Delaunay(self.transposec)


        self.las[2:,:] = 0

        for i in xrange(self.N):
            ineighber = np.array([]) #creat a empty array to store the neighors` cords
            for simplex in self.tri.simplices: #tri.simplices gives the indices of the points who form the Delaunay tris
                if i in simplex: #we only need the original pattern's neighbors
                    ineighber = np.append(ineighber,simplex)

            ineighber = np.unique(np.int32(ineighber))%self.N


            self.las[2,i] = np.sum(self.fore[2,ineighber])
            self.las[3,i] = np.sum(self.fore[3,ineighber])




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

