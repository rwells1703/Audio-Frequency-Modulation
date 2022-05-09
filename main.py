from matplotlib import pyplot as plt
import numpy as np
from sys import argv

import audio
import audio_file
import data_conversion
import generic_shift_keying
import waves

SEGMENT_BITS = 4

def send(text):
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    # Convert the text into a binary string
    binary_string = data_conversion.text_to_binary_string(text)
    
    # Convert the binary string into an array of integers
    data = data_conversion.bits_to_integers(binary_string, SEGMENT_BITS)

    data = audio.add_integers_stops(data)

    # Time segment between each modulation
    segment_time = 0.1
    
    # Modulate the data
    wave = generic_shift_keying.shift_keying(data, segment_time)

    # Convert the binary string into a digital wave
    digital_wave = waves.generate_digital_wave(binary_string)

    # Turn the data into a square signal wave
    square_wave = waves.generate_square_wave(data, segment_time)

    # Create a time axis
    time = waves.generate_time_axis(segment_time, len(data))


    # Plot the waves on a graph
    plt.subplot(3,1,1)
    plt.step(range(0, len(digital_wave)), digital_wave)

    plt.subplot(3,1,2)
    plt.grid(axis = "y")
    plt.plot(time, square_wave)

    plt.subplot(3,1,3)
    plt.grid(axis = "y")
    plt.plot(time, wave)

    plt.show()

    # Play the modulated wave as a sound
    audio.play_wave(stream_play, wave)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def receive_and_fourier():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    data = audio.record_audio(stream_record, 5)
    audio_file.save_audio_file(pyaudio_instance, data)
    d = audio_file.read_audio_file()

    int_data = data_conversion.raw_data_to_int(d)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

    freq, fourier_wave = waves.generate_fourier_wave(int_data)

    freq_subset = freq[1:int(audio.SAMPLE_RATE/4)]
    fourier_wave_subset = np.abs(fourier_wave)[1:int(audio.SAMPLE_RATE/4)]

    freq_max = freq_subset[np.argmax(fourier_wave_subset)]
    print(freq_max)

    plt.plot(freq_subset, fourier_wave_subset)
    plt.show()

def record():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    data = audio.record_audio(stream_record, 5)
    audio_file.save_audio_file(pyaudio_instance, data)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def receive():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    # How many consecutive samples should be identical before recording the value
    sureness = 5

    int_stream_raw = [0] * (sureness)
    int_stream = []
    
    try:
        text = ""

        while True:
            # Record a chunk of audio and get its integer value
            data = stream_record.read(audio.RECORDING_CHUNK_SIZE)
            int_value = audio.extract_int_from_audio(data)

            # Add this integer value to the log of data
            audio.add_to_int_stream(int_value, int_stream, int_stream_raw, sureness)

            # Convert integer data back into text
            int_stream_no_stops = audio.remove_integers_stops(int_stream)
            binary_string = data_conversion.integers_to_bits(int_stream_no_stops, SEGMENT_BITS)

            # Display the text when it changes
            text_new = data_conversion.binary_string_to_text(binary_string)
            if text_new != text:
                text = text_new
                print(text)
    except KeyboardInterrupt:
        audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

if __name__ == "__main__":
    if argv[1] == "send":
        send("helloworldhowareyou?")
    elif argv[1] == "receive":
        receive()
    elif argv[1] == "record":
        record()