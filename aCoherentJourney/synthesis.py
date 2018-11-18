import numpy as np
import csv
from scipy.io.wavfile import write

def createSineWave(dur, freq, filename):
    # Volume regulation
    rquiet = 0.01

    # Samples per second
    sps = 44100

    # Frequency / pitch of the sine wave
    freq_hz = freq

    freq_hz_bass = 55.0


    # Duration
    duration_s = dur

    # Numpy magiiiic
    each_sample_number = np.arange(duration_s * sps)
    waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
    waveform_integers = np.int16(waveform * 32767)

    # Output
    write(filename, sps, waveform_integers)








def getInputData(filename):
    ifile = open(filename, "rU")
    reader = csv.reader(ifile, delimiter=",")

    rownum = 0
    a = []

    for row in reader:
        a.append(row)
        rownum += 1


    ifile.close()
    return a


    print(", ".join(a))