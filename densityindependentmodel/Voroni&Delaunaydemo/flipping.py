import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay 


points = [[5.,9.],[1.5,4.7],[8.2,5.3]] #create an list to store the points

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlim([0,10])
ax.set_ylim([0,10])


origin = np.asarray(points)
ax.plot(origin[:,0],origin[:,1],'ro')
ax.text(5.,9.5,'B',fontsize = 20)
#ax.text(4.8,8.2,r'$\beta$',fontsize=20)
ax.text(8.7,5.3,'A',fontsize = 20)
#ax.text(7.6,5.,r'$\alpha$',fontsize=20)
ax.text(1.,4.7,'C',fontsize = 20)
#ax.text(1.8,4.7,r'$\gamma$',fontsize=20)


####################
def dot2(u, v):
    return u[0]*v[0] + u[1]*v[1]

def cross2(u, v, w):
    """u x (v x w)"""
    return dot2(u, w)*v - dot2(u, v)*w

def ncross2(u, v):
    """|| u x v ||^2"""
    return sq2(u)*sq2(v) - dot2(u, v)**2

def sq2(u):
    return dot2(u, u)
#######################

def findcenter(tri):
   
    A = tri[0,:].T
    B = tri[1,:].T
    C = tri[2,:].T

    a = A - C
    b = B - C
    
    cc = cross2(sq2(a) * b - sq2(b) * a, a, b) / (2*ncross2(a, b)) + C 
    
    r = np.sqrt(sq2(a))*np.sqrt(sq2(b))*np.sqrt(sq2(a - b)) / (2*np.sqrt(ncross2(a,b)))
        
    return (cc[0],cc[1]),r
        
def radiant(a,b,c):
    aa = np.asarray(a)
    bb = np.asarray(b)
    cc = np.asarray(c)
    

    A = aa-cc

    B = bb-cc

    cos = dot2(A,B)/(np.sqrt(sq2(A))*np.sqrt(sq2(B)))

    return np.degrees(np.arccos(cos))

     
def click(event): #the function to run everytime click the plane
    global ax,points    #use global vars to pass the data
    ax.cla()    #clean the old axe to draw the new ones
    ax.set_xlim([0,10])
    ax.set_ylim([0,10])
    
    origin = list(points)
    
    point = [event.xdata,event.ydata]

    origin.append(point)
     
    pointsarray = np.asarray(origin)

    
    
    tri = Delaunay(pointsarray)

    ax.triplot(pointsarray[:,0],pointsarray[:,1],tri.simplices)
        
    p = tri.points[tri.simplices]
    
    center1,r1 = findcenter(p[0])
    center2,r2 = findcenter(p[-1])
    
    
    circ1 = plt.Circle(center1,radius = r1,fill = False,)
    ax.add_patch(circ1)
    
    circ2 = plt.Circle(center2,radius = r2,fill = False,)
    ax.add_patch(circ2)
    
    beta = radiant([8.2,5.3],[1.5,4.7],[5.,9.])
    alpha = radiant([5.,9.],point,[8.2,5.3])
    gamma = radiant([5.,9.],point,[1.5,4.7])
    delta = radiant([8.2,5.3],[1.5,4.7],point)
    
    ax.plot(pointsarray[:,0],pointsarray[:,1],'ro')    #mark every point
    ax.text(5.,9.5,'B',fontsize = 20)
    ax.text(4.8,8.2,r'$\beta$',fontsize=20)
    ax.text(8.7,5.3,'A',fontsize = 20)
    ax.text(7.6,5.,r'$\alpha$',fontsize=20)
    ax.text(1.,4.7,'C',fontsize = 20)
    ax.text(1.8,4.7,r'$\gamma$',fontsize=20)
    ax.text(point[0]-0.1,point[1]-0.7,'D',fontsize= 20)
    ax.text(point[0],point[1]+0.5,r'$\delta$',fontsize = 20)
    
    ax.text(6.5,9.5,r'$\alpha + \gamma$ = %.2f$^\circ$'%(alpha+gamma),fontsize = 20)
    ax.text(6.5,8.5,r'$\beta + \delta$ = %.2f$^\circ$'%(beta + delta),fontsize = 20)

    ax.figure.canvas.draw()    #redraw the canvas everytime you click

#connect the event with the eventhandler    
cid = fig.canvas.mpl_connect('button_press_event',click)

plt.show()
