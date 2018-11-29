import numpy as np
#from aCoherentJourney.dataProcessing import *
from config import *


inputFilePath = "./data/input/"
outputFilePath = "./data/output/"
inputFile = ("testData4")
soundDurationRel = 0.2
totalDuration = 20
durMin = 0.5
durMax = 1
volMin = 0.5
volMax = 1
freqMin = 55
freqMax = 14080/2
#reference frequency (adjusted via iterative halving if larger than maximum frequency)
freqRef_hz = 440
while freqRef_hz > freqMax:
    freqRef_hz = freqRef_hz / 2
while freqRef_hz < freqMin:
    freqRef_hz = freqRef_hz * 2
#lowest root tone frequency (larger than minimum frequency)
rootFreqMin = freqRef_hz / 2**int( np.log2(freqRef_hz / freqMin))
#key of preferred scale
freqKey_hz = 196
