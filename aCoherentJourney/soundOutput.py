### Creates sine with decay from data file, with first column in he data file corresponds to the volume and the second to the frequency of the sound
def createSoundsFromFile(inputFile, outputFile, mode):
    data = getInputData(str(inputFilePath) + "" + str(inputFile))
    for i in range(len(data)):
        # Duration of sine wave in s
        dur = soundDurationRel*durMax
        # Volume (scaled to predetermined range)
        vol = convertLinData(data[i,0], volMax, volMin)
        # Frequency (scaled to predetermined range) and converted to notes from major scale
        # Create saw wave
        if mode == "saw":
            freq = createSawWave(10, 440, 1, str(outputFilePath) + "" + str(outputFile) + ".wav")
        else:
            if mode == "major":
                freq = freq2MajorConverter(convertLinData(data[i,1], freqMax, freqMin))
            if mode == "minor":
                freq = freq2MinorConverter(convertLinData(data[i,1], freqMax, freqMin))
            if mode == "nomode":
                #freq = freq2MajorConverter(convertLinData(data[i,1], freqMax, freqMin))
                freq = freq2NotesConverter(convertLinData(data[i,1], freqMax, freqMin))
            else:
                freq = convertLinData(data[i,1], freqMax, freqMin)
            # Create sine wave
            createSineWave(dur, freq, vol, str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav")
            dct['audio_%s' % int(i)] = AudioSegment.from_file(str(outputFilePath) + str(outputFile) + str(int(i+1)) + ".wav")
            # Introduce decay
            silence = AudioSegment.silent(duration = 1000 * dur)
            dct['audio_%s' % int(i)] = dct['audio_%s' % int(i)].append(silence, crossfade = 999 * dur)
            dct['audio_%s' % int(i)].export(str(outputFilePath) + "" + str(outputFile) + "" + str(i+1) + ".wav", format='wav')
        # Remove file to save space
        #os.remove(str(outputFilePath) + "testSounds" + str(int(i+1)) + ".wav")


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
    mixed.export(str(outputFilePath) + "" + str(outputFile) + ".wav", format='wav')


