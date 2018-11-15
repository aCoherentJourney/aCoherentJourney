import numpy as np
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

