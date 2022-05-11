import numpy as np
import sounddevice as sd
import time

import audio
import waves

# Define audio stream parameters
SAMPLE_RATE = 48000
CHANNELS = 1
FORMAT_RECORD = "int16"
RECORD_BITS = 16

# Initialise the audio streams
def start(recording_block_size):
    stream_play = sd.OutputStream(
        samplerate=audio.SAMPLE_RATE,
        channels=audio.CHANNELS)

    stream_record = sd.InputStream(
        samplerate=audio.SAMPLE_RATE,
        channels=audio.CHANNELS,
        dtype=audio.FORMAT_RECORD,
        blocksize=recording_block_size)

    time.sleep(0.1)
    stream_record.start()

    return stream_play, stream_record

# Reads the audio as a wave
def read_wave(stream, recording_block_size):
    wave = stream.read(recording_block_size)[0].flatten()

    return wave
    
# Plays the wave as sound
def play_wave(stream, wave):
    # Convert the wave to the correct format
    data = wave.astype(np.float32)

    # Write the data to the playback stream
    play_audio(stream, data)

# Plays audio data as bytes
def play_audio(stream, data):
    with stream:
        stream.write(data)

# Records the microphone audio
def record_audio(stream, seconds, recording_block_size, log=True):
    if log:
        print("Started recording")
    
    wave = []

    # Take the specified number of recording chunks
    for i in range(0, int(audio.SAMPLE_RATE / recording_block_size * seconds)):
        # Write the frame to the data
        wave = waves.combine_waves(wave, read_wave(stream))

    if log:
        print("Stopped recording")

    return wave