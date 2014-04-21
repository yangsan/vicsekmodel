# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


class Flipping(object):
    def __init__(self):
        self.points = [[5., 9.], [1.5, 4.7], [8.2, 5.3]]
        # create an list to store the points
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

        self.origin = np.asarray(self.points)
        self.ax.plot(self.origin[:, 0], self.origin[:, 1], 'ro')
        self.ax.text(5., 9.5, 'B', fontsize=20)
        #ax.text(4.8, 8.2, r'$\beta$', fontsize=20)
        self.ax.text(8.7, 5.3, 'A', fontsize=20)
        #self.ax.text(7.6, 5., r'$\alpha$', fontsize=20)
        self.ax.text(1., 4.7, 'C', fontsize=20)
        #self.ax.text(1.8, 4.7, r'$\gamma$', fontsize=20)
        #connect the event with the eventhandler
        self.cid = self.fig.canvas.mpl_connect('button_press_event',
                                               self.click)

    def click(self, event):
        # the function to run everytime click the plane
        self.ax.cla()  # clean the old axe to draw the new ones
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([0, 10])

        self.origin = self.points[:]

        point = [event.xdata, event.ydata]

        self.origin.append(point)

        pointsarray = np.asarray(self.origin)

        tri = Delaunay(pointsarray)

        self.ax.triplot(pointsarray[:, 0], pointsarray[:, 1], tri.simplices)

        p = tri.points[tri.simplices]

        center1, r1 = findcenter(p[0])
        center2, r2 = findcenter(p[-1])

        circ1 = plt.Circle(center1, radius=r1, fill=False, )
        self.ax.add_patch(circ1)

        circ2 = plt.Circle(center2, radius=r2, fill=False, )
        self.ax.add_patch(circ2)

        beta = radiant([8.2, 5.3], [1.5, 4.7], [5., 9.])
        alpha = radiant([5., 9.], point, [8.2, 5.3])
        gamma = radiant([5., 9.], point, [1.5, 4.7])
        delta = radiant([8.2, 5.3], [1.5, 4.7], point)

        self.ax.plot(pointsarray[:, 0], pointsarray[:, 1], 'ro')
        #mark every point
        self.ax.text(5., 9.5, 'B', fontsize=20)
        self.ax.text(4.8, 8.2, r'$\beta$', fontsize=20)
        self.ax.text(8.7, 5.3, 'A', fontsize=20)
        self.ax.text(7.6, 5., r'$\alpha$', fontsize=20)
        self.ax.text(1., 4.7, 'C', fontsize=20)
        self.ax.text(1.8, 4.7, r'$\gamma$', fontsize=20)
        self.ax.text(point[0] - 0.1, point[1] - 0.7, 'D', fontsize=20)
        self.ax.text(point[0], point[1] + 0.5, r'$\delta$', fontsize=20)

        self.ax.text(6.5, 9.5,
                     r'$\alpha + \gamma$ = %.2f$^\circ$' % (alpha + gamma),
                     fontsize=20)
        self.ax.text(6.5, 8.5,
                     r'$\beta + \delta$ = %.2f$^\circ$' % (beta + delta),
                     fontsize=20)

        self.ax.figure.canvas.draw()  # redraw the canvas everytime you click


####################
def dot2(u, v):
    """
    点乘
    """
    return u[0] * v[0] + u[1] * v[1]


def cross2(u, v, w):
    """u x (v x w)"""
    return dot2(u, w) * v - dot2(u, v) * w


def ncross2(u, v):
    """|| u x v ||^2"""
    return sq2(u) * sq2(v) - dot2(u, v) ** 2


def sq2(u):
    return dot2(u, u)
#######################


def findcenter(tri):
    A = tri[0, :].T
    B = tri[1, :].T
    C = tri[2, :].T
    a = A - C
    b = B - C
    cc = cross2(sq2(a) * b - sq2(b) * a, a, b) / (2 * ncross2(a, b)) + C

    r = np.sqrt(sq2(a)) * np.sqrt(sq2(b)) * np.sqrt(sq2(a - b)) /\
        (2 * np.sqrt(ncross2(a, b)))

    return (cc[0], cc[1]), r


def radiant(a, b, c):
    aa = np.asarray(a)
    bb = np.asarray(b)
    cc = np.asarray(c)

    A = aa - cc
    B = bb - cc

    cos = dot2(A, B) / (np.sqrt(sq2(A)) * np.sqrt(sq2(B)))

    return np.degrees(np.arccos(cos))

if __name__ == "__main__":
    print "Hello world"
    flip = Flipping()
    plt.show()
