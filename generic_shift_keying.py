import utils

# Characteristics of the carrier wave
carrier_values = {"a":1, "f":5, "p":1}

# Example shift keying (binary shift key modulation on all of: amplitude, frequency and phase)
#shift_key_possibilites = {"a":[1,0.1], "f":[80,120], "p":[-1,1]}
shift_key_possibilites = {"a":[1], "f":range(150,9999,20), "p":[1]}

shift_key_values = utils.generate_shift_key_values(shift_key_possibilites)

utils.display_shift_key_values(shift_key_values)

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