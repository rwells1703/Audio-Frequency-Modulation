import numpy as np
import pyaudio

import constants

# Start the pyaudio library and a stream
def start_pyaudio():
    # Start pyaudio
    pyaudio_instance = pyaudio.PyAudio()

    # Create the stream for playing audio through the speakers
    stream_play = pyaudio_instance.open(format=constants.FORMAT_PLAY,
                    channels=constants.CHANNELS,
                    rate=constants.SAMPLE_RATE,
                    output=True)

    # Create the stream for recording audio from the microphone     
    stream_record = pyaudio_instance.open(format=constants.FORMAT_RECORD,
                channels=constants.CHANNELS,
                rate=constants.SAMPLE_RATE,
                frames_per_buffer=constants.RECORDING_CHUNK_SIZE,
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

# Plays audio data as bytes
def play_audio(stream, data):
    stream.write(data)

# Records the microphone input as a wave and outputs the data as bytes
def record_audio(stream, seconds, log=True):
    if log:
        print("Started recording")
    
    data = b''

    # Take the specified number of recording chunks
    for i in range(0, int(constants.SAMPLE_RATE / constants.RECORDING_CHUNK_SIZE * seconds)):
        # Read the audio frame from the stream
        frame = stream.read(constants.RECORDING_CHUNK_SIZE)
        # Write the frame to frame list
        data += frame

    if log:
        print("Stopped recording")

    #return data[47042:]
    return data