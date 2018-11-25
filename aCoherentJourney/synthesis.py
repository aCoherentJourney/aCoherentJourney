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

dct = {} # Create dictionary in order to iteratively declare names for variables/parameters/...

inputFilePath = "./../data/input/"
outputFilePath = "./../data/output/"

### Read data from csv-file and returns data as Numpy array (N-dimensional according to number of columns in file)
def getInputData(inputFile):
    data = np.genfromtxt(inputFile, delimiter = ",")
    return data


### Scales length of total sound (= sound of silences before and after sound + sound itself) to length of timeline, where absolute length of the timeline in s is a fixed parameter
def durMax(x, inputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    # declares Numpy array for the "RELATIVE" length of total sounds
    soundSilenceDurationRel = np.zeros(len(data))
    #iterate through entire data array
    for i in range(len(data)):
        # the "RELATIVE" duration of the sound itself is a fixed parameter (soundDurationRel)
        # optional: for variable duration (nth column contains relevant data): soundDurationRel = data[i,n]
        # takes "RELATIVE" length of silence BEFORE sound from data
        silenceDurationRel = data[i,2]
        # counts "RELATIVE" total sound length ("RELATIVE" in quotes, because values can exceed 1)
        soundSilenceDurationRel[i] = soundDurationRel + silenceDurationRel
    # returns absolute total sound lenght, which is the duration of the timeline divided by the maximum "RELATIVE" total sound length
    return x/max(soundSilenceDurationRel)
        

### Converts data points within given range in a linear scale
def convertLinData(x, dmax, dmin):
    # Makes sure that dmax > dmin
    if dmax < dmin:
        a = dmax
        dmax = dmin
        dmin = a        
    return (dmax - dmin) * x + dmin

  
### Converts data points within given range in a logarithmic scale
def convertLogData(x, dmax, dmin):
    # Makes sure that dmax > dmin
    if dmax < dmin:
        a = dmax
        dmax = dmin
        dmin = a
    # Make sure the input value is not zero
    if dmin == 0:
        dmin = 0.01
    return np.exp( (np.log(dmax) - np.log(dmin)) * x + np.log(dmin) )


### Creates sine wave or duration dur, frequency freq and volume vol and write it to sound file
def createSineWave(dur, freq, vol, outputFile):
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
    # Calculates waveform (basic sound processing)
    each_sample_number = np.arange(duration_s * sps)
    waveform = np.sin(2 * np.pi * each_sample_number * freq_Hz / sps) * rquiet * vol
    waveform_integers = np.int16(waveform * 2**(nbit-1)-1)
    # Output
    write(outputFile, sps, waveform_integers)


    ### Create black body sound of duration dur, frequency freq and volume vol
    ### Generation principle: Create interference of sine waves in quasi-continuous frequency range, where contribution of each frequency bin scales according to blackbody curve (I = x**3/(exp(x)-1)) at that frequency, scaled such that the target frequency is at extremal value x = 2.82...
    ### The sound is separated into three parts beginning/ending at freqMin, inflection frequencies (0.96... and 4.63...) and freqMax.
def blackBodySoundGenerator(dur, freq, vol, outputFile):
    # Bit rate
    nbit = 32
    # Samples per second
    sps = 44100
    # Duration
    duration_s = dur
    # Extremal and inflection points of black body funcion
    extremum = 2.8214393721
    inflection1 = 0.966268
    inflection2 = 4.62325
    # Scales frequency such that input frequency is a extremal value
    maxNu = freq / extremum
    # Defines starting and end points of each part
    nuMin = [freqMin / extremum, freq * inflection1 / extremum, freq * inflection2 / extremum]
    nuMax = [freq * inflection1 / extremum, freq * inflection2 / extremum, freqMax / extremum]
    nuPart = ['low', 'main', 'high']
    # Creates waveforms of each part
    each_sample_number = np.arange(duration_s * sps)
    # ... number of samples per part
    nFreq = [1e3,1e3,1e3]
    # Declares scale factor of each part to determine their relative volumes
    scalePart = np.zeros(len(nuPart))
    for j in range(len(nuMin)):
        print("Generating " + nuPart[j] + " part...")
        # Creates Numpy array of frequency spectrum of each part
        nu = np.arange(nFreq[j])
        # Scales the array such that it lies between determined frequency range
        nu = (nu*(nuMax[j]-nuMin[j])/nFreq[j] + nuMin[j])
        # Calculate black body function value of frequenc nu scaled such that extremal value is at freq (x = nu/maxNu)
        x = nu / maxNu
        bNu = x**3 / ( np.exp(x) - 1)
        ## Scale factor of each part is equal to integral of each part divided by total integral of black body function
        # Calculates integral
        dNu = (nu[1]-nu[0]) # step size
        area1 = trapz(bNu, dx = dNu)
        # Alternative method for calculating integral
        sumbNu = sum(bNu) # sum of all values of black body function
        area2 = sum(bNu) * dNu
        # Scale factor such that total contribution of frequencies is 1
        rquiet = 1/area1
        scaleNorm = rquiet * bNu * dNu
        # Individual scale factor of each part
        scalePart[j] = 1/(rquiet * 1012.7219561245)
        print("Integral of black body curve (trapez vs. column): " + str(area1) + " and " + str(area2))
        # Calculate wave form of frequency spectrum
        totWaveform = 0
        for i in range(len(nu)):
            # Creates sine wave of frequency nu scaled by its contribution according to black body function
            waveform = np.sin(2 * np.pi * each_sample_number * nu[i] / sps) * scaleNorm[i] * scalePart[j] * 100
            # Adds each sine wave together to create interference
            totWaveform += waveform
            if (i%int(nFreq[j]/20) == 0):
                print(nu[i], rquiet * bNu[i] * dNu)
        # Waveform changes according to number of bits ...
        if nbit == 16:
            waveform_integers = np.int16(totWaveform * 2**(nbit-1)-1)
        elif nbit == 32:
            waveform_integers = np.int32(totWaveform * 2**(nbit-1)-1)
        elif nbit == 64:
            waveform_integers = np.int64(totWaveform * 2**(nbit-1)-1)
        # Output of each part
        if j == 0:
            write(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_low.wav", sps, waveform_integers)
            low =  AudioSegment.from_file(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_low.wav")
        if j == 1:
            write(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_main.wav", sps, waveform_integers)
            main =  AudioSegment.from_file(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_main.wav")
        if j == 2:
            write(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_high.wav", sps, waveform_integers)
            high =  AudioSegment.from_file(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_high.wav")
        print("Done!")
    # Overlay each part
    mixed = low.overlay(main)
    mixed = mixed.overlay(high)
    # Output of merged sound
    main.export(outputFilePath + outputFile + "_n" + str(int( nFreq[j] / 10**(int(np.log10(nFreq[j]))) )) + "e" + str(int(np.log10(nFreq[j]))) + "_mixed.wav")


### Assigns each frequency to the next lowest "note frequency" with respect to given reference frequency (here: 440 Hz)
def freq2NotesConverter(freq):
    noteFreq = 440
    # if frequency is smaller than that of smallest root note, which is a predetermined parameter from given frequency range, it is set to this root note
    if freq <= rootFreqMin:
        interval = 0
        noteFreq = rootFreqMin
    # otherwise assign it to next lowest interval 
    else:
        #calculate interval by taking the base 2 logarithm of the truncated ratio of the frequency to the lowest root frequency scaled by 12 (12 is th enumber of half steps in an octave)
        interval = int( np.log2(freq / rootFreqMin) * 12)
        # note frequency is the xth multiple of 2 of the lowest root frequency, where x is the interval divided by 12
        noteFreq = float(rootFreqMin * 2 ** (interval / 12))
    return noteFreq


### Shifts note frequencies such that the sound of a major or ionian mode of a predetermined key is created
def freq2MajorConverter(freq): #    W-W-H-W-W-W-H
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_hz
    if freqKey < freqRef_hz:
        freqKey = freqRef_hz * 2 ** ( int(np.log2(freqKey / freqRef_hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_hz * 2 ** ( int(np.log2(freqKey / freqRef_hz) * 12) / 12 )
    # generate notes
    noteFreq = freq2NotesConverter(freq)
    # calculate interval and the corresponding root of each note (i.e. which octave of reference note)
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
    # define the intervals of major or ionian scale
    cutInterval = [0, 2, 4, 5, 7, 9, 11]
    # assign weights to each interval to make it sounds more "major" or ionian
    cutIntervalWeight = [10, 1, 4, 2, 6, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in major or ionian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    #print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq

### Shifts note frequencies such that the sound of a minor or aeolian mode of a predetermined key is created
def freq2MinorConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_hz
    if freqKey < freqRef_hz:
        freqKey = freqRef_hz * 2 ** ( int(np.log2(freqKey / freqRef_hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_hz * 2 ** ( int(np.log2(freqKey / freqRef_hz) * 12) / 12 )
    #print("In key of: " + str(freqKey))
    #generate notes
    noteFreq = freq2NotesConverter(freq)
    # calculate interval and the corresponding root of each note (i.e. which octave of reference note)
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
    # define the intervals of minor or aeolian scale
    cutInterval = [0, 2, 3, 5, 6, 8, 10]
    # assign weights to each interval to make it sounds more "minor" or aeolian
    cutIntervalWeight = [10, 1, 3, 1, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in minor or aeolian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    #print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Creates sine with decay from data file, with first column in he data file corresponds to the volume and the second to the frequency of the sound
def createSoundsFromFile(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    for i in range(len(data)):
        # Duration of sine wave in s
        dur = soundDurationRel*durMax
        # Volume (scaled to predetermined range)
        vol = convertLinData(data[i,0], volMax, volMin)
        # Frequency (scaled to predetermined range) and converted to notes from major scale
        freq = freq2MajorConverter(convertLogData(data[i,1], freqMax, freqMin))
        # Create sine wave
        createSineWave(dur, freq, vol, str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav")
        dct['audio_%s' % int(i)] = AudioSegment.from_file(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")
        # Introduce decay
        silence = AudioSegment.silent(duration = 1000 * dur)
        dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silence, crossfade = 999 * dur)
        dct['audio_%s' % int(i)].export(str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav", format='wav')
        # Remove file to save space
        os.remove(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")


### Creates sound timeline of (decaying) sine waves, where the starting of each sine wave is taken from the third column of the data
def createTimeline(inputFile, outputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    for i in range(len(data)):
        # Duration of sound in s
        soundDuration = soundDurationRel*durMax
        # Duration of silence in s before sine wave starts taken from data
        silenceDuration = durMax*data[i,2]
        # Create silent sound of durations of the silence before sound
        silence = AudioSegment.silent(duration = 1000 * silenceDuration)
        # Append sound to pause        
        dct['audio_%s' % int(i)] = silence.append(dct['audio_%s' % int(i)], crossfade=0)
        # If the duration of the total sound is shorter than that of timeline, add silence of residual length (i.e. t_timeline = t_totalsound) to that sound
        if soundDuration + silenceDuration < totalDuration:
            silenceDurationEnd = totalDuration - (soundDuration + silenceDuration)
            silenceEnd = AudioSegment.silent(duration=1000*silenceDurationEnd)
            dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silenceEnd, crossfade=0)
    # Create silent sound file of duration equal to that of the timeline
    mixed = AudioSegment.silent(duration = 1000*totalDuration)
    #mixed = dct['audio_%s' % int(0)]
    # Merge all sound files
    for i in range(len(data)):
        mixed = mixed.overlay(dct['audio_%s' % int(i)])
    # Output
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

createSoundsFromFile(inputFile, "testSounds")
createTimeline(inputFile, "mixed")
blackBodySoundGenerator(3, 440, 1, "testBlackbody")

print(".wav files generated!")
