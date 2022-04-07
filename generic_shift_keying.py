import utils

# Example 8 bit shift keying (binary shift key modulation on all of: amplitude, frequency and phase)
shift_key_values = [
    {"a":0.1, "f":523.25, "p":-1},
    {"a":1, "f":523.25, "p":-1},
    {"a":0.1, "f":440, "p":-1},
    {"a":1, "f":440, "p":-1},
    {"a":0.1, "f":523.25, "p":1},
    {"a":1, "f":523.25, "p":1},
    {"a":0.1, "f":440, "p":1},
    {"a":1, "f":440, "p":1}
]

# Characteristics of the carrier wave
carrier_values = {"a":1, "f":440, "p":1}

# Performs generic shift keying
def shift_keying(data, segment_time):
    waves = []

    # Loop through the input data
    for c in data:
        # Get amplitude, frequency and phase values for that section of wave
        amplitude = shift_key_values[c]["a"]
        frequency = shift_key_values[c]["f"]
        phase = shift_key_values[c]["p"]

        # Generate that section of wave
        wave_segment = utils.generate_wave(segment_time, frequency, amplitude, phase)
        waves.append(wave_segment)
    
    # Create a time axis
    time = utils.generate_time_axis(segment_time, len(waves))

    # Combine all wave sections
    wave = utils.combine_waves(waves)

    return time, wave