import numpy as np
import simpleaudio
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100

def main():
    time, amplitude = default_wave(2, 440)

    plot_wave(time, amplitude)
    play_wave(amplitude)

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency):
    time = np.linspace(0, seconds, seconds * SAMPLE_RATE, False)
    amplitude = np.sin(frequency * time * 2 * np.pi)
    
    return time, amplitude

# Plots the note against time, on a graph
def plot_wave(time, note):
    plt.plot(time, note) 
    plt.show()

# Plays the note as sound
def play_wave(note):
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16)

    play_obj = simpleaudio.play_buffer(audio, 1, 2, SAMPLE_RATE)

    play_obj.wait_done()

if __name__ == "__main__":
    main()