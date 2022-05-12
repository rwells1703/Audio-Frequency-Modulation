from matplotlib import pyplot as plt
import numpy as np

import audio
import waves

# Generates a waveform using Amplitude Shift Keying
def amplitude_shift_keying(bits, bit_time=0.2, high_amp=1, frequency=440, phase=1):
    wave = []

    for b in bits:
        if b == 0:
            wave_segment = waves.generate_flat_signal(0, bit_time)
        else:
            # Generate a wave for a 1
            wave_segment = waves.generate_wave(frequency, high_amp, phase, bit_time)

        wave = waves.combine_waves(wave, wave_segment)

    return wave

# Generates a waveform using Frequency Shift Keying
def frequency_shift_keying(bits, bit_time=0.2, low_freq=440, high_freq=523.25, amplitude=1, phase=1):
    wave = []

    for b in bits:
        if b == 0:
            # Generate a low frequency wave for a 0
            frequency = low_freq
        else:
            # Generate a high frequency wave for a 1
            frequency = high_freq

        wave_segment = waves.generate_wave(frequency, amplitude, phase, bit_time)
        wave = waves.combine_waves(wave, wave_segment)

    return wave

# Generates a waveform using Phase Shift Keying
def phase_shift_keying(bits, bit_time=0.2, frequency=440, amplitude=1):
    wave = []

    for b in bits:
        if b == 0:
            # Generate an in phase wave for a 0
            phase = 1
        else:
            # Generate an out of phase wave for a 1
            phase = -1

        wave_segment = waves.generate_wave(frequency, amplitude, phase, bit_time)
        wave = waves.combine_waves(wave, wave_segment)

    return wave

bits = [0,0,1,0,0,0,1,1,1,1,0,1,0,1,1]

digital_wave = waves.generate_digital_wave(bits)

time = waves.generate_time_axis(len(bits)*0.2, len(bits)*audio.SAMPLE_RATE*0.2)

ask_wave = amplitude_shift_keying(bits, frequency=10)
fsk_wave = frequency_shift_keying(bits, low_freq=10, high_freq=30)
psk_wave = phase_shift_keying(bits, frequency=10)

# Plot the waves on a graph
plt.subplot(4,1,1)
plt.step(range(0, len(digital_wave)), digital_wave)

plt.subplot(4,1,2)
plt.grid(axis = "y")
plt.plot(time, ask_wave)

plt.subplot(4,1,3)
plt.grid(axis = "y")
plt.plot(time, fsk_wave)

plt.subplot(4,1,4)
plt.grid(axis = "y")
plt.plot(time, psk_wave)

plt.show()