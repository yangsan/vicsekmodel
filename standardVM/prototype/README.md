#1.0 version

The 1.0 version was translated from fortran, so it may look not pythonic.

#2.0 version

The 2.0 version was trying to be more pythonic. I remove most of the for loops for sake of efficiency. The trick is to use Numpy verctorized functions as much as possible, which will also make the codes more readeble.

#3.0 version

In this version, I remove the animation parts, so I can run the simulation on cluster. I also make the simulation core into a function so it can be imported into other codes.

#1.0版

这个版是从更早时写的一个fortran程序翻译过来的，所以看上去并不是很pythonic。

#2.0版

为了使代码更pythonic一些，我重写了部分代码，尽可能地移除了for循环。这样做主要是希望提升运行效率，使用Numpy的向量化函数代替for循环不仅能提升运行效率，也使得代码更加易读。

#3.0版

这一版去掉了画图的部分，并且把模拟的核心摘出来写成了函数，这样可以在集群上运行这个脚本，也可以在其他代码中调用这个函数。
