import numpy as np
import simpleaudio
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100

def main():
    # Generates a 440Hz (A4) note for 2 seconds
    seconds = 2

    time = np.linspace(0, seconds, seconds * SAMPLE_RATE, False)
    note = np.sin(440 * time * 2 * np.pi)

    plot_wave(time, note)
    play_note(note)

# Plots the note against time, on a graph
def plot_wave(time, note):
    plt.plot(time, note) 
    plt.show()

# Plays the note as sound
def play_note(note):
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16)

    play_obj = simpleaudio.play_buffer(audio, 1, 2, SAMPLE_RATE)

    play_obj.wait_done()

if __name__ == "__main__":
    main()