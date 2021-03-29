from typing import List

from tones.mixer import Mixer
from tones import SINE_WAVE
from playsound import playsound

from scipy import signal
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

from Logger import Logger


class AuditorySupercube:

    def __init__(self, wav_path, window_size=5, stdv=1, alt_min=50, threshold_function=None):
        self.wav_path = wav_path
        self.log = Logger(wav_path.split("/")[1])
        self.window_size = window_size
        self.stdv = stdv
        self.alt_min = alt_min
        self.compute_threshold = threshold_function if threshold_function else self.default_compute_threshold
        self.__mixer = None
        self.state_to_freq = {}
        self.freq_to_state = {}
        file = open("absolute_positioning.txt")
        lines = file.readlines()
        for line in lines:
            parts = line.split(" ")
            self.state_to_freq[parts[0]] = float(parts[1])
            self.freq_to_state[float(parts[1])] = parts[0]

        self.state = {'U': 0, "D": 0, "F": 0, "B": 0, "R": 0, "L": 0}
        for k, v in self.state_to_freq.items():  # Included to double check proper reading of the file.
            print("%s %s" % (k, v))

    def __str__(self):
        return ' U' + str(self.state['U']) + \
               ' D' + str(self.state['D']) + \
               ' F' + str(self.state['F']) + \
               ' B' + str(self.state['B']) + \
               ' R' + str(self.state['R']) + \
               ' L' + str(self.state['L'])

    def U(self):
        self.state['U'] = (self.state['U'] + 1) % 4

    def D(self):
        self.state['D'] = (self.state['D'] + 1) % 4

    def F(self):
        self.state['F'] = (self.state['F'] + 1) % 4

    def B(self):
        self.state['B'] = (self.state['B'] + 1) % 4

    def R(self):
        self.state['R'] = (self.state['R'] + 1) % 4

    def L(self):
        self.state['L'] = (self.state['L'] + 1) % 4

    def Uprime(self):
        self.state['U'] = (self.state['U'] + 3) % 4

    def Dprime(self):
        self.state['D'] = (self.state['D'] + 3) % 4

    def Fprime(self):
        self.state['F'] = (self.state['F'] + 3) % 4

    def Bprime(self):
        self.state['B'] = (self.state['B'] + 3) % 4

    def Rprime(self):
        self.state['R'] = (self.state['R'] + 3) % 4

    def Lprime(self):
        self.state['L'] = (self.state['L'] + 3) % 4

    def apply_alg(self, alg: str, tps: float, simulation: bool = False):
        moves = alg.split(" ")
        if simulation:  # Represent the initial cube state
            if not self.__mixer:
                self.__create_mixer()
            for i in range(0, 5):
                self.__append_state_to_mixer(tps=tps)
        for move in moves:
            if move == "U":
                self.U()
            if move == "D":
                self.D()
            if move == "F":
                self.F()
            if move == "B":
                self.B()
            if move == "R":
                self.R()
            if move == "L":
                self.L()
            if move == "U'":
                self.Uprime()
            if move == "D'":
                self.Dprime()
            if move == "F'":
                self.Fprime()
            if move == "B'":
                self.Bprime()
            if move == "R'":
                self.Rprime()
            if move == "L'":
                self.Lprime()
            if simulation:
                self.__append_state_to_mixer(tps=tps)
            self.log.info(self)

    def play_simulation(self, silent: bool = False):
        # Mix all tracks into a single list of samples and write to .wav file
        if self.__mixer:
            self.__mixer.write_wav('tones.wav')
            if not silent:
                playsound('tones.wav')
        else:
            self.log.error("No simulation to play")

    def __create_mixer(self):
        self.__mixer = Mixer(44100, 1)
        self.__mixer.create_track('U', SINE_WAVE, attack=0.01, decay=0.1)
        self.__mixer.create_track('D', SINE_WAVE, attack=0.01, decay=0.1)
        self.__mixer.create_track('F', SINE_WAVE, attack=0.01, decay=0.1)
        self.__mixer.create_track('B', SINE_WAVE, attack=0.01, decay=0.1)
        self.__mixer.create_track('R', SINE_WAVE, attack=0.01, decay=0.1)
        self.__mixer.create_track('L', SINE_WAVE, attack=0.01, decay=0.1)

    def __append_state_to_mixer(self, tps: float):
        self.__mixer.add_tone('U', self.state_to_freq['U' + str(self.state['U'])], 1 / tps)
        self.__mixer.add_tone('D', self.state_to_freq['D' + str(self.state['D'])], 1 / tps)
        self.__mixer.add_tone('F', self.state_to_freq['F' + str(self.state['F'])], 1 / tps)
        self.__mixer.add_tone('B', self.state_to_freq['B' + str(self.state['B'])], 1 / tps)
        self.__mixer.add_tone('R', self.state_to_freq['R' + str(self.state['R'])], 1 / tps)
        self.__mixer.add_tone('L', self.state_to_freq['L' + str(self.state['L'])], 1 / tps)

    def extract_alg_from_audio(self):
        state_over_time = self.__extract_state_over_time(self.wav_path)
        alg = self.extract_alg_from_state_over_time(state_over_time)
        return alg

    @staticmethod
    def default_compute_threshold(spectrogram_slice, pct_of_stdv: float = 1, alt_min=50):
        """
        The default approach to computing the threshold value to use for identifying face turn frequencies.

        Returns the standard deviation of the spectrogram slice or 50, whichever is higher.
        :param spectrogram_slice: The slice of the spectrogram to analyze.
        :param pct_of_stdv: A saaling factor for the standard deviation
        :param alt_min: The smallest possible threshold to return
        :return:
        """
        return max(np.std(spectrogram_slice) * pct_of_stdv, alt_min)

    def __extract_state_over_time(self, wav_path):
        SAMPLES_PER_WINDOW = 1024  # Seems to be a good number to balance frequency precision with time precision.
        sample_rate, audio_samples = wavfile.read(wav_path)
        freq, time, Zxx = signal.stft(audio_samples,
                                      fs=sample_rate,
                                      nperseg=SAMPLES_PER_WINDOW,
                                      noverlap=(SAMPLES_PER_WINDOW // 4) * 3)
        # Determine the frequencies of interest
        spectrogram = np.abs(Zxx).transpose()
        # Show off a spectrogram of the detected audio
        # plt.pcolormesh(time, freq, np.abs(Zxx), shading='gouraud')
        # plt.title('STFT Magnitude')
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.show()
        state_over_time = []
        for time_idx in range(len(time)):
            important_freqs = []
            threshold = self.compute_threshold(spectrogram[time_idx], self.stdv, self.alt_min)
            # Save an image of the current strength of the frequency slice.
            # plt.plot(freq, spectrogram[time_idx])
            # plt.axhline(threshold, color='red')
            # plt.axis([0, 20000, 0, np.amax(spectrogram)])
            # plt.title(f"Frequencies at {time[time_idx]:.2f} seconds")
            # plt.ylabel("Strength")
            # plt.xlabel("Frequency [Hz]")
            # plt.savefig(f"./plt/{time[time_idx]:.2f}.png")
            # plt.clf()
            for freq_idx in range(len(freq)):
                if spectrogram[time_idx][freq_idx] > threshold:
                    important_freqs.append((freq[freq_idx], spectrogram[time_idx][freq_idx]))
            if len(important_freqs) > 0:
                detected_states = self.get_state_from_freq(important_freqs)
                state_over_time.append((time[time_idx], detected_states))
                self.log.info(f"At time {time[time_idx]:.6f} the states {detected_states} were detected.") # based on the "
                      # f"{len(important_freqs)} frequencies {important_freqs} that surpassed the threshold.")
        return state_over_time

    def get_state_from_freq(self, detected_freqs: List[float]) -> List[str]:
        detected_states = {}
        strongest_state = {
            "U": 0,
            "D": 0,
            "R": 0,
            "L": 0,
            "F": 0,
            "B": 0,
        }
        for d_freq, power in detected_freqs:
            for s_freq in self.freq_to_state.keys():
                if abs(d_freq - s_freq) < 40:
                    state = self.freq_to_state[s_freq]
                    face = state[0]
                    rotation = int(state[1])
                    if power > strongest_state[face]:
                        detected_states[face] = rotation
                        strongest_state[face] = power
        return detected_states

    def extract_alg_from_state_over_time(self, state_over_time):
        useful_states = [x for x in state_over_time if 'ERR' not in x[1]]
        num_useful_states = len(useful_states)
        window_size = self.window_size
        current_state = useful_states[0][1]
        alg = ""
        for idx in range(0, num_useful_states - window_size):  # Iterate over batches of size `window_size`
            for face in ["U", "D", "F", "B", "R", "L"]:
                candidate_state = -1
                confidence = 0
                rotation = 0
                for state in useful_states[idx : idx + window_size]:
                    if face in state[1]:
                        if state[1][face] == candidate_state:
                            confidence += 1
                        else:
                            candidate_state = state[1][face]
                            confidence = 1
                if confidence >= window_size:  # If all the states in the window are the same
                    if face in current_state:  # If we've already determined the starting position
                        rotation = candidate_state - current_state[face]  # Calculate the rotation
                    current_state[face] = candidate_state
                    if rotation == 1:  # Next state up
                        alg += " " + face
                    elif rotation == -1:  # Next state down
                        alg += " " + face + "'"
                    elif rotation == -3:  # Next state up with wrap-around
                        alg += " " + face
                    elif rotation == 3:  # Next state down with wrap-around
                        alg += " " + face + "'"
        return alg
