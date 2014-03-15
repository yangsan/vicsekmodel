import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay,Voronoi
points = [] #create an empty list to store the points

fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(121)
ax1.set_title('Voronoi Diagram')
ax2 = fig.add_subplot(122)
ax2.set_title('Delaunay Triangulation')
ax1.set_xlim([0,10])
ax1.set_ylim([0,10])
ax2.set_xlim([0,10])
ax2.set_ylim([0,10])

def click(event): #the function to run everytime click the plane
    global ax1,ax2,points    #use global vars to pass the data
    ax1.cla()    #clean the old axe to draw the new ones
    ax2.cla()
    ax1.set_xlim([0,10]) #to draw the Voronoi diagram
    ax1.set_ylim([0,10]) 
    ax2.set_xlim([0,10]) #to draw the Delaunay tris
    ax2.set_ylim([0,10])
    ax1.set_title('Voronoi Diagram')
    ax2.set_title('Delaunay Triangulation')
    points.append([event.xdata,event.ydata])    #put the location of your click into the list
    pointsarray = np.asarray(points)    #convert the list into ndarray
    if len(points)>=3:     #the Delaunay diagram needs at least three points to work     
        vor = Voronoi(pointsarray)
        voronoi_plot_2d(vor,ax1)
        dela = Delaunay(pointsarray)
        ax2.triplot(pointsarray[:,0],pointsarray[:,1],dela.simplices)

      
    ax1.plot(pointsarray[:,0],pointsarray[:,1],'ro')    #mark every point
    ax2.plot(pointsarray[:,0],pointsarray[:,1],'ro')

    ax1.figure.canvas.draw()    #redraw the canvas everytime you click
    ax2.figure.canvas.draw()


def voronoi_plot_2d(vor, ax=None):

    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    ax.plot(vor.points[:,0], vor.points[:,1], '.')
#    ax.plot(vor.vertices[:,0], vor.vertices[:,1], 'o')

    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(vor.vertices[simplex,0], vor.vertices[simplex,1], 'k-')

    ptp_bound = vor.points.ptp(axis=0)

    center = vor.points.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0] # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]]) # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            ax.plot([vor.vertices[i,0], far_point[0]], 
                    [vor.vertices[i,1], far_point[1]], 'k')



    return ax.figure

#connect the event with the eventhandler    
cid = fig.canvas.mpl_connect('button_press_event',click)

plt.show()

