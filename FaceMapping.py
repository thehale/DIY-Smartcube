from typing import List

from tones.mixer import Mixer
from tones import SINE_WAVE
from playsound import playsound


class AbsolutePositioning:

    def __init__(self):
        self.state_to_freq = {}
        self.freq_to_state = {}
        file = open("absolute_positioning.txt")
        lines = file.readlines()
        for line in lines:
            parts = line.split(" ")
            self.state_to_freq[parts[0]] = float(parts[1])
            self.freq_to_state[float(parts[1])] = parts[0]

        self.state = {'U': 3, "D": 3, "F": 3, "B": 3, "R": 3, "L": 3}
        for k, v in self.state_to_freq.items():  # Included to double check proper reading of the file.
            print("%s %s" % (k, v))
        self.mixer = Mixer(44100, 1)
        self.mixer.create_track('U', SINE_WAVE, attack=0.01, decay=0.1)
        self.mixer.create_track('D', SINE_WAVE, attack=0.01, decay=0.1)
        self.mixer.create_track('F', SINE_WAVE, attack=0.01, decay=0.1)
        self.mixer.create_track('B', SINE_WAVE, attack=0.01, decay=0.1)
        self.mixer.create_track('R', SINE_WAVE, attack=0.01, decay=0.1)
        self.mixer.create_track('L', SINE_WAVE, attack=0.01, decay=0.1)

    def appendStateToSound(self, tps: float):
        self.mixer.add_tone('U', self.state_to_freq['U' + str(self.state['U'])], 1 / tps)
        self.mixer.add_tone('D', self.state_to_freq['D' + str(self.state['D'])], 1 / tps)
        self.mixer.add_tone('F', self.state_to_freq['F' + str(self.state['F'])], 1 / tps)
        self.mixer.add_tone('B', self.state_to_freq['B' + str(self.state['B'])], 1 / tps)
        self.mixer.add_tone('R', self.state_to_freq['R' + str(self.state['R'])], 1 / tps)
        self.mixer.add_tone('L', self.state_to_freq['L' + str(self.state['L'])], 1 / tps)

    def getState(self, detected_freqs: List[float]) -> List[str]:
        detected_states = set()
        for d_freq in detected_freqs:
            for s_freq in self.freq_to_state.keys():
                if abs(d_freq - s_freq) < 50:
                    detected_states.add(self.freq_to_state[s_freq])
        detected_states = list(detected_states)
        detected_states.sort()
        return detected_states


    def printState(self):
        print(' U' + str(self.state['U']) +
              ' D' + str(self.state['D']) +
              ' F' + str(self.state['F']) +
              ' B' + str(self.state['B']) +
              ' R' + str(self.state['R']) +
              ' L' + str(self.state['L']))

    def playSound(self):
        # Mix all tracks into a single list of samples and write to .wav file
        self.mixer.write_wav('tones.wav')
        playsound('tones.wav')
        #Addition
        y = self.mixer.mix()
        x = [i for i in range(len(y))]
        import matplotlib.pyplot as plt
        plt.plot([x, y])
        plt.show()
        #/Addition

    def transmitAlg(self, alg: str, tps: float):
        moves = alg.split(" ")
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
            self.appendStateToSound(tps=tps)
            self.printState()

    def receiveAlg(self, wav) -> str:
        """
        Parses the moves out of the given wav file.
        """
    
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


# pos = AbsolutePositioning()
# pos.transmitAlg("U U U U D D D D R R R R L L L L F F F F B B B B", 1.5)
# pos.playSound()
# pos.parseAlg("U U U U", 2)
# pos.playSound()
# pos.parseAlg("D D D D", 2)
# pos.playSound()
# pos.parseAlg("R R R R", 2)
# pos.playSound()
# pos.parseAlg("L L L L", 2)
# pos.playSound()
# pos.parseAlg("F F F F", 2)
# pos.playSound()
# pos.parseAlg("B B B B", 2)
# pos.playSound()
