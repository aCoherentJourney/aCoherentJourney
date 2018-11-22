import numpy as np
import csv
import os
from scipy.io.wavfile import write
from pydub import AudioSegment


### Define functions ###

dct = {}


inputFilePath = "./../data/input/"
outputFilePath = "./../data/output/"


def getInputData(inputFile):
    data = np.genfromtxt(inputFile, delimiter = ",")
    #print(data)
    return data

def durMax(x,inputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    soundSilenceDurationRel = np.zeros(len(data))
    for i in range(len(data)):
        #for variable duration (nth column contains relevant data): soundDurationRel = data[i,n]
        silenceDurationRel = data[i,2]
        soundSilenceDurationRel[i] = soundDurationRel + silenceDurationRel
    return x/max(soundSilenceDurationRel)
        

def convertLinData(x, dmax, dmin):
    a = 0.
    if dmax < dmin:
        a = dmax
        dmax = dmin
        dmin = a        
    return (dmax - dmin) * x + dmin

  
def convertLogData(x, dmax, dmin):
    if dmax < dmin:
        a = dmax
        dmax = dmin
        dmin = a
    if dmin == 0:
        dmin = 0.01
    return np.exp( (np.log(dmax) - np.log(dmin)) * x + np.log(dmin) )


def createSineWave(dur, freq, vol, outputFilePath):
    # Volume regulation
    rquiet = 0.01
    # Bit rate
    nbit = 16
    # Samples per second
    sps = 44100
    # Frequency / pitch of the sine wave
    freq_hz = freq
    # Duration
    duration_s = dur
    # Numpy magiiiic
    each_sample_number = np.arange(duration_s * sps)
    waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps) * rquiet * vol
    waveform_integers = np.int16(waveform * 2**(nbit-1)-1)
    # Output
    write(outputFilePath, sps, waveform_integers)
    

def freq2NotesConverter(freq):
    noteFreq = 440
    if freq <= rootFreqMin:
        interval = 0
        noteFreq = rootFreqMin
    else:
        #calculate interval by taking the base 2 logarithm of the truncated of 12 times the ratio of the frequency to the lowest root frequency
        interval = int( np.log2(freq / rootFreqMin) * 12)
        noteFreq = float(rootFreqMin * 2 ** (interval / 12))
    return noteFreq


def freq2MajorConverter(freq):
    #frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_hz
    if freqKey < freqRef_hz:
        freqKey = freqRef_hz * 2 ** ( int(np.log2(freqKey / freqRef_hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_hz * 2 ** ( int(np.log2(freqKey / freqRef_hz) * 12) / 12 )
    #print("In key of: " + str(freqKey))
    #generate notes
    noteFreq = freq2NotesConverter(freq)
    interval = np.log2( noteFreq / freqKey ) * 12
    if interval < 0.:
        interval = - (int(interval) + 1)
    else:
        interval = int(interval)
    cutInterval = [1, 3, 6, 8, 10]
    for i in range(len(cutInterval)):
        if interval % 12 == cutInterval[i]:
            interval += 1
        else:
            pass
    noteFreq = freqKey * 2 ** (interval / 12)
    #print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


def createSoundsFromFile(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    for i in range(len(data)):
        dur = soundDurationRel*durMax
        vol = convertLinData(data[i,0], volMax, volMin)
        freq = freq2MajorConverter (convertLinData(data[i,1], freqMax, freqMin))
        createSineWave(dur, freq, vol, str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav")
        dct['audio_%s' % int(i)] = AudioSegment.from_file(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")
        if i%1 == 0:
            os.remove(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")


def createTimeline(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    mixed = AudioSegment.silent(duration = 1000*totalDuration)
    for i in range(len(data)):
        soundDuration = soundDurationRel*durMax
        #print(soundDuration)
        silenceDuration = durMax*data[i,2]
        #print(silenceDuration)
        silence = AudioSegment.silent(duration = 1000 * silenceDuration)
        #dct['audio_%s' % int(i)] = AudioSegment.from_file(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")
        #os.remove(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")
        dct['audio_%s' % int(i)] = silence.append(dct['audio_%s' % int(i)], crossfade=0)
        if soundDuration + silenceDuration < totalDuration:
            silenceDurationEnd = totalDuration - (soundDuration + silenceDuration)
            #print(silenceDurationEnd)
            silenceEnd = AudioSegment.silent(duration=1000*silenceDurationEnd)
            dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silenceEnd, crossfade=0)
        #print("__________________")
    mixed = dct['audio_%s' % int(0)]
    for i in range(len(data)-1):
        mixed = mixed.overlay(dct['audio_%s' % int(i+1)])
    mixed.export(str(outputFilePath) + "" + str(outputFile) + ".wav", format='wav')

### Run ###
###################################################################

inputFile = ("testData4.csv")
soundDurationRel = 0.2
totalDuration = 20
volMin = 0
volMax = 1
durMin = 0
durMax = durMax(totalDuration,inputFile)
freqMin = 40
freqMax = 15000
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

createSoundsFromFile(inputFile, "testSounds")
createTimeline(inputFile, "mixed")

print(".wav files generated!")
