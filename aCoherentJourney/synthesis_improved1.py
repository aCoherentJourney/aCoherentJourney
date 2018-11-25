import numpy as np
from numpy import trapz
import csv
import random
import os
from scipy.io.wavfile import write
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy import fftpack

### Define functions ###

dct = {}


#inputFilePath = "aCoherentJourneyProject/aCoherentJourney/data/input/"
inputFilePath = "/home/alex/"
#outputFilePath = "aCoherentJourneyProject/"
outputFilePath = "/home/alex/"


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
    freq_Hz = freq
    # Duration
    duration_s = dur
    # Numpy magiiiic
    each_sample_number = np.arange(duration_s * sps)
    waveform = np.sin(2 * np.pi * each_sample_number * freq_Hz / sps) * rquiet * vol
    waveform_integers = np.int16(waveform * 2**(nbit-1)-1)
    # Output
    write(outputFilePath, sps, waveform_integers)


def blackBodySoundGenerator(dur, freq, vol, outputFilePath):
    #Sound generation principle create interference of sine waves quasi-continuous frequency range, where contribution of each frequency bin scales according to blackbody curve (I = x**3/(exp(x)-1)) at that freqency (scale such that the target frequency is at extremal frequency x = 2.82... The sound is separated into three parts beginning/ending to freqMin, inflection frequencies (0.96... and 4.63...) and freqMax.
    # Bit rate
    nbit = 32
    # Samples per second
    sps = 44100
    # Duration
    duration_s = dur
    # Numpy magiiiic
    each_sample_number = np.arange(duration_s * sps)
    nFreq = [1e3,1e3,1e3]
    extremum = 2.8214393721
    inflection1 = 0.966268
    inflection2 = 4.62325
    # Frequency / pitch of the sine wave
    maxNu = freq / extremum
    #nuMin = freq * inflection1 / extremum
    #nuMax = freq * inflection2 / extremum
    nuMin = [freqMin / extremum, freq * inflection1 / extremum, freq * inflection2 / extremum]
    nuMax = [freq * inflection1 / extremum, freq * inflection2 / extremum, freqMax / extremum]
    nuPart = ['low', 'main', 'high']
    rquietPart = np.zeros(len(nuPart))
    for j in range(len(nuMin)):
        print("Generating " + nuPart[j] + " part...")
        nu = np.arange(nFreq[j])
        nu = (nu*(nuMax[j]-nuMin[j])/nFreq[j] + nuMin[j])
        bNu = (nu/maxNu)**3 / ( np.exp(nu/maxNu) - 1)
        # Volume regulation
        dNu = (nu[1]-nu[0])
        period = sps / nu
        area1 = trapz(bNu, dx = dNu)
        sumbNu = sum(bNu)
        area2 = sum(bNu) * dNu
        print("Integral of black body curve (trapez vs. column): " + str(area1) + " and " + str(area2))
        rquiet = 1/area1
        rquietPart[j] = rquiet / 1012.7219561245
        totWaveform = 0
        for i in range(len(nu)):
            waveform = np.sin(2 * np.pi * each_sample_number * nu[i] / sps) * rquiet * bNu[i] * dNu * 100000 * rquietPart[j]
            totWaveform += waveform
            if (i%int(nFreq[j]/20) == 0):
                print(nu[i], rquiet * bNu[i] * dNu)
        print("Total contribution of normalisation factor: ", rquiet * sumbNu * dNu)
        if nbit == 16:
            waveform_integers = np.int16(totWaveform * 2**(nbit-1)-1)
        elif nbit == 32:
            waveform_integers = np.int32(totWaveform * 2**(nbit-1)-1)
        elif nbit == 64:
            waveform_integers = np.int64(totWaveform * 2**(nbit-1)-1)
        if j == 0:
            write(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_low.wav", sps, waveform_integers)
            low =  AudioSegment.from_file(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_low.wav")
        if j == 1:
            write(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_main.wav", sps, waveform_integers)
            main =  AudioSegment.from_file(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_main.wav")
        if j == 2:
            write(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_high.wav", sps, waveform_integers)
            high =  AudioSegment.from_file(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_high.wav")
        print("Done!")
    mixed = low.overlay(main)
    mixed = mixed.overlay(high)
    main.export(outputFilePath + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_mixed.wav")
    # Output
    """fig, ax = plt.subplots()
    ax.plot(nu, bNu * rquiet)
    ax.set_xlim(0, nuMax)
    ax.set_ylim(0, max(bNu) * rquiet * 1.1)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude')
    plt.show()
    plt.close()"""


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


def freq2MajorConverter(freq): #    W-W-H-W-W-W-H
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
    root = int(abs((interval/12)))
    if interval < 0:
        root = - root
    else:
        root = root
    if interval < 0.:
        interval = - (int(interval) + 1)
    else:
        interval = int(interval)
    cutInterval = [0, 2, 4, 5, 7, 9, 11]
    cutIntervalWeight = [10, 1, 4, 2, 6, 1, 2]
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


def freq2MinorConverter(freq): #    W-H-W-W-H-W-W
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
    root = int(abs((interval/12)))
    if interval < 0:
        root = - root
    else:
        root = root
    if interval < 0.:
        interval = - (int(interval) + 1)
    else:
        interval = int(interval)
    cutInterval = [0, 2, 3, 5, 6, 8, 10]
    cutIntervalWeight = [10, 1, 3, 1, 5, 1, 2]
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


def createSoundsFromFile(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    for i in range(len(data)):
        dur = soundDurationRel*durMax
        vol = convertLinData(data[i,0], volMax, volMin)
        freq = freq2MinorConverter(convertLogData(data[i,1], freqMax, freqMin))
        createSineWave(dur, freq, vol, str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav")
        dct['audio_%s' % int(i)] = AudioSegment.from_file(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")
        silence = AudioSegment.silent(duration = 999 * dur)
        dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silence, crossfade = 900 * dur)
        dct['audio_%s' % int(i)].export(str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav", format='wav')
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
volMin = 0.5
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

#createSoundsFromFile(inputFile, "testSounds")

#createTimeline(inputFile, "mixed")

blackBodySoundGenerator(3, 440, 1, "testBlackbody")

print(".wav files generated!")
