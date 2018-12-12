from config import *
from aCoherentJourney.dataProcessing import *
from aCoherentJourney.soundSynthesis import *
from aCoherentJourney.soundOutput import *
import os

dct = {} # Create dictionary in order to iteratively declare names for variables/parametres/...


### Define output file including path
def outputFilePathFile(outputFile):
    return outputFilePath + outputFile


### Creates sine with decay from data file, with first column in he data file corresponds to the volume and the second to the frequency of the sound
def createSoundsFromFile(inputFile, outputFile, mode, sound, bar, meter, division):
    data = getInputData(inputFile)
    index = outputFile.find(".wav")
    for i in range(len(data)):
        # Duration of sine wave in s
        if bar == "none":
            durMax = scaleDur(totalDuration,inputFile)
            dur = timeAcc(durMax * data[i,3], timeAcc)
        else:
            #define array that contains total duration of timeline, individual duration of sounds and silences
            durVec = scaleDurMeter(totalDuration, inputFile, bar, meter, division)
            soundDuration = timeAcc(durVec[2*i], timeAcc)
            silenceDuration = timeAcc(durVec[2*i+1], timeAcc)
        # Volume (scaled to predetermined range)
        vol = convertLinData(data[i,0], volMax, volMin)
        # Frequency (scaled to predetermined range) and converted to notes from major scale
        # Create saw wave
        if mode == "major":
            freq = freq2MajorConverter(convertLogData(data[i,1], freqMax, freqMin))
        if mode == "minor":
            freq = freq2MinorConverter(convertLogData(data[i,1], freqMax, freqMin))
        if mode == "nomode":
            #freq = freq2MajorConverter(convertLinData(data[i,1], freqMax, freqMin))
            freq = freq2NotesConverter(convertLogData(data[i,1], freqMax, freqMin))
        if mode == "contfreq":
            freq = convertLinData(data[i,1], freqMax, freqMin)
        #print(freq)
        # Create saw wave if requested
        if sound == "saw":
            createSawWave(soundDuration, freq, vol, outputFile + str(i+1) + '.wav')
        # Create square wave if requested
        if sound == "square":
            createSquareWave(soundDuration, freq, vol, outputFile + str(i+1) + '.wav')
        # Create back body wave if requested
        if sound == "blackbody":
            createBlackBodyWave(soundDuration, freq, vol, outputFile + str(i+1) + '.wav')
        # Else create sine wave
        else:
            createSineWave(dur, freq, vol, outputFile + str(i+1) + '.wav')
        dct['audio_%s' % int(i)] = AudioSegment.from_file(outputFile + str(i+1) + '.wav')
        # Introduce decay
        decayStart = 0.5
        #if silenceDuration == (beats-1)/beats:
            #if soundDuration >= 1/beats
            #decayStart = soundDuration - 1 / (2 * beats)
        silence = AudioSegment.silent(duration = 1000 * soundDuration * decayStart)
        dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silence, crossfade = 0.9 * 1000 * soundDuration * decayStart)
        dct['audio_%s' % int(i)].export(outputFile + str(i+1) + '.wav', format='wav')
        # Remove file to save space
        os.remove(outputFile + str(int(i+1)) + '.wav')


### Creates sound timeline of (decaying) sine waves, where the starting of each sine wave is taken from the third column of the data
def createTimeline(inputFile, outputFile, bar, meter, division):
    data = getInputData(inputFile)
    for i in range(len(data)):
        # Duration of silence and sound in s
        if bar == "none":
            durMax = scaleDur(totalDuration,inputFile)
            soundDuration = timeAcc(durMax * data[i,3], timeAcc)
            silenceDuration = timeAcc(durMax * data[i,2], timeAcc)
        else:
            #define array that contains total duration of timeline, individual duration of sounds and silences
            durVec = scaleDurMeter(totalDuration, inputFile, bar, meter, division)
            #for i in range(len(data)):
            soundDuration = timeAcc(durVec[2*i], timeAcc)
            silenceDuration = timeAcc(durVec[2*i+1], timeAcc)
            #print(silenceDuration)
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
    mixed.export(outputFile + '.wav', format='wav')


