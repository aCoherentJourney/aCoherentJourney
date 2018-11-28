### Define functions ###

dct = {} # Create dictionary in order to iteratively declare names for variables/parameters/...

inputFilePath = "./../data/input/"
outputFilePath = "./../data/output/"


### Creates sine wave or duration dur, frequency freq and volume vol and write it to sound file
def createSawWave(dur, freq, vol, outputFile):
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
    t = np.linspace(0, duration_s, sps * duration_s)
    waveform = signal.sawtooth(2 * np.pi * freq_Hz * t) * rquiet * vol
    waveform_integers = np.int16(waveform * 2**(nbit-1)-1)
    # Output
    write(outputFile, sps, waveform_integers)


### Creates saw wave or duration dur, frequency freq and volume vol and write it to sound file
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




