import numpy as np
import sounddevice as sd
import time

import constants

def start():
    stream_play = sd.OutputStream(
        samplerate=constants.SAMPLE_RATE,
        channels=constants.CHANNELS)

    stream_record = sd.InputStream(
        samplerate=constants.SAMPLE_RATE,
        channels=constants.CHANNELS,
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

def read_audio(stream):
    data = stream.read(constants.RECORDING_BLOCK_SIZE)[0]

    return data

# Records the microphone input as a wave and outputs the data as bytes
def record_audio(stream, seconds, log=True):
    if log:
        print("Started recording")
    
    data = b''

    # Take the specified number of recording chunks
    for i in range(0, int(constants.SAMPLE_RATE / constants.RECORDING_BLOCK_SIZE * seconds)):
        # Read the audio frame from the stream
        with stream:
            frame = stream.read(constants.RECORDING_BLOCK_SIZE)
        # Write the frame to frame list
        data += frame

    if log:
        print("Stopped recording")

    #return data[47042:]
    return data