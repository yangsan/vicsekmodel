import numpy as np
from scipy.spatial.distance import cdist

@profile
def old(fore, r):
    N = fore.shape[1]
    las = np.zeros((2, N))
    for i in xrange(N):
        distance = np.sqrt((fore[0, i] - fore[0, :]) ** 2 + (fore[1, i] - fore[1, :]) ** 2)
        las[0, i] += np.sum(np.where(distance < r, fore[2, :], 0))
        las[1, i] += np.sum(np.where(distance < r, fore[3, :], 0))

    return las


@profile
def new(fore, r):
    N = fore.shape[1]
    las = np.zeros((2, N))
    square = np.sqrt((fore[0, :] - fore[0, :].reshape(N, 1))**2
                     + (fore[1, :] - fore[1, :].reshape(N, 1))**2)
    #print (square < r)
    #print square
    #print fore[0, :]
    squarej = np.where((square < r), fore[2, :], 0)
    squarey = np.where((square < r), fore[3, :], 0)
    #print squarej
    #print squarej.sum(1)
    las[0, :] = squarej.sum(1)
    las[1, :] = squarey.sum(1)
    return las

@profile
def scipy(fore, r):
    N = fore.shape[1]
    las = np.zeros((2, N))
    cor = fore[:2, :].T
    square = cdist(cor, cor)

    squarej = np.where((square < r), fore[2, :], 0)
    squarey = np.where((square < r), fore[3, :], 0)
    #print squarej
    #print squarej.sum(1)
    las[0, :] = squarej.sum(1)
    las[1, :] = squarey.sum(1)
    return las


if __name__ == "__main__":
    r = 0.2
    fore = np.random.random((4, 5))
    print old(fore, r)
    print new(fore ,r)
    print scipy(fore, r)
