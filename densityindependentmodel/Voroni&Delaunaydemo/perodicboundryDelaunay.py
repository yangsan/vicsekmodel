import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay 

points = [] #create an empty list to store the points

l = 10
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0,l])
ax.set_ylim([0,l])

def click(event): #the function to run everytime click the plane
    global ax,points,l    #use global vars to pass the data
    ax.cla()    #clean the old axe before draw the new ones
    ax.set_xlim([0,l])
    ax.set_ylim([0,l])
    
    points.append([event.xdata,event.ydata])    #put the location of your click into the list
    

    pointsarray = np.asarray(points)    #convert the list into ndarray
    p = np.zeros((9,len(pointsarray),2))
    #the perodic boundry
    p[0,:,0] = pointsarray[:,0] - l
    p[0,:,1] = pointsarray[:,1] + l

    p[1,:,0] = pointsarray[:,0]
    p[1,:,1] = pointsarray[:,1] + l
    
    p[2,:,0] = pointsarray[:,0] + l
    p[2,:,1] = pointsarray[:,1] + l
    
    p[3,:,0] = pointsarray[:,0] - l
    p[3,:,1] = pointsarray[:,1]
    
    p[4,:,0] = pointsarray[:,0]
    p[4,:,1] = pointsarray[:,1]
    
    p[5,:,0] = pointsarray[:,0] + l
    p[5,:,1] = pointsarray[:,1]
    
    p[6,:,0] = pointsarray[:,0] - l
    p[6,:,1] = pointsarray[:,1] - l
    
    p[7,:,0] = pointsarray[:,0]
    p[7,:,1] = pointsarray[:,1] - l
    
    p[8,:,0] = pointsarray[:,0] + l
    p[8,:,1] = pointsarray[:,1] - l
    
    p = p.reshape(9*len(pointsarray),2)
    tri = Delaunay(p)
    #draw the triangles
    ax.triplot(p[:,0],p[:,1],tri.simplices)
    ax.plot(p[:,0],p[:,1],'ro')    #mark every point
    ax.figure.canvas.draw()    #redraw the canvas everytime you click

#connect the event with the eventhandler    
cid = fig.canvas.mpl_connect('button_press_event',click)

plt.show()

