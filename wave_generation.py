import numpy as np
import simpleaudio
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100

def main():
    time, amplitude = phase_shift_keying([0,1,1,0,0,0,0,0,1,0,1,1,1,0,0,1,1,1,1])

    plot_wave(time, amplitude)
    play_wave(amplitude)

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency, amplitude_coef):
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    amplitude = np.sin(frequency * time * 2 * np.pi) * amplitude_coef
    
    return time, amplitude

# Generates two sine waves of different frequencies and appends them along the time axis
def generate_dual_freq_wave(seconds, frequency1, frequency2):
    time1, wave1 = generate_wave(seconds/2, frequency1, 1)
    time2, wave2 = generate_wave(seconds/2, frequency2, 1)
    
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    note = np.append(wave1, wave2)

    return time, note

# Generates a waveform using Amplitude Shift Keying
def amplitude_shift_keying(bits, bit_time=0.2, high_amp=1, frequency=440):
    waves = []

    for b in bits:
        if b == 0:
            # Generate a flat line for a 0
            time_divisions = np.ceil(bit_time * SAMPLE_RATE).astype(int)
            wave = np.full(time_divisions, 0)
        else:
            # Generate a wave for a 1
            time_slice, wave = generate_wave(bit_time, frequency, high_amp)

        waves.append(wave)
    
    time = np.linspace(0, bit_time*len(bits), np.ceil(bit_time*len(bits) * SAMPLE_RATE).astype(int), False)
    note = np.append([], waves)

    return time, note

# Generates a waveform using Frequency Shift Keying
def frequency_shift_keying(bits, bit_time=0.2, low_freq=440, high_freq=523.25, amplitude=1):
    waves = []

    for b in bits:
        if b == 0:
            # Generate a low frequency wave for a 0
            frequency = low_freq
        else:
            # Generate a high frequency wave for a 1
            frequency = high_freq

        time_slice, wave = generate_wave(bit_time, frequency, amplitude)
        waves.append(wave)
    
    time = np.linspace(0, bit_time*len(bits), np.ceil(bit_time*len(bits) * SAMPLE_RATE).astype(int), False)
    note = np.append([], waves)

    return time, note

# Generates a waveform using Phase Shift Keying
def phase_shift_keying(bits, bit_time=0.2, frequency=440, amplitude=1):
    waves = []

    for b in bits:
        if b == 0:
            # Generate an in phase wave for a 0
            phase = 1
        else:
            # Generate an out of phase wave for a 1
            phase = -1

        time_slice, wave = generate_wave(bit_time, frequency, amplitude * phase)
        waves.append(wave)
    
    time = np.linspace(0, bit_time*len(bits), np.ceil(bit_time*len(bits) * SAMPLE_RATE).astype(int), False)
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

if __name__ == "__main__":
    main()