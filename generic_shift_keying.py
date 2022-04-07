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

# Performs generic shift keying
def shift_keying(data, segment_time):
    wave = []

    # Loop through the input data
    for d in data:
        # Get amplitude, frequency and phase values for that section of wave
        amplitude = shift_key_values[d]["a"]
        frequency = shift_key_values[d]["f"]
        phase = shift_key_values[d]["p"]

        # Generate that section of wave
        wave_segment = utils.generate_wave(segment_time, frequency, amplitude, phase)
        wave = utils.combine_waves(wave, wave_segment)

    return wave