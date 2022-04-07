import utils

# Generates a waveform using Amplitude Shift Keying
def amplitude_shift_keying(bits, bit_time=0.2, high_amp=1, frequency=440, phase=1):
    wave = []

    for b in bits:
        if b == 0:
            wave_segment = utils.generate_flat_signal(0, bit_time)
        else:
            # Generate a wave for a 1
            wave_segment = utils.generate_wave(bit_time, frequency, high_amp, phase)

        wave = utils.combine_waves(wave, wave_segment)

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

        wave_segment = utils.generate_wave(bit_time, frequency, amplitude, phase)
        wave = utils.combine_waves(wave, wave_segment)

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

        wave_segment = utils.generate_wave(bit_time, frequency, amplitude, phase)
        wave = utils.combine_waves(wave, wave_segment)

    return wave