Demos of density independent models/密度无关的模型演示
============================

In the standard Vicsek Model, the density of agents is an important parameter which will affect the behaviour of the system greatly. But some field researches showed that this maybe not true and the agents only assume the n(for example, 6) nearest neighbors` avarage velocity at each time step so densiy became irrelevant. 

#The 1.0 version model

According to the assumption here we have an density independent Vicsek model modification 1.0 version. But as you can find in the demo, in the simulation, the system can not reach a consensus. What`s more? Individuals would form dense clusters and only interact with individuals within the cluster. Interaction between clusters happens rarely when two cluster collide. The behaviour is easy to understood: individuals within the same cluster become each other`s n nearest neighbors so they don`t need to interact with others outside the cluster.

In this case, the model can not descripe collective motion every well so more work need to be done here.

#The 2.0 version model

As some researchers suggested, maybe we should  define the nearest neighbors topologically rather than in metric distance.

The way to define the neighbors topologically is to use Voronoi diagram. Wikipedia shows:

> In mathematics, a Voronoi diagram is a way of dividing space into a number of regions. A set of points (called seeds, sites, or generators) is specified beforehand and for each seed there will be a corresponding region consisting of all points closer to that seed than to any other. The regions are called Voronoi cells.

In this case, every agent(a point or a generator) is associated with a region, so an agents are those who are associated with the adjacent regions. 

In simulation, it`s more practical to use Delaunay triangulation to find the neighbors, and it`s dual to Voronoi diagram.

#Delaunay triangulation

As the wikipedia shows:

>In mathematics and computational geometry, a Delaunay triangulation for a set P of points in a plane is a triangulation DT(P) such that no point in P is inside the circumcircle of any triangle in DT(P). Delaunay triangulations maximize the minimum angle of all the angles of the triangles in the triangulation; they tend to avoid skinny triangles.

I wrote demos for both of Voronoi dagram and Delaunay triagulation individually and a demo to show them at the same time.

In the demos, you can click in the canvas and according the point you click it will show the diagram.
