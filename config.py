import numpy as np
#from aCoherentJourney.dataProcessing import *
from config import *


inputFilePath = "./data/input/"
outputFilePath = "./data/output/"
inputFile = ("testData4")
#inputFile = ("testData5")
#soundDurationRel = 0.1
#totalDuration = 20.208
bpm = 90
#17.9439252
#totalDuration = 20.208
timeAcc = 1000
bar = 4
nBars = 4
division = 0.5
totalDuration = 60. / bpm * bar * nBars
beats = nBars * bar * division
durRelMinBass = 2 / beats
durRelMaxBass = 16 / beats
durRelMinMid = 0.25 / beats
durRelMaxMid = 0.25 / beats
durRelMinHigh = 0.25 / beats
durRelMaxHigh = 16 / beats
durRelMin = durRelMinHigh
durRelMax = durRelMaxHigh
#durRelMin = totalDuration
#durRelMax = totalDuration
volMin = 0.5
volMax = 1
freqMin = 440 * 2 ** (-3)
freqMax = 440 * 2 ** (2)
#freqMax = 14080/2
#reference frequency (adjusted via iterative halving if larger than maximum frequency)
freqRef_Hz = 440
while freqRef_Hz > freqMax:
    freqRef_Hz = freqRef_Hz / 2
while freqRef_Hz < freqMin:
    freqRef_Hz = freqRef_Hz * 2
#lowest root tone frequency (larger than minimum frequency)
rootFreqMin = freqRef_Hz / 2**int( np.log2(freqRef_Hz / freqMin))
#key of preferred scale
#freqKey_Hz = 392.00
#freqKey_Hz = 329.628
#freqKey_Hz = 440
freqKey_Hz = 261.63
