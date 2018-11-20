import numpy as np
import csv
from scipy.io.wavfile import write

dur = 1.
freq = 440
inputFilePath = "./../data/input/testData2.csv"

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
        dur = data[i,0]
        freq = data[i,1]
        createSineWave(dur, freq, "./../data/output/" + str(outputFilePath) + "" + str(i+1) + ".wav")

createSoundsFromFile(inputFilePath, "testSounds")
