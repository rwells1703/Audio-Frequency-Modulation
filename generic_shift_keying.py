import numpy as np

import waves

MAX_FREQ = 3000
MIN_FREQ = 1400
FREQ_STEP = 100
FREQ_TOLERANCE = 45

# Example shift keying (binary shift key modulation on all of: amplitude, frequency and phase)
#shift_key_possibilites = {"a":[1,0.1], "f":[80,120], "p":[-1,1]}
shift_key_possibilites = {"a":[1], "f":range(MIN_FREQ, MAX_FREQ, FREQ_STEP), "p":[1]}

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

# Performs generic shift keying
def shift_keying(data, segment_time):
    wave = []
    
    # Generate a list of shift key values
    shift_key_values = generate_shift_key_values(shift_key_possibilites)

    # Loop through the input data
    for d in data:
        # Get amplitude, frequency and phase values for that section of wave
        amplitude = shift_key_values[d]["a"]
        frequency = shift_key_values[d]["f"]
        phase = shift_key_values[d]["p"]

        # Generate that section of wave
        wave_segment = waves.generate_wave(segment_time, frequency, amplitude, phase)
        
        wave = waves.combine_waves(wave, wave_segment)

    return wave

# Finds the correct integer data point for a given approximate frequency
def match_frequency(target):
    # Generate a list of shift key values
    shift_key_values = generate_shift_key_values(shift_key_possibilites)

    frequencies = extract_values_from_array_of_dicts(shift_key_values, "f")
    differences = np.abs(frequencies - target)
    smallest_difference_index = differences.argmin()

    if (differences[smallest_difference_index] > FREQ_TOLERANCE):
        return None
    
    return smallest_difference_index
    
# Iteratively apply a function to an array of dictionaries, editing a certain key value in each one
# E.g. add 1 to the "age" key, for an array of dictionaries representing people
def apply_func_to_array_of_dicts(dict_array, key, function):
    output = []

    for dict in dict_array:
        dict[key] = function(dict[key])
        output.append(dict)

    return output

# Iterate through an array of dictionaries, extracting a certain key value from each one into an output array
# E.g. get "age" key, for an array of dictionaries representing people
def extract_values_from_array_of_dicts(dict_array, key):
    output = []

    for dict in dict_array:
        output.append(dict[key])

    return output