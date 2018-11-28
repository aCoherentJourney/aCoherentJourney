import numpy as np
from numpy import trapz
import csv
import random
import os
from scipy.io.wavfile import write
from scipy import signal
from pydub import audio_segment
import matplotlib.pyplot as plt
from scipy import fftpack


### Run ###
###################################################################

inputFile = ("testData4.csv")
soundDurationRel = 0.2
totalDuration = 20
volMin = 0.5
volMax = 1
durMin = 0.5
durMax = scaleDur(totalDuration,inputFile)
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

#createSoundsFromFile(inputFile, "testSounds", "nomode")
#createTimeline(inputFile, "mixed")
#blackBodySoundGenerator(3, 440, 1, "testBlackbody")
createSoundsFromFile(inputFile, "testSaw", "saw")
print(".wav files generated!")
