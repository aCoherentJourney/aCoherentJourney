import numpy as np
import csv
from scipy.io.wavfile import write

dur = 1.
freq = 440
inputFilePath = "./../data/input/testData2.csv"
durMax = 10
durMin = 0
freqMax = 15000
freqMin = 40


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


def getInputData(inputFilePath):
    data = np.genfromtxt(inputFilePath, delimiter = ",")
    #print(data)
    return data

def createSoundsFromFile(inputFilePath, outputFilePath):
    data = getInputData(inputFilePath)
    for i in range(len(data)):
        dur = convertLogData(data[i,0], durMax, durMin)
        freq = convertLogData(data[i,1], freqMax, freqMin)
        createSineWave(dur, freq, "./../data/output/" + str(outputFilePath) + "" + str(i+1) + ".wav")

createSoundsFromFile(inputFilePath, "testSounds")
