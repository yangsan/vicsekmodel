import os
from ConfigParser import SafeConfigParser
import numpy as np

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
        etapath = Npath + "/eta=%f" % eta
        os.makedirs(etapath)
        os.chdir(etapath)
        conf = SafeConfigParser()
        conf.add_section('p')
        conf.set('p', 'N', str(N))
        conf.set('p', 'eta', str(eta))
        conf.set('p', 'L', '15')
        conf.write(open('parameter.conf', 'w'))
        for i in xrange(10):
            filename = "%i.out" % i
            f = open(filename, "w")
