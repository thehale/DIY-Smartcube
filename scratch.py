from tones.mixer import Mixer
from tones import SINE_WAVE
from playsound import playsound

mixer = Mixer(44100, 0.5)

mixer.create_track(1, SINE_WAVE, attack=0.01, decay=0.1)

mixer.add_tone(1, 799.872020476724, .5)
mixer.add_tone(1, 899.604174163368, .5)
mixer.add_tone(1, 1000.40016006403, .5)
mixer.add_tone(1, 1100.5943209333, .5)
mixer.add_tone(1, 1301.06687483737, .5)
mixer.add_tone(1, 1400.56022408964, .5)
mixer.add_tone(1, 1500.60024009604, .5)
mixer.add_tone(1, 1601.53747597694, .5)
mixer.add_tone(1, 1799.20834832674, .5)
mixer.add_tone(1, 1899.69604863222, .5)
mixer.add_tone(1, 2000.80032012805, .5)
mixer.add_tone(1, 2100.84033613445, .5)
mixer.add_tone(1, 2296.73863114378, .5)
mixer.add_tone(1, 2396.93192713327, .5)
mixer.add_tone(1, 2497.5024975025, .5)
mixer.add_tone(1, 2597.4025974026, .5)
mixer.add_tone(1, 2801.12044817927, .5)
mixer.add_tone(1, 2903.60046457607, .5)
mixer.add_tone(1, 3001.20048019208, .5)
mixer.add_tone(1, 3105.5900621118, .5)
mixer.add_tone(1, 3306.87830687831, .5)
mixer.add_tone(1, 3401.36054421769, .5)
mixer.add_tone(1, 3501.40056022409, .5)
mixer.add_tone(1, 3607.50360750361, .5)

mixer.write_wav('tones.wav')
playsound('tones.wav')

#Addition
import wave
import numpy as np
import matplotlib.pyplot as plt

spf = wave.open('tones.wav')

signal = spf.readframes(-1)
signal = np.fromstring(signal, "Int16")

plt.plot(signal)
plt.show()
#/Addition