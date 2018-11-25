import random 
import numpy as np

Ndat = 100

data = np.zeros([Ndat,3])

def UniformRandDataGen(x):
    dataRnd = np.random.random(x)
    return dataRnd

def ExpRandDataGen(x,y):
    dataRnd = np.exp(-np.random.random(x)**2/y)
    return dataRnd

def orderDataGen(x):
    dataOrd = np.random.random([x,3])
    for i in range(x):
        dataOrd[i,0] = 1.
        dataOrd[i,1] = ( 440 * 2**((i%36)/12) - 50 ) / (15000-50)
        dataOrd[i,2] = i/50.
    return dataOrd

decayStrength = 0.05
time = UniformRandDataGen(Ndat)
freq = ExpRandDataGen(Ndat,decayStrength)
vol = 1-freq
#print(freq,vol)
data = np.array([vol, freq, time])
data = np.transpose(data)
np.savetxt('testData4.csv',data, fmt = "%.5f", delimiter=",")
