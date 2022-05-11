from re import I
import numpy as np

import constants
import waves

# Example shift keying (binary shift key modulation on all of: amplitude, frequency and phase)
shift_key_possibilites = {"a":[1], "f":constants.CLIPPED_FREQ_RANGE, "p":[1]}

#print(shift_key_possibilites)

# From a given set of possible values, generate a list of shift key values
def generate_shift_key_values(shift_key_possibilites):
    shift_key_values = []

    # Iterate through all possible variations of the given values
    for amplitude in shift_key_possibilites["a"]:
        for frequency in shift_key_possibilites["f"]:
            for phase in shift_key_possibilites["p"]:
                # Add this variation to the list
                shift_key_values.append({"a":amplitude, "f":frequency, "p":phase})

    return shift_key_values

# Display all the possible shift key values
def display_shift_key_values(shift_key_values):
    for v in range(0,len(shift_key_values)):
        print(v, shift_key_values[v])

# Performs shift keying on amplitude, frequency and phase concurrently
def ints_to_wave(ints, segment_time):
    wave = []
    
    # Generate a list of shift key values
    shift_key_values = generate_shift_key_values(shift_key_possibilites)

    # Loop through the input data
    for i in ints:
        # Get amplitude, frequency and phase values for that section of wave
        amplitude = shift_key_values[i]["a"]
        frequency = shift_key_values[i]["f"]
        phase = shift_key_values[i]["p"]

        # Generate that section of wave and append it to the overall wave
        wave_segment = waves.generate_wave(segment_time, frequency, amplitude, phase)
        wave = waves.combine_waves(wave, wave_segment)

    return wave

# Takes a chunk of audio data, and gets the integer value it corresponds to
def wave_to_int(wave):
    frequencies, fourier_wave = waves.generate_fourier_wave(wave)

    freq_max = get_loudest_frequency(frequencies, fourier_wave)

    '''if clip_frequency(freq_max):
        return None'''
    
    int_value = match_frequency(freq_max)
    #print(int_value, " = ", freq_max)

    return int_value

# Returns the loudest frequency present from the fourier transform
def get_loudest_frequency(frequencies, fourier_wave):
    return frequencies[np.argmax(fourier_wave)]

# Finds the correct integer data point for a given approximate frequency
def match_frequency(frequency):
    # Generate a list of shift key values
    shift_key_values = generate_shift_key_values(shift_key_possibilites)

    # Get the possible frequencies as a list
    frequencies = extract_values_from_array_of_dicts(shift_key_values, "f")

    # Get the corresponding integer value for that frequency
    int_values_matched = np.where(frequencies == frequency)[0]
    if len(int_values_matched) > 0:
        return int_values_matched[0]

    # No integer value matches this frequency
    return None

# Iterate through an array of dictionaries, extracting a certain key value from each one into an output array
# E.g. get "age" key, for an array of dictionaries representing people
def extract_values_from_array_of_dicts(dict_array, key):
    output = []

    for dict in dict_array:
        output.append(dict[key])

    return output

# Iteratively apply a function to an array of dictionaries, editing a certain key value in each one
# E.g. add 1 to the "age" key, for an array of dictionaries representing people
def apply_func_to_array_of_dicts(dict_array, key, function):
    output = []

    for dict in dict_array:
        dict[key] = function(dict[key])
        output.append(dict)

    return output

# Check to see if a detected value has been detected a several times recently
# if it is recurring, store it as it is probably being deliberately sent
def check_sent_deliberately(int_value, int_stream_raw):
    # Calculate the total proportion of recently received values (within a given sample size)
    # that are equal to the target value
    target_value_count = int_stream_raw[-constants.CERTAINTY_SAMPLE_SIZE:].count(int_value)

    # If the amount of values equal to the target value is above a threshold "CERTAINTY", the value was sent deliberately so store it
    if target_value_count >= constants.CERTAINTY:
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
    #if frequency > constants.MAX_FREQ + constants.FREQ_TOLERANCE or frequency < constants.MIN_FREQ - constants.FREQ_TOLERANCE:
    if frequency > constants.MAX_FREQ or frequency < constants.MIN_FREQ:
        return True

    return False