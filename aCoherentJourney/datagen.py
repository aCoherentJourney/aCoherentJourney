import random 
import numpy as np

inputFilePath = "./../data/input/"
outputFilePath = "./../data/output/"
Ndat = 50



def UniformRandDataGen(x):
    dataRnd = np.random.random([x,3])
    return dataRnd

def ExpRandDataGen(x,y):
    dataRnd = np.exp(-np.random.random([x,3])/y)
    return dataRnd

def orderDataGen(x):
    dataOrd = np.random.random([x,3])
    for i in range(x):
        dataOrd[i,0] = 1.
        dataOrd[i,1] = ( 440 * 2**((i%36)/12) - 50) / (15000-50)
        dataOrd[i,2] = i/50.
    return dataOrd


data = ExpRandDataGen(Ndat,0.1)
np.savetxt(inputFilePath + 'testData4.csv',data, fmt = "%.5f", delimiter=",")
