# -*- coding: utf-8 -*-

'''标准Vicsek模型的模拟部分，入：4*N的ndarray类型的数组，前两行为坐标，
后两行为方向。出为下一步的模拟结果其余参数需要从外部进行调用'''

__author__ = "Kevin Young"

import numpy as np


#该函数只用来迭代，进去一个fore，出来一个las
#@profile
def simulation(fore, N, L, eta):

    r = 1.
    v = 0.03

    #the periodic boundary
    extra1 = np.zeros((4, N))
    extra2 = np.zeros((4, N))
    extra1[:2, :] = -10
    extra2[:2, :] = -10

    las = np.zeros((4, N))
#To deal with the periodic boundary,
#copy the agents on the corner of the area
#so I can compare the distance between these agents with the choosen one
#in next step. The same goes to the codes below.
    judge1 = np.logical_and(fore[0, :] < r, fore[1, :] < r)
    extra2[:2, :] = np.where(judge1, fore[:2, :] + L, extra2[:2, :])
    extra2[2:, :] = np.where(judge1, fore[2:, :], extra2[2:, :])

    judge2 = np.logical_and(fore[0, :] < r, fore[1, :] > (L - r))
    extra2[0, :] = np.where(judge2, fore[0, :] + L, extra2[0, :])
    extra2[1, :] = np.where(judge2, fore[1, :] - L, extra2[1, :])
    extra2[2:, :] = np.where(judge2, fore[2:, :], extra2[2:, :])

    judge3 = np.logical_and(fore[0, :] > (L - r), fore[1, :] < r)
    extra2[0, :] = np.where(judge3, fore[0, :] - L, extra2[0, :])
    extra2[1, :] = np.where(judge3, fore[1, :] + L, extra2[1, :])
    extra2[2:, :] = np.where(judge3, fore[2:, :], extra2[2:, :])

    judge4 = np.logical_and(fore[0, :] > (L - r), fore[1, :] > (L - r))
    extra2[:2, :] = np.where(judge4, fore[:2, :] - L, extra2[:2, :])
    extra2[2:, :] = np.where(judge4, fore[2:, :], extra2[2:, :])

    judge5 = fore[0, :] < r
    extra1[0, :] = np.where(judge5, fore[0, :] + L, extra1[0, :])
    extra1[1:, :] = np.where(judge5, fore[1:, :], extra1[1:, :])

    judge6 = fore[1, :] < r
    extra1[0, :] = np.where(judge6, fore[0, :], extra1[0, :])
    extra1[1, :] = np.where(judge6, fore[1, :] + L, extra1[1, :])
    extra1[2:, :] = np.where(judge6, fore[2:, :], extra1[2:, :])

    judge7 = fore[0, :] > (L - r)
    extra1[0, :] = np.where(judge7, fore[0, :] - L, extra1[0, :])
    extra1[1:, :] = np.where(judge7, fore[1:, :], extra1[1:, :])

    judge8 = fore[1, :] > (L - r)
    extra1[0, :] = np.where(judge8, fore[0, :], extra1[0, :])
    extra1[1, :] = np.where(judge8, fore[1, :] - L, extra1[1, :])
    extra1[2:, :] = np.where(judge8, fore[2:, :], extra1[2:, :])

        ##############################
    #the simulation
    #move the agents
    las[0, :] = fore[0, :] + v * fore[2, :]
    las[1, :] = fore[1, :] + v * fore[3, :]

    #the periodic boundary, move the agents who go out of the area back.
    las[:2, :] = np.where(las[:2, :] > L, las[:2, :] - L, las[:2, :])
    las[:2, :] = np.where(las[:2, :] < 0, las[:2, :] + L, las[:2, :])

    ###########################

    #the direction

    las[2:, :] = dis(fore, fore, r)
    las[2:, :] += dis(fore, extra1, r)
    las[2:, :] += dis(fore, extra2, r)

    denominator = np.sqrt(las[2, :] ** 2 + las[3, :] ** 2)
    las[2:, :] /= denominator

    #the perturbation
    ran = np.random.random((2, N))

    theta1 = ran[0, :] * eta - eta / 2.
    theta2 = ran[1, :] * eta - eta / 2.

    sintemp = np.copy(las[2, :])
    costemp = np.copy(las[3, :])

    las[2, :] = sintemp * np.cos(theta1) + costemp * np.sin(theta1)
    las[3, :] = costemp * np.cos(theta1) - sintemp * np.sin(theta1)
    #######################

    #fore = np.copy(las)
    return las

#@profile
def dis(fore, extra, r):
    N = fore.shape[1]
    las = np.zeros((2, N))
    square = np.sqrt((fore[0, :] - extra[0, :].reshape(N, 1)) ** 2
                     + (fore[1, :] - extra[1, :].reshape(N, 1)) ** 2)
    squarex = np.where((square < r), fore[2, :], 0)
    squarey = np.where((square < r), fore[3, :], 0)
    las[0, :] = squarex.sum(1)
    las[1, :] = squarey.sum(1)
    return las


if __name__ == "__main__":

    import time

    N = 10  # the number of the agents
    L = 15  # the size of the area the simulation is carried out
    r = 1.  # the interaction radius
    v = 0.03  # the absolute velocity of the agents
    eta = 1.0  # the noise

    #to store the x,y cordinates and the directions of every agents
    fore = np.random.random((4, N))
    ran = np.random.random((2, N))  # two list of random numbers
    zero = np.zeros(N)

    #give an initial configeration

    #give the initial posision
    fore[0, :] *= L
    fore[1, :] *= L

    #give the initial direction, the directions should be random
    fore[2, :] = np.where(ran[0, :] > 0.5, - fore[2, :], fore[2, :])
    fore[3, :] = np.where(ran[1, :] > 0.5, - fore[3, :], fore[3, :])

    #renormolazitionk
    denominator = np.sqrt(fore[2, :] ** 2 + fore[3, :] ** 2)
    fore[2, :] /= denominator
    fore[3, :] /= denominator

    start = time.time()
    for i in xrange(10):
        #filename = "%i.out" % i
        #np.savetxt(filename, fore[:, :].T)
        bench = time.time()
        fore = simulation(fore, N, L, eta)
        print "bench %i time: %f" % (i, (time.time() - bench))
    print "Exacating time: %f" % (time.time() - start)
