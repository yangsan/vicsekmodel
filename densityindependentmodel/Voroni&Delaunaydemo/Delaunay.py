import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay 

points = [] #create an empty list to store the points

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0,10])
ax.set_ylim([0,10])

def click(event): #the function to run everytime click the plane
    global ax,points    #use global vars to pass the data
    ax.cla()    #clean the old axe to draw the new ones
    ax.set_xlim([0,10])
    ax.set_ylim([0,10])
    
    points.append([event.xdata,event.ydata])    #put the location of your click into the list
    pointsarray = np.asarray(points)    #convert the list into ndarray
    if len(points)>=3:     #the Delaunay diagram needs at least three points to work     
        tri = Delaunay(pointsarray)
        #draw the triangles
        ax.triplot(pointsarray[:,0],pointsarray[:,1],tri.simplices)
        
        
            
    ax.plot(pointsarray[:,0],pointsarray[:,1],'ro')    #mark every point
    
    

    
    ax.figure.canvas.draw()    #redraw the canvas everytime you click

#connect the event with the eventhandler    
cid = fig.canvas.mpl_connect('button_press_event',click)

plt.show()

