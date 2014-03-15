# -*- coding: utf-8 -*-

import numpy as np
import os
from ConfigParser import SafeConfigParser

i = 0

#在eta目录下，处理时间序列的部分
def timeseries():
    while True:
        filename = "./data/%i.out" % i
        if os.path.exists(filename):
            frame = np.loadtxt(filename).T
            #calculate the sum velocity of all agents
            sumx = np.sum(frame[2, :]) / float(N)
            sumy = np.sum(frame[3, :]) / float(N)
            i += 1
        else:
            break

#处理目录的部分

    beginningdir = os.getcwd()
    datapath = beginningdir + "/data"
    os.chdir(datapath)

    number = [40, 100, 400, 4000, 10000]

    for N in number:
        Npath = datapath + "/N=%i" % N
        os.chdir(Npath)
        dirlist = os.listdir(Npath)
        for eta in dirlist:

            etapath = Npath + eta
            os.chdir(etapath)
            conf = SafeConfigParser()

            conf.read('parameter.conf')
            eta = float(conf.get('p', 'eta'))
            n = int(conf.get('p', 'n'))

