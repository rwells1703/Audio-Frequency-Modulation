import numpy as np
import sounddevice as sd
import time

import constants
import waves

# Initialise the audio streams
def start(recording_block_size):
    stream_play = sd.OutputStream(
        samplerate=constants.SAMPLE_RATE,
        channels=constants.CHANNELS)

    stream_record = sd.InputStream(
        samplerate=constants.SAMPLE_RATE,
        channels=constants.CHANNELS,
        dtype=constants.FORMAT_RECORD,
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
def record_audio(stream, seconds, log=True):
    if log:
        print("Started recording")
    
    wave = []

    # Take the specified number of recording chunks
    for i in range(0, int(constants.SAMPLE_RATE / constants.RECORDING_BLOCK_SIZE * seconds)):
        # Write the frame to the data
        wave = waves.combine_waves(wave, read_wave(stream))

    if log:
        print("Stopped recording")

    return wave