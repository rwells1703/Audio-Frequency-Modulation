import simpleaudio
import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency, amplitude_coef):
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    amplitude = np.sin(frequency * time * 2 * np.pi) * amplitude_coef
    
    return time, amplitude

# Appends many waves along the time axis
def combine_waves(waves, total_length):
    time = np.linspace(0, total_length, np.ceil(total_length * SAMPLE_RATE).astype(int), False)
    note = np.append([], waves)

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