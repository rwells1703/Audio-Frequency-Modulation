import numpy as np
import simpleaudio
from matplotlib import pyplot as plt

#megan is the best person ever i love her so much 

SAMPLE_RATE = 44100

def main():
    time, amplitude = multi_freq_wave([0,1,1,0,1,0,1,1,1,0,0,1,1,0,1], 0.2)

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

# Generates an AM or FM wave based upon the input bit array
def multi_freq_wave(bits, bit_time):
    modulation = "FM"

    # Frequency values for FM
    low_freq = 523.25
    high_freq = 440
    
    # Amplitude values for AM
    low_amp = 0.01
    high_amp = 1
    
    # Default values
    amplitude = 1
    freq = 440

    waves = []
    for b in bits:
        if modulation == "AM":
            if b == 0:
                amplitude = low_amp
            else:
                amplitude = high_amp
        elif modulation == "FM":
            if b == 0:
                freq = low_freq
            else:
                freq = high_freq

        time_slice, wave = generate_wave(bit_time, freq, amplitude)
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