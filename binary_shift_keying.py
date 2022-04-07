import numpy as np

import utils

# Generates a waveform using Amplitude Shift Keying
def amplitude_shift_keying(bits, bit_time=0.2, high_amp=1, frequency=440):
    waves = []

    for b in bits:
        if b == 0:
            # Generate a flat line for a 0
            time_divisions = np.ceil(bit_time * utils.SAMPLE_RATE).astype(int)
            wave = np.full(time_divisions, 0)
        else:
            # Generate a wave for a 1
            time_slice, wave = utils.generate_wave(bit_time, frequency, high_amp)

        waves.append(wave)
    
    return utils.combine_waves(waves, bit_time*len(bits))

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

        time_slice, wave = utils.generate_wave(bit_time, frequency, amplitude)
        waves.append(wave)
    
    return utils.combine_waves(waves, bit_time*len(bits))

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

        time_slice, wave = utils.generate_wave(bit_time, frequency, amplitude * phase)
        waves.append(wave)
    
    return utils.combine_waves(waves, bit_time*len(bits))