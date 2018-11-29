from config import *
from aCoherentJourney.dataProcessing import *
from aCoherentJourney.soundSynthesis import *
from aCoherentJourney.soundOutput import *
import os

dct = {} # Create dictionary in order to iteratively declare names for variables/parameters/...


### Define output file including path
def outputFilePathFile(outputFile):
    return outputFilePath + outputFile + ".wav"


### Creates sine with decay from data file, with first column in he data file corresponds to the volume and the second to the frequency of the sound
def createSoundsFromFile(inputFile, outputFile, mode, sound):
    data = getInputData(inputFile)
    index = outputFile.find(".wav")
    for i in range(len(data)):
        # Duration of sine wave in s
        durMax = scaleDur(totalDuration,inputFile)
        dur = soundDurationRel*durMax
        # Volume (scaled to predetermined range)
        vol = convertLinData(data[i,0], volMax, volMin)
        # Frequency (scaled to predetermined range) and converted to notes from major scale
        # Create saw wave
        if mode == "major":
            freq = freq2MajorConverter(convertLinData(data[i,1], freqMax, freqMin))
        if mode == "minor":
            freq = freq2MinorConverter(convertLinData(data[i,1], freqMax, freqMin))
        if mode == "nomode":
            #freq = freq2MajorConverter(convertLinData(data[i,1], freqMax, freqMin))
            freq = freq2NotesConverter(convertLinData(data[i,1], freqMax, freqMin))
        else:
            freq = convertLinData(data[i,1], freqMax, freqMin)
        # Create saw wave if requested
        if sound == "saw":
            createSawWave(dur, freq, vol, outputFile + str(i+1))
        # Else create sine wave
        else:
            createSineWave(dur, freq, vol, outputFile + str(i+1))
        dct['audio_%s' % int(i)] = AudioSegment.from_file(outputFile + str(i+1))
        # Introduce decay
        silence = AudioSegment.silent(duration = 1000 * dur)
        dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silence, crossfade = 999 * dur)
        dct['audio_%s' % int(i)].export(outputFile + str(i+1), format='wav')
        # Remove file to save space
        os.remove(outputFile + str(int(i+1)))


### Creates sound timeline of (decaying) sine waves, where the starting of each sine wave is taken from the third column of the data
def createTimeline(inputFile, outputFile):
    data = getInputData(inputFile)
    for i in range(len(data)):
        # Duration of sound in s
        durMax = scaleDur(totalDuration,inputFile)
        soundDuration = soundDurationRel*durMax
        # Duration of silence in s before sine wave starts taken from data
        silenceDuration = durMax*data[i,2]
        # Create silent sound of durations of the silence before sound
        silence = AudioSegment.silent(duration = 1000 * silenceDuration)
        # Append sound to pause
        dct['audio_%s' % int(i)] = silence.append(dct['audio_%s' % int(i)], crossfade=0)
        # If the duration of the total sound is shorter than that of timeline, add silence of residual length (i.e. t_timeline - t_totalsound) to that sound
        if soundDuration + silenceDuration < totalDuration:
            silenceDurationEnd = totalDuration - (soundDuration + silenceDuration)
            silenceEnd = AudioSegment.silent(duration=1000*silenceDurationEnd)
            dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silenceEnd, crossfade=0)
    # Create silent sound file of duration equal to that of the timeline
    mixed = AudioSegment.silent(duration = 1000*totalDuration)
    # Merge all sound files
    for i in range(len(data)):
        mixed = mixed.overlay(dct['audio_%s' % int(i)])
    # Output
    mixed.export(outputFile, format='wav')


