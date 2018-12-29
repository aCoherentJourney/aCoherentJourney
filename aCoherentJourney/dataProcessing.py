import random
from aCoherentJourney.dataInput import *
#import sys
#sys.path.append('./../')
#from test import *
from config import *

### Scales length of total sound (= sound of silences before and after sound + sound itself) to length of timeline, where absolute length of the timeline in s is a fixed parameter
def scaleDur(x, inputFile):
    data = getInputData(inputFile)
    # declares Numpy array for the "RELATIVE" length of total sounds
    soundSilenceDurationRel = np.zeros(len(data))
    # iterate through entire data array
    for i in range(len(data)):
        # the "RELATIVE" duration of the sound itself is a fixed parameter (soundDurationRel)
        # optional: for variable duration (nth column contains relevant data): soundDurationRel = data[i,n]
        # takes "RELATIVE" length of silence BEFORE sound from data
        silenceDurationRel = data[i,2]
        soundDurationRel = data[i,3]
        # counts "RELATIVE" total sound length ("RELATIVE" in quotes, because values can exceed 1)
        soundSilenceDurationRel[i] = soundDurationRel + silenceDurationRel
    # returns absolute total sound lenght, which is the duration of the timeline divided by the maximum "RELATIVE" total sound length
    return x / max(soundSilenceDurationRel)


### Scales length of total sound (= sound of silences before and after sound + sound itself) to length of timeline, where absolute length of the timeline in s is a fixed parameter
def scaleDurMeter(x, inputFile, bar, meter, division):
    #nBars = 8
    beats = nBars * bar * division
    #print(beats)
    data = getInputData(inputFile)
    # declares Numpy array for the "RELATIVE" length of total sounds
    vol = np.zeros(len(data))
    soundSilenceDurationRel = np.zeros(len(data))
    soundDurationRel = np.zeros(len(data))
    silenceDurationRel = np.zeros(len(data))
    # iterate through entire data array
    output = []
    for i in range(len(data)):
        # the "RELATIVE" duration of the sound itself is a fixed parameter (soundDurationRel)
        # optional: for variable duration (nth column contains relevant data): soundDurationRel = data[i,n]
        # takes "RELATIVE" length of silence BEFORE sound from data
        vol[i] = convertLinData(data[i,0], volMax, volMin)
        silenceDurationRel[i] = data[i,2]
        soundDurationRel[i] = convertLinData(data[i,3],durRelMax, durRelMin)
        # counts "RELATIVE" total sound length ("RELATIVE" in quotes, because values can exceed 1)
        soundSilenceDurationRel[i] = soundDurationRel[i] + silenceDurationRel[i]
        if soundSilenceDurationRel[i] >= 1.:
            soundDurationRel[i] = 1 - silenceDurationRel[i]
            soundSilenceDurationRel[i] = soundDurationRel[i] + silenceDurationRel[i]
        #scaling factor
        #maxSoundSilenceDurationRel = max(soundSilenceDurationRel)
        #scale = 1 / maxSoundSilenceDurationRel
        #print(scale)
        #np.zeros(1 + len(soundDurationRel) + len(silenceDurationRel))
        #for i in range(len(data)):
        #soundDurationRel[i] = int(soundDurationRel[i] * scale * beats) / beats * x
        #silenceDurationRel[i] = int(silenceDurationRel[i] * scale * beats) / beats * x
        silenceDurationRel[i] = int(silenceDurationRel[i] * beats) / beats * x
        soundDurationRel[i] = soundDurationRel[i] * x
        barBeat = beats / x
        #print((silenceDurationRel[i] * barBeat))# % bar)
        if int(silenceDurationRel[i] * barBeat) % bar == meter[0]:
            vol[i] = vol[i] * 4
        if int(silenceDurationRel[i] * barBeat) % bar == meter[1]:
            vol[i] = vol[i] * 2
    vol = vol / max(vol)
    for i in range(len(data)):
        output.append(soundDurationRel[i])
        output.append(silenceDurationRel[i])
        #print(int(silenceDurationRel[i]) % bar)
        output.append(vol[i])
    return np.array(output)


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
    return np.exp((np.log(dmax) - np.log(dmin)) * x + np.log(dmin))


def timeAcc(x, timeAcc):
    timeAcc_ms = 1000
    return int(x * timeAcc_ms) / timeAcc_ms


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
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # assign weights to each interval to make it sound more "major" or ionian
    #cutIntervalWeight = [40, 1, 20, 2, 30, 1, 2]
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        intervalVec = random.choices(cutInterval, weights = cutIntervalWeight)
        interval = intervalVec[0]
        #print(intervalVec)
    else:
        pass
    # calculate note in major or ionian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    #print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a minor or aeolian mode of a predetermined key is created
def freq2MinorConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    cutInterval = [0, 2, 3, 5, 7, 8, 10]
    # assign weights to each interval to make it sound more "minor" or aeolian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in minor or aeolian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a dorian mode of a predetermined key is created
def freq2DorianConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # define the intervals of dorian scale
    cutInterval = [0, 2, 3, 5, 7, 9, 10]
    # assign weights to each interval to make it sound more dorian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in dorian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a phrygian mode of a predetermined key is created
def freq2PhrygianConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # define the intervals of phrygian scale
    cutInterval = [0, 1, 3, 5, 7, 8, 10]
    # assign weights to each interval to make it sound more phrygian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in phrygian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a lydian mode of a predetermined key is created
def freq2LydianConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # define the intervals of lydian scale
    cutInterval = [0, 2, 4, 6, 7, 9, 11]
    # assign weights to each interval to make it sound more lydian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in lydian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a mixolydian mode of a predetermined key is created
def freq2MixolydianConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # define the intervals of mixolydian scale
    cutInterval = [0, 2, 4, 5, 7, 9, 10]
    # assign weights to each interval to make it sound more mixolydian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in mixolydian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a locrian mode of a predetermined key is created
def freq2LocrianConverter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # define the intervals of locrian scale
    cutInterval = [0, 1, 3, 5, 6, 8, 10]
    # assign weights to each interval to make it sound more locrian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in locrian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq


### Shifts note frequencies such that the sound of a mixolydian mode of a predetermined key is created
def freq2MixolydianFlat6Converter(freq): #    W-H-W-W-H-W-W
    # frequency of the key must be adjusted to the reference frequency
    freqKey = freqKey_Hz
    if freqKey < freqRef_Hz:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12 - 1) / 12 )
    else:
        freqKey = freqRef_Hz * 2 ** ( int(np.log2(freqKey / freqRef_Hz) * 12) / 12 )
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
    # define the intervals of mixolydian scale
    cutInterval = [0, 2, 4, 5, 7, 8, 10]
    # assign weights to each interval to make it sound more mixolydian
    #cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    cutIntervalWeight = [10, 1, 3, 2, 5, 3, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in mixolydian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq
