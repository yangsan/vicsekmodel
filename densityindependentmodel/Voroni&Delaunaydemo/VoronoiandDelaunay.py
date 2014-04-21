# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay, Voronoi


class DelVor(object):
    def __init__(self):
        self.points = []  # create an empty list to store the points
        self.fig = plt.figure(figsize=(16, 8))
        self.ax1 = self.fig.add_subplot(121)
        self.ax1.set_title('Voronoi Diagram')
        self.ax2 = self.fig.add_subplot(122)
        self.ax2.set_title('Delaunay Triangulation')
        self.ax1.set_xlim([0, 10])
        self.ax1.set_ylim([0, 10])
        self.ax2.set_xlim([0, 10])
        self.ax2.set_ylim([0, 10])
        # connect the event with the eventhandler
        self.cid = self.fig.canvas.mpl_connect('button_press_event',
                                               self.click)

    def click(self, event):  # the function to run everytime click the plane
        self.ax1.cla()    # clean the old axe to draw the new ones
        self.ax2.cla()
        self.ax1.set_xlim([0, 10])  # to draw the Voronoi diagram
        self.ax1.set_ylim([0, 10])
        self.ax2.set_xlim([0, 10])  # to draw the Delaunay tris
        self.ax2.set_ylim([0, 10])
        self.ax1.set_title('Voronoi Diagram')
        self.ax2.set_title('Delaunay Triangulation')
        self.points.append([event.xdata, event.ydata])
        # put the location of your click into the list
        pointsarray = np.asarray(self.points)
        # convert the list into ndarray
        if len(self.points) >= 3:
            # the Delaunay diagram needs at least three points to work
            vor = Voronoi(pointsarray)
            voronoi_plot_2d(vor, self.ax1)
            dela = Delaunay(pointsarray)
            self.ax2.triplot(pointsarray[:, 0],
                             pointsarray[:, 1], dela.simplices)

        self.ax1.plot(pointsarray[:, 0], pointsarray[:, 1], 'ro')
        # mark every point
        self.ax2.plot(pointsarray[:, 0], pointsarray[:, 1], 'ro')

        self.ax1.figure.canvas.draw()
        # redraw the canvas everytime you click
        self.ax2.figure.canvas.draw()


def voronoi_plot_2d(vor, ax=None):
    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")
    ax.plot(vor.points[:, 0], vor.points[:, 1],  '.')
#    ax.plot(vor.vertices[:, 0],  vor.vertices[:, 1],  'o')
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(vor.vertices[simplex, 0], vor.vertices[simplex, 1], 'k-')
    ptp_bound = vor.points.ptp(axis=0)
    center = vor.points.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]
            # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])
            # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            ax.plot([vor.vertices[i, 0],  far_point[0]],
                    [vor.vertices[i, 1],  far_point[1]], 'k')
    return ax.figure


if __name__ == "__main__":
    delvor = DelVor()
    plt.show()
