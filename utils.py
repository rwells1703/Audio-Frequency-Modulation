import struct
import pyaudio
import wave as w
import numpy as np

# Define audio parameters
SAMPLE_RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORDING_CHUNK_SIZE = 1024

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

# Turn a square wave signal into a waveform
def generate_square_wave(data, segment_time):
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

# Start the pyaudio library and a stream
def start_pyaudio():
    # Start pyaudio
    pyaudio_instance = pyaudio.PyAudio()

    # Create the stream for playing audio through the speakers
    stream_play = pyaudio_instance.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    output=True)

    # Create the stream for recording audio from the microphone     
    stream_record = pyaudio_instance.open(format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                frames_per_buffer=RECORDING_CHUNK_SIZE,
                input=True)

    return pyaudio_instance, stream_play, stream_record

# Stop the stream, and the pyaudio library
def stop_pyaudio(pyaudio_instance, stream_play, stream_record):
    # Close both playing and recoding streams
    stream_play.stop_stream()
    stream_play.close()

    stream_record.stop_stream()
    stream_record.close()

    # Stop pyaudio
    pyaudio_instance.terminate()

# Plays the wave as sound
def play_wave(stream, wave):
    # Convert the wave to the correct format
    wave = wave.astype(np.float32).tobytes()

    # Write the data to the playback stream
    stream.write(wave)

# Records the microphone input as a wave and outputs the data as bytes
def record_audio(stream, seconds):
    print("Started recording")
    data = b''

    # Take the specified number of recording chunks
    for i in range(0, int(SAMPLE_RATE / RECORDING_CHUNK_SIZE * seconds)):
        # Read the audio frame from the stream
        frame = stream.read(RECORDING_CHUNK_SIZE)
        # Write the frame to frame list
        data += frame

    print("Stopped recording")

    return data[47042:]
    #return data

# Plays audio data as bytes
def play_audio(stream, data):
    stream.write(data)

# Save the recorded audio frames to a wav file
def save_audio_file(pyaudio_instance, frames):
    with w.open("sound.wav", 'wb') as file:
        # Set the parameters for the audio file
        file.setnchannels(CHANNELS)
        file.setsampwidth(pyaudio_instance.get_sample_size(FORMAT))
        file.setframerate(SAMPLE_RATE)
        file.writeframes(frames)

# Read the audio file and output the data in bytes
def read_audio_file():
    with w.open("sound.wav") as file:
        frame_number = file.getnframes()
        data = file.readframes(frame_number)

    return data

# Convert a bytestring of wav audio data to a list of integer values
def wav_data_to_wave(data):
    data_tuples = struct.iter_unpack("H", data)
    wave = list(map(lambda t : t[0], data_tuples))

    return wave

# Transform a wave into its frequency and fourier components
def generate_fourier_wave(wave):
    fourier_wave = np.fft.fft(wave)

    N = len(fourier_wave)
    n = np.arange(N)
    T = N/SAMPLE_RATE
    frequency = n/T
    
    return frequency, fourier_wave