# Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html

import os
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile
import numpy as np

import librosa


audio_path = "./tones.wav"
# audio_samples, sample_rate = librosa.load(audio_path)
sample_rate, audio_samples = wavfile.read(audio_path)
samples_per_window = 1024
freq, time, Zxx = signal.stft(audio_samples, fs=sample_rate, nperseg=samples_per_window, noverlap=(samples_per_window // 4) * 3)

plt.pcolormesh(time, freq, np.abs(Zxx), shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

input("Press Enter to finish")
