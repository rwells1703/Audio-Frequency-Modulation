import data_conversion
import generic_shift_keying
import waves

import numpy as np
import pyaudio

# Define audio parameters
SAMPLE_RATE = 44100
FORMAT_PLAY = pyaudio.paFloat32
FORMAT_RECORD = pyaudio.paInt16
CHANNELS = 1
RECORDING_CHUNK_SIZE = 512

# Start the pyaudio library and a stream
def start_pyaudio():
    # Start pyaudio
    pyaudio_instance = pyaudio.PyAudio()

    # Create the stream for playing audio through the speakers
    stream_play = pyaudio_instance.open(format=FORMAT_PLAY,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    output=True)

    # Create the stream for recording audio from the microphone     
    stream_record = pyaudio_instance.open(format=FORMAT_RECORD,
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
def record_audio(stream, seconds, log=True):
    if log:
        print("Started recording")
    
    data = b''

    # Take the specified number of recording chunks
    for i in range(0, int(SAMPLE_RATE / RECORDING_CHUNK_SIZE * seconds)):
        # Read the audio frame from the stream
        frame = stream.read(RECORDING_CHUNK_SIZE)
        # Write the frame to frame list
        data += frame

    if log:
        print("Stopped recording")

    #return data[47042:]
    return data

# Plays audio data as bytes
def play_audio(stream, data):
    stream.write(data)

# Rejects any frequency higher or lower than the clipping bounds
def clip_frequency(frequency):
    if frequency > generic_shift_keying.MAX_FREQ + generic_shift_keying.FREQ_TOLERANCE or frequency < generic_shift_keying.MIN_FREQ - generic_shift_keying.FREQ_TOLERANCE:
        return True

    return False

# Splits audio into equally sized (apart from the final) chunks of the segment time
def split_audio(wave, segment_time):
    wave_chunk_size = segment_time * SAMPLE_RATE
    wave_split = np.array_split(wave, wave_chunk_size)

    return wave_split

# Takes a chunk of audio data, and gets the integer value it corresponds to
def extract_int_from_audio(data):
    int_data = data_conversion.raw_data_to_int(data)

    freq, fourier_wave = waves.generate_fourier_wave(int_data)

    freq_subset = freq[1:]
    fourier_wave_subset = np.abs(fourier_wave)[1:]

    freq_max = freq_subset[np.argmax(fourier_wave_subset)]

    if clip_frequency(freq_max):
        return None
    
    int_value = generic_shift_keying.match_frequency(freq_max)
    #print(int_value, " = ", freq_max)

    return int_value

# Interlace zeros between the integer values to symbolise the end of each symbol
def add_integers_stops(data):
    output = []

    for d in data:
        output.append(d)
        output.append(0)

    return output

# Remove interlaced zeros between the integer values to symbolise the end of each symbol
def remove_integers_stops(data):
    output = []

    for i in data:
        if i != 0:
            output.append(i)

    return output

# If it was sent deliberately, add a new int value to the incoming data stream
def add_to_int_stream(int_value, int_stream, int_stream_raw, sureness):
    # Potentially record value if it is not None
    if (int_value != None):
        int_stream_raw.append(int_value)
        #print(int_value)

    # If the last few values were identical, it is usually deliberate so record it
    if int_stream_raw[-sureness*2:].count(int_value) >= sureness:
        try:
            # Record only if the previous character has not already been recorded
            if int_stream[-1] != int_value:
                int_stream.append(int_value)
                #print(int_stream)
        except IndexError:
            int_stream.append(int_value)
            #print(int_stream)