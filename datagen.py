import random 
import numpy as np

outputFilePath = "./data/input/"

Ndat = 95*2**0

data = np.zeros([Ndat,3])

def RhythmicRandDataGen(x):
    dataRnd = np.random.randint(64,size = x)
    dataRnd = dataRnd/64
    return dataRnd

def UniformRandDataGen(x):
    dataRnd = np.random.random(x)
    return dataRnd

def ExpRandDataGen(x,y):
    dataRnd = np.exp(-np.random.random(x)**2/y)
    return dataRnd

def OrderDataGen(x):
    dataOrd = np.arange(x)/x
    return dataOrd

def ConstDataGen(x, soundDurationRel):
    dataConst = np.ones(x)# * soundDurationRel
    return dataConst

decayStrength = 0.01
soundDurationRel = 0.1
time = UniformRandDataGen(Ndat)
#time = RhythmicRandDataGen(Ndat)
#time = OrderDataGen(Ndat)
freq = UniformRandDataGen(Ndat)
#freq = ( 440 * 2**( (OrderDataGen(Ndat)) * 5 - 2) ) / 7040 
vol = 1 - freq
#vol =  np.sqrt( abs( -np.log(freq) * decayStrength) ) 
duration = ConstDataGen(Ndat, soundDurationRel)
#duration = UniformRandDataGen(Ndat)
data = np.array([vol, freq, time, duration])
data = np.transpose(data)
#print(data)
np.savetxt(outputFilePath + 'testData4.csv', data, fmt = "%.5f", delimiter=",")
