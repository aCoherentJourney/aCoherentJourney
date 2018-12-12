import numpy as np
#from aCoherentJourney.dataProcessing import *
from config import *


inputFilePath = "./data/input/"
outputFilePath = "./data/output/"
inputFile = ("testData4")
#inputFile = ("testData5")
#soundDurationRel = 0.1
totalDuration = 20.208
timeAcc = 1000
bar = 4
nBars = 8
division = 2
#totalDuration = 4
beats = nBars * bar * division
durRelMin = 1 / beats
durRelMax = 8 / beats
volMin = 0.5
volMax = 1
freqMin = 55
freqMax = 14080/2
#reference frequency (adjusted via iterative halving if larger than maximum frequency)
freqRef_Hz = 440
while freqRef_Hz > freqMax:
    freqRef_Hz = freqRef_Hz / 2
while freqRef_Hz < freqMin:
    freqRef_Hz = freqRef_Hz * 2
#lowest root tone frequency (larger than minimum frequency)
rootFreqMin = freqRef_Hz / 2**int( np.log2(freqRef_Hz / freqMin))
#key of preferred scale
#freqKey_Hz = 196
freqKey_Hz = 329.628
#freqKey_Hz = 440
