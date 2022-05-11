import numpy as np

import constants
import waves

# Display all the possible shift key values
def display_shift_key_values(shift_key_values):
    for v in range(0,len(shift_key_values)):
        print(v, shift_key_values[v])

# Performs shift keying on amplitude, frequency and phase concurrently
def ints_to_wave(ints):
    wave = []

    # Loop through the input data
    for i in ints:
        # Get frequency values for that section of wave
        frequency = constants.MFSK_FREQ_RANGE[i]

        # Generate that section of wave and append it to the overall wave
        wave_segment = waves.generate_wave(frequency, 1, 1, constants.MFSK_SEGMENT_TIME)
        wave = waves.combine_waves(wave, wave_segment)

    return wave

# Takes a chunk of audio data, and gets the integer value it corresponds to
def wave_to_int(wave):
    frequencies, fourier_wave = waves.generate_fourier_wave(wave)

    freq_max = get_loudest_frequency(frequencies, fourier_wave)

    if clip_frequency(freq_max):
        return None
    
    int_value = match_frequency(freq_max)

    return int_value

# Returns the loudest frequency present within the fourier fransform
def get_loudest_frequency(frequencies, fourier_wave):
    return frequencies[np.argmax(fourier_wave)]

# Returns the n loudest frequencies present within the fourier fransform
def get_loudest_frequencies(frequencies, fourier_wave, n):
    sorted_inds = np.argsort(fourier_wave)
    sorted_freqs = np.flip(frequencies[sorted_inds].astype(int))

    # Round the frequencies to the nearest 100
    rounded_freqs = list(map(lambda f : round(f, -2), sorted_freqs))

    # Remove any duplicated occurences of frequencies
    # these occur when there are several similar frequencies in the loudest frequency list
    # which are then rounded to the same value
    unique_freqs = []
    i = 0
    c = n
    while i < len(rounded_freqs) and c > 0:
        if not rounded_freqs[i] in unique_freqs:
            unique_freqs.append(rounded_freqs[i])
            c -= 1
        i += 1

    return unique_freqs

# Finds the correct integer data point for a given approximate frequency
def match_frequency(frequency):
    # Get the corresponding integer value for that frequency
    int_values_matched = np.where(constants.MFSK_FREQ_RANGE == frequency)[0]
    if len(int_values_matched) > 0:
        return int_values_matched[0]

    # No integer value matches this frequency
    return None

# Check to see if a detected value has been detected a several times recently
# if it is recurring, store it as it is probably being deliberately sent
def check_sent_deliberately(int_value, int_stream_raw, certainty, certainy_sample_size):
    # Calculate the total proportion of recently received values (within a given sample size)
    # that are equal to the target value
    target_value_count = int_stream_raw[-certainy_sample_size:].count(int_value)

    # If the amount of values equal to the target value is above a threshold "certainty", the value was sent deliberately so store it
    if target_value_count >= certainty:
        return True
    
    # The value was probably a result of random noise
    return False

# Only store values that are not identical to the value directly preceding them
# This should never occur as after each value is sent, a "gap" value is also sent
def check_not_added(int_value, int_stream):
    if len(int_stream) == 0:
        # If there are no values stored
        return True
    elif int_stream[-1] != int_value:
        # If the previous value has not already been stored
        return True

    # The value is already stored
    return False

# Rejects any frequency higher or lower than the clipping bounds
def clip_frequency(frequency):
    if frequency > constants.MFSK_MAX_FREQ or frequency < constants.MFSK_MIN_FREQ:
        return True

    return False