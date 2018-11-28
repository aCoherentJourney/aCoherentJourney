### Scales length of total sound (= sound of silences before and after sound + sound itself) to length of timeline, where absolute length of the timeline in s is a fixed parameter
def scaleDur(x, inputFile):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    # declares Numpy array for the "RELATIVE" length of total sounds
    soundSilenceDurationRel = np.zeros(len(data))
    # iterate through entire data array
    for i in range(len(data)):
        # the "RELATIVE" duration of the sound itself is a fixed parameter (soundDurationRel)
        # optional: for variable duration (nth column contains relevant data): soundDurationRel = data[i,n]
        # takes "RELATIVE" length of silence BEFORE sound from data
        silenceDurationRel = data[i ,2]
        # counts "RELATIVE" total sound length ("RELATIVE" in quotes, because values can exceed 1)
        soundSilenceDurationRel[i] = soundDurationRel + silenceDurationRel
    # returns absolute total sound lenght, which is the duration of the timeline divided by the maximum "RELATIVE" total sound length
    return x/ max(soundSilenceDurationRel)


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
    # assign weights to each interval to make it sound more "major" or ionian
    #cutIntervalWeight = [40, 1, 20, 2, 30, 1, 2]
    cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in major or ionian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
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
    cutInterval = [0, 2, 3, 5, 7, 8, 10]
    # assign weights to each interval to make it sound more "minor" or aeolian
    cutIntervalWeight = [40, 1, 15, 2, 25, 1, 2]
    # if note is not part of the determined intervals, a random interval of that mode is chosen according to its weight
    if interval % 12 != [cutInterval[i] for i in range(len(cutInterval))]:
        interval = random.choices(cutInterval, weights = cutIntervalWeight)[0]
    else:
        pass
    # calculate note in minor or aeolian scale
    noteFreq = freqKey * 2 ** (root + interval / 12)
    print("Intervals in reference key: " + str(interval % 12) + " and frequency of notes: " + str(noteFreq) )
    return noteFreq

