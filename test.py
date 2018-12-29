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

"""getInputData(inputFilePathFile(inputFile))
scaleDur(1,inputFilePathFile(inputFile))
convertLinData(1,0,1)
convertLogData(1,0,1)
freq2NotesConverter(1)
freq2MajorConverter(1)
freq2MinorConverter(1)
createSawWave(1, 1, 1, outputFilePathFile("TestTestSaw"))
createSineWave(1, 1, 1, outputFilePathFile("TestTestSine"))
#blackBodySoundGenerator(1, 1, 1, "TestTestBlackBody")
createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("TestSound"), "major", "sine")
createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("TestSound"), "major", "saw")
createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("TestSound"), "major", "square")
createTimeline(inputFilePathFile(inputFile), outputFilePathFile("TestTimeline"))
"""
#createSineWave(3, 440, 3, outputFilePathFile("TestTestSine"))
#createSawWave(3, 440, 3, outputFilePathFile("TestTestSaw"))
#createSquareWave(3, 440, 3, outputFilePathFile("TestTestSquare"))
#createBlackBodyWave(3, 440, 3, outputFilePathFile("TestTestBackBody"))

#createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("BlackBodySounds"), "minor", "blackbody")
#createTimeline(inputFilePathFile(inputFile), outputFilePathFile("EMinorBlackBodyTimeline"))
#createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("BlackBodySounds"), "major", "blackbody")
#createTimeline(inputFilePathFile(inputFile), outputFilePathFile("EMajorBlackBodyTimeline"))
#createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("SineSounds"), "minor", "sine")
#createTimeline(inputFilePathFile(inputFile), outputFilePathFile("EMinorSineTimeline"))
#createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("SineSounds"), "major", "sine", "none", "", "")
#createTimeline(inputFilePathFile(inputFile), outputFilePathFile("EMajorSineTimeline"), "none", "", "")
#createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("BlackBodyRhythmSounds"), "major", "blackbody", bar, [1,3], division)
#createTimeline(inputFilePathFile(inputFile), outputFilePathFile("AMajorBlackBodyRhythmTimeline"), bar, [1,3], division)
#createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("BlackBodyRhythmSounds"), "minor", "blackbody", bar, [1,3], division)
#createTimeline(inputFilePathFile(inputFile), outputFilePathFile("AMinorBlackBodyRhythmTimelineNew"), bar, [1,3], division)
createSoundsFromFile(inputFilePathFile(inputFile), outputFilePathFile("BlackBodyRhythmSounds"), "mixolydian", "blackbody", bar, [1,3], division)
createTimeline(inputFilePathFile(inputFile), outputFilePathFile("GMixolydianBlackBodyRhythmTimelineNew"), bar, [0,2], division)

print(".wav files generated!")
