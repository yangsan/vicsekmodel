import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


class DrawDelaunay(object):
    def __init__(self):
        self.points = []  # create an empty list to store the points
        self.l = 10
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, self.l])
        self.ax.set_ylim([0, self.l])
        #connect the event with the eventhandler
        self.cid = self.fig.canvas.mpl_connect('button_press_event',
                                               self.click)

    def click(self, event):  # the function to run everytime click the plane
        self.ax.cla()  # clean the old axe before draw the new ones
        self.ax.set_xlim([0, self.l])
        self.ax.set_ylim([0, self.l])

        self.points.append([event.xdata, event.ydata])
        # put the location of your click into the list

        pointsarray = np.asarray(self.points)
        #convert the list into ndarray
        p = np.zeros((9, len(pointsarray), 2))
        #the perodic boundry
        p[0, :, 0] = pointsarray[:, 0] - self.l
        p[0, :, 1] = pointsarray[:, 1] + self.l

        p[1, :, 0] = pointsarray[:, 0]
        p[1, :, 1] = pointsarray[:, 1] + self.l

        p[2, :, 0] = pointsarray[:, 0] + self.l
        p[2, :, 1] = pointsarray[:, 1] + self.l

        p[3, :, 0] = pointsarray[:, 0] - self.l
        p[3, :, 1] = pointsarray[:, 1]

        p[4, :, 0] = pointsarray[:, 0]
        p[4, :, 1] = pointsarray[:, 1]

        p[5, :, 0] = pointsarray[:, 0] + self.l
        p[5, :, 1] = pointsarray[:, 1]

        p[6, :, 0] = pointsarray[:, 0] - self.l
        p[6, :, 1] = pointsarray[:, 1] - self.l

        p[7, :, 0] = pointsarray[:, 0]
        p[7, :, 1] = pointsarray[:, 1] - self.l

        p[8, :, 0] = pointsarray[:, 0] + self.l
        p[8, :, 1] = pointsarray[:, 1] - self.l

        p = p.reshape(9 * len(pointsarray), 2)
        tri = Delaunay(p)
        #draw the triangles
        self.ax.triplot(p[:, 0], p[:, 1], tri.simplices)
        self.ax.plot(p[:, 0], p[:, 1], 'ro')    # mark every point
        self.ax.figure.canvas.draw()    # redraw the canvas everytime you click

if __name__ == "__main__":
    draw = DrawDelaunay()
    plt.show()
