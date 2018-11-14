import numpy as np
from scipy.io.wavfile import write

# Volume regulation
rquiet = 0.01

# Samples per second
sps = 44100

# Frequency / pitch of the sine wave
freq_hz_1 = 440.0
freq_hz_2 = 880.0

freq_hz_bass = 55.0


# Duration
duration_s = 5.0

#Numpy magiiiic
each_sample_number = np.arange(duration_s * sps)
waveform_1 = np.sin(2 * np.pi * each_sample_number * freq_hz_1 / sps)
waveform_2 = np.sin(2 * np.pi * each_sample_number * freq_hz_2 / sps)
waveform_bass = np.sin(2 * np.pi * each_sample_number * freq_hz_bass / sps)

waveform = ((waveform_1 + waveform_2 + waveform_bass)/3) * rquiet
waveform_integers = np.int16(waveform * 32767)

waveform_bass = np.sin(2 * np.pi * each_sample_number * freq_hz_bass / sps) * rquiet
waveform_integers_bass = np.int16(waveform_bass * 32767)


write('first_sine_wave.wav', sps, waveform_integers)
write('first_sine_wave_bass.wav', sps, waveform_integers_bass)
