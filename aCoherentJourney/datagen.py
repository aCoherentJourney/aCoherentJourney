import random 
import numpy as np

Ndat = 50

def randDataGen(x):
    data = np.random.random([x,3])
    return data


def orderDataGen(x):
    for i in range(x):
        data[i,0] = 1.
        data[i,1] = ( 440 * 2**((i%36)/12) - 50) / (15000-50)
        data[i,2] = i/50.
    return data


randDataGen(Ndat)
np.savetxt('testData4.csv',data, fmt = "%.5f", delimiter=",")
