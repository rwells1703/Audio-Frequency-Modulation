import simpleaudio
import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency, amplitude, phase):
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    wave = np.sin(frequency * time * 2 * np.pi) * amplitude * phase
    
    return wave

# Appends many wave segments together
def combine_waves(waves):
    return np.append([], waves)

# Generate a time axis for a given amount of wave segments
def generate_time_axis(segment_time, segment_count):
    return np.linspace(0, segment_time*segment_count, (np.ceil(segment_time * SAMPLE_RATE) * segment_count).astype(int), False)

# Plots the wave against time, on a graph
def plot_wave(time, wave):
    plt.plot(time, wave) 
    plt.show()

# Plays the wave as sound
def play_wave(wave):
    audio = wave * (2**15 - 1) / np.max(np.abs(wave))
    audio = audio.astype(np.int16)

    play_obj = simpleaudio.play_buffer(audio, 1, 2, SAMPLE_RATE)

    play_obj.wait_done()