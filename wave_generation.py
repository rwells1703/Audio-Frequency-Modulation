import numpy as np
import simpleaudio
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100

def main():
    time, amplitude = generate_dual_freq_wave(3, 10, 5)

    plot_wave(time, amplitude)
    #play_wave(amplitude)

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency):
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    amplitude = np.sin(frequency * time * 2 * np.pi)
    
    return time, amplitude

# Generates two sine waves of different frequencies and appends them along the time axis
def generate_dual_freq_wave(seconds, frequency1, frequency2):
    time1, wave1 = generate_wave(seconds/2, frequency1)
    time2, wave2 = generate_wave(seconds/2, frequency2)
    
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    note = np.append(wave1, wave2)

    return time, note

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