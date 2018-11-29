import csv
#from pydub import audio_segment
import matplotlib.pyplot as plt
from scipy import fftpack

from aCoherentJourney.dataInput import *
from aCoherentJourney.dataProcessing import *
#from aCoherentJourney.soundSynthesis import *
from aCoherentJourney.soundOutput import *
from config import *

### Run ###
###################################################################


print(".wav files generated!")

getInputData(inputFilePathFile(inputFile))
scaleDur(1,inputFilePathFile(inputFile))
convertLinData(1,0,1)
convertLogData(1,0,1)
freq2NotesConverter(1)
freq2MajorConverter(1)
freq2MinorConverter(1)
createSawWave(1, 1, 1, outputFilePathFile("TestTestSaw"))
createSineWave(1, 1, 1, outputFilePathFile("TestTestSine"))
#blackBodySoundGenerator(1, 1, 1, "TestTestBlackBody")
createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("TestSound"), "major", "sadsa")
createTimeline(inputFilePathFile(inputFile), outputFilePathFile("TestTimeline"))
