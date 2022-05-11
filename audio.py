import numpy as np
import sounddevice as sd
import time

import constants
import waves

def start():
    stream_play = sd.OutputStream(
        samplerate=constants.SAMPLE_RATE,
        channels=constants.AUDIO_CHANNELS)

    stream_record = sd.InputStream(
        samplerate=constants.SAMPLE_RATE,
        channels=constants.AUDIO_CHANNELS,
        dtype="int16",
        blocksize=constants.RECORDING_BLOCK_SIZE)

    time.sleep(0.1)
    stream_record.start()

    return stream_play, stream_record

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

# Reads the audio as a wave
def read_audio(stream):
    wave = stream.read(constants.RECORDING_BLOCK_SIZE)[0].flatten()

    return wave

# Records the microphone audio
def record_audio(stream, seconds, log=True):
    if log:
        print("Started recording")
    
    wave = []

    # Take the specified number of recording chunks
    for i in range(0, int(constants.SAMPLE_RATE / constants.RECORDING_BLOCK_SIZE * seconds)):
        # Write the frame to the data
        wave = waves.combine_waves(wave, read_audio(stream))

    if log:
        print("Stopped recording")

    return wave