# Reference: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html

import os
import matplotlib.pyplot as plt

from scipy import signal
from scipy.io import wavfile
import numpy as np

from FaceMapping import AuditorySupercube

SAMPLES_PER_WINDOW = 1024  # Seems to be a good number to balance frequency precision with time precision.
THRESHOLD = 100  # The minimum value required for a frequency to be detected as present.


# Compute the Gabor transform on the affected audio
audio_path = "./output.wav"
sample_rate, audio_samples = wavfile.read(audio_path)
freq, time, Zxx = signal.stft(audio_samples,
                              fs=sample_rate,
                              nperseg=SAMPLES_PER_WINDOW,
                              noverlap=(SAMPLES_PER_WINDOW // 4) * 3)

# Determine the frequencies of interest
spectrogram = np.abs(Zxx)
face_mapping = AuditorySupercube()
for time_idx in range(len(time)):
    important_freqs = []
    for freq_idx in range(len(freq)):
        if spectrogram[freq_idx][time_idx] > THRESHOLD:
            important_freqs.append(freq[freq_idx])
    if len(important_freqs) > 0:
        detected_states = face_mapping.get_state_from_freq(important_freqs)
        print(f"At time {time[time_idx]:.6f} the states {detected_states} were detected based on the {len(important_freqs)} frequencies {important_freqs} that surpassed the threshold.")

# Show off a spectrogram of the detected audio
plt.pcolormesh(time, freq, np.abs(Zxx), shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

input("Press Enter to finish")
