# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi


class DrawVoronoi(object):
    def __init__(self):
        self.points = []  # create an empty list to store the points
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        #connect the event with the eventhandler
        self.cid = self.fig.canvas.mpl_connect('button_press_event',
                                               self.click)

    def click(self, event):
        #the function to run everytime click the plane
        self.ax.cla()  # clean the old axe to draw the new ones
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

        self.points.append([event.xdata, event.ydata])
        # put the location of your click into the list
        pointsarray = np.asarray(self.points)
        # convert the list into ndarray
        if len(self.points) >= 3:
            # the Delaunay diagram needs at least three points to work
            tri = Voronoi(pointsarray)
            #draw the triangles
            voronoi_plot_2d(tri, self.ax)

        self.ax.plot(pointsarray[:, 0], pointsarray[:, 1], 'ro')
        #mark every point
        self.ax.figure.canvas.draw()
        #redraw the canvas everytime you click


#the source code from scipy.spatial.Voronoi, to plot the voronoi diagram
def voronoi_plot_2d(vor,  ax=None):
    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    ax.plot(vor.points[:, 0],  vor.points[:, 1],  '.')
#    ax.plot(vor.vertices[:, 0],  vor.vertices[:, 1],  'o')

    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(vor.vertices[simplex, 0],  vor.vertices[simplex, 1], 'k-')

    ptp_bound = vor.points.ptp(axis=0)

    center = vor.points.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0]
            # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            ax.plot([vor.vertices[i, 0],  far_point[0]],
                    [vor.vertices[i, 1], far_point[1]], 'k')

    return ax.figure


if __name__ == "__main__":
    vor = DrawVoronoi()
    plt.show()
