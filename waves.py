import numpy as np
import struct

import constants

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency, amplitude, phase):
    time = np.linspace(0, seconds, np.ceil(seconds * constants.SAMPLE_RATE).astype(int), False)
    wave = np.sin(frequency * time * 2 * np.pi) * amplitude * phase
    return wave

# Appends one wave segment to the end of another
def combine_waves(wave1, wave2):
    return np.append(wave1, wave2)

# Generate a time axis for a given amount of wave segments
def generate_time_axis(segment_time, segment_count):
    return np.linspace(0, segment_time*segment_count, (np.ceil(segment_time * constants.SAMPLE_RATE) * segment_count).astype(int), False)

# Convert the binary string into a digital wave
def generate_digital_wave(binary_string):
    digital_wave = []

    # Duplicate the first value, otherwise the graph will be plotted incorrectly
    digital_wave.append(int(binary_string[0]))
    # Loop through the binary data and convert it into an array of ints
    for b in binary_string:
        digital_wave.append(int(b))
    
    return digital_wave

# Turn a square wave signal into a waveform
def generate_square_wave(data, segment_time):
    wave = []

    for d in data:
        wave_segment = generate_flat_signal(d, segment_time)
        wave = combine_waves(wave, wave_segment)

    return wave

# Generate a flat line signal
def generate_flat_signal(amplitude, segment_time):
    samples = np.ceil(segment_time * constants.SAMPLE_RATE).astype(int)
    flat_signal = np.full(samples, amplitude)

    return flat_signal

# Splits wave into equally sized (apart from the final) chunks of the segment time
def split_wave(wave, segment_time):
    wave_chunk_size = segment_time * constants.SAMPLE_RATE
    wave_split = np.array_split(wave, wave_chunk_size)

    return wave_split

# Convert a bytestring of wav audio data to a wave of integer values
def bytestring_audio_to_wave(data):
    int_tuples = struct.iter_unpack("H", data)
    wave = list(map(lambda t : t[0], int_tuples))

    return wave

# Transform a wave into its frequency and fourier components
def generate_fourier_wave(wave):
    fourier_wave = np.fft.fft(wave)
    frequency = np.fft.fftfreq(len(wave))
    
    return frequency, fourier_wave