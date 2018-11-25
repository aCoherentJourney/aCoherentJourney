import numpy as np
import csv
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
    durations = np.zeros(len(data))
    for i in range(len(data)):
        durations[i] = data[i,0] + data[i,2]
    return x/max(durations)
        

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


def createSineWave(dur, freq, outputFilePath):
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
    waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
    waveform_integers = np.int16(waveform * 2**(nbit-1)-1)
    # Output
    write(outputFilePath, sps, waveform_integers)


def createSoundsFromFile(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    for i in range(len(data)):
        dur = convertLinData(data[i,0], durMax, durMin)
        freq = convertLogData(data[i,1], freqMax, freqMin)
        createSineWave(dur, freq, str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav")


def createTimeline(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    mixed = AudioSegment.silent(duration = 1000*totalDuration)
    for i in range(len(data)):
        soundDuration = convertLinData(data[i,0], durMax, durMin)
        #print(data[i,0], data[i,1], data[i,2])
        #print(soundDuration)
        silenceDuration = durMax*data[i,2]
        #print(silenceDuration)
        #print(soundDuration)
        silence = AudioSegment.silent(duration = 1000 * silenceDuration)
        dct['audio_%s' % int(i)] = AudioSegment.from_file(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")
        #print(outputFilePath + "testSounds" + str(int(i+1)) + ".wav")
        dct['audio_%s' % int(i)] = silence.append(dct['audio_%s' % int(i)], crossfade=0)
        if soundDuration + silenceDuration < totalDuration:
            silenceDurationEnd = totalDuration - (soundDuration + silenceDuration)
            silenceEnd = AudioSegment.silent(duration=1000*silenceDurationEnd)
            dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silenceEnd, crossfade=0)
            #print(silenceDurationEnd)
        #print("________")
    mixed = dct['audio_%s' % int(0)]
    for i in range(len(data)-1):
        mixed = mixed.overlay(dct['audio_%s' % int(i+1)])
    mixed.export(str(outputFilePath) + "" + str(outputFile) + ".wav", format='wav')

### Run ###
###################################################################

totalDuration = 15
durMin = 0
durMax = durMax(totalDuration,"testData2.csv")
freqMax = 15000
freqMin = 40

createSoundsFromFile("testData2.csv", "testSounds")

createTimeline("testData2.csv", "mixed")

print(".wav files generated!")

'''audio1 = AudioSegment.from_file(allpath + "testSounds1.wav")
audio2 = AudioSegment.from_file(allpath + "testSounds2.wav")
audio3 = AudioSegment.from_file(allpath + "testSounds3.wav")

silence = AudioSegment.silent(duration=1000)
silence1 = AudioSegment.silent(duration=0)
silence2 = AudioSegment.silent(duration=3000)
silence3 = AudioSegment.silent(duration=6000)

maudio1 = audio1.append(silence, crossfade=0)
maudio2 = silence.append(audio1, crossfade=0)
maudio3 = silence3.append(audio3, crossfade=0)

mixed = maudio1.overlay(maudio2)

#mixed = maudio1.append(maudio2)
#mixed = mixed.append(maudio3)
mixed.export("mixed.wav", format='wav')
#mixed.export("mixed.wav", format='wav')
#maudio1.export("mixed1.wav", format='wav')
#maudio2.export("mixed2.wav", format='wav')
#maudio3.export("mixed3.wav", format='wav')'''
