import numpy as np
from scipy.io.wavfile import write

def writeSound(samplerate, waveform, 'testname.wav'):
    write(samplerate, waveform)
