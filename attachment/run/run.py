# -*- coding: utf-8 -*-

if __name__ == "__main__":

    import numpy as np
    from standardsimu import simulation
    import os
    from ConfigParser import SafeConfigParser
    from math import sqrt

    timestep = 10000

    beginningdir = os.getcwd()
    datapath = beginningdir + "/data"
    os.makedirs(datapath)
    os.chdir(datapath)

    number = [40, 100, 400, 4000, 10000]

    for N in number:
        Npath = datapath + "/N=%i" % N
        os.makedirs(Npath)
        os.chdir(Npath)
        for eta in np.linspace(0, 5., 100):

            rho = 4.
            L = sqrt(N / rho)# the size of the area the simulation is carried out

            etapath = Npath + "/eta=%f" % eta
            os.makedirs(etapath)
            os.chdir(etapath)
            conf = SafeConfigParser()
            conf.add_section('p')
            conf.set('p', 'N', str(N))
            conf.set('p', 'eta', str(eta))
            conf.set('p', 'L', str(L))
            conf.set('p', 'v', '0.03')
            conf.set('p', 'r', '1.')
            conf.set('p', 'rho', str(rho))
            conf.write(open('parameter.conf', 'w'))

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

            for i in xrange(timestep):
                filename = "%i.out" % i
                np.savetxt(filename, fore[:, :].T, fmt='%.4e')
                fore = simulation(fore, N, L, eta)
