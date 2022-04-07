import simpleaudio
import numpy as np

SAMPLE_RATE = 44100

# Generates a sine wave for a specified number of seconds
def generate_wave(seconds, frequency, amplitude, phase):
    time = np.linspace(0, seconds, np.ceil(seconds * SAMPLE_RATE).astype(int), False)
    wave = np.sin(frequency * time * 2 * np.pi) * amplitude * phase
    
    return wave

# Appends one wave segment to the end of another
def combine_waves(wave1, wave2):
    return np.append(wave1, wave2)

# Generate a time axis for a given amount of wave segments
def generate_time_axis(segment_time, segment_count):
    return np.linspace(0, segment_time*segment_count, (np.ceil(segment_time * SAMPLE_RATE) * segment_count).astype(int), False)

# Turn a digital signal into a waveform
def generate_digital_wave(data, segment_time):
    wave = []

    for d in data:
        wave_segment = generate_flat_signal(d, segment_time)
        wave = combine_waves(wave, wave_segment)

    return wave

# Generate a flat line signal
def generate_flat_signal(amplitude, segment_time):
    samples = np.ceil(segment_time * SAMPLE_RATE).astype(int)
    flat_signal = np.full(samples, amplitude)

    return flat_signal

# From a given set of possible values, generate a list of shift key values
def generate_shift_key_values(shift_key_possibilites):
    shift_key_values = []

    for amplitude in shift_key_possibilites["a"]:
        for frequency in shift_key_possibilites["f"]:
            for phase in shift_key_possibilites["p"]:
                shift_key_values.append({"a":amplitude, "f":frequency, "p":phase})

    return shift_key_values

# Display all the possible shift key values
def display_shift_key_values(shift_key_values):
    for v in range(0,len(shift_key_values)):
        print(v, shift_key_values[v])

# Plays the wave as sound
def play_wave(wave):
    audio = wave * (2**15 - 1) / np.max(np.abs(wave))
    audio = audio.astype(np.int16)

    play_obj = simpleaudio.play_buffer(audio, 1, 2, SAMPLE_RATE)

    play_obj.wait_done()