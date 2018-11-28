import random 
import numpy as np

outputFilePath = "./../data/input/"

Ndat = 100

data = np.zeros([Ndat,3])

def UniformRandDataGen(x):
    dataRnd = np.random.random(x)
    return dataRnd

def ExpRandDataGen(x,y):
    dataRnd = np.exp(-np.random.random(x)**2/y)
    return dataRnd

def OrderDataGen(x):
    dataOrd = np.arange(x)/x
    return dataOrd

decayStrength = 0.1
#time = UniformRandDataGen(Ndat)
time = OrderDataGen(Ndat)
#freq = ExpRandDataGen(Ndat,decayStrength)
freq = ( 440 * 2**( (OrderDataGen(Ndat)) * 5 - 2) ) / 7040 
vol = 1 - freq
#vol =  np.sqrt( abs( -np.log(freq) * decayStrength) ) 
#print(freq,vol)
data = np.array([vol, freq, time])
data = np.transpose(data)
np.savetxt(outputFilePath + 'testData4.csv',data, fmt = "%.5f", delimiter=",")
