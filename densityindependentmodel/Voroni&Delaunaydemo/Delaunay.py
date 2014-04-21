import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


class DrawDelaunay(object):
    def __init__(self):
        self.points = []  # create an empty list to store the points
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])
        # connect the event with the eventhandler
        self.cid = self.fig.canvas.mpl_connect('button_press_event',
                                               self.click)

    def click(self, event):  # the function to run everytime click the plane
        self.ax.cla()  # clean the old axe to draw the new ones
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

        self.points.append([event.xdata, event.ydata])
        # put the location of your click into the list
        pointsarray = np.asarray(self.points)
        #convert the list into ndarray
        if len(self.points) >= 3:
            #the Delaunay diagram needs at least three points to work
            tri = Delaunay(pointsarray)
            #draw the triangles
            self.ax.triplot(pointsarray[:, 0], pointsarray[:, 1],
                            tri.simplices)

        self.ax.plot(pointsarray[:, 0], pointsarray[:, 1], 'ro')
        # mark every point

        self.ax.figure.canvas.draw()  # redraw the canvas everytime you click


if __name__ == "__main__":
    draw = DrawDelaunay()
    plt.show()
