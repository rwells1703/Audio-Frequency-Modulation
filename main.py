from matplotlib import pyplot as plt
import numpy as np
from sys import argv
import time

import audio
import audio_file
import constants
import data_conversion
import shift_keying
import waves

def send_old(text):
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    # Convert the text into bits
    bits = data_conversion.text_to_bits(text)
    print(bits)

    # Convert the bits into an array of integers
    int_stream_gaps = data_conversion.bits_to_ints(bits)
    int_stream = data_conversion.add_ints_gaps(int_stream_gaps)
    print(int_stream)
    
    # Modulate the data
    wave = shift_keying.ints_to_wave(int_stream, constants.SENDING_SEGMENT_TIME)

    '''
    # Convert the binary string into a digital wave
    digital_wave = waves.generate_digital_wave(bits)

    # Turn the data into a square signal wave
    square_wave = waves.generate_square_wave(wave, constants.SENDING_SEGMENT_TIME)

    # Create a time axis
    time = waves.generate_time_axis(constants.SENDING_SEGMENT_TIME, len(wave))


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
    '''

    # Play the modulated wave as a sound
    audio.play_wave(stream_play, wave)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def receive_old():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    int_stream_raw = [0] * (constants.CERTAINTY_SAMPLE_SIZE)
    int_stream = []
    text = ""

    try:
        while True:
            # Record a chunk of audio and get its integer value
            data = stream_record.read(constants.RECORDING_CHUNK_SIZE)

            # Convert microphone audio data into a waveform
            wave = np.frombuffer(data, dtype=np.int16)

            # Extract integer values from the audio wave
            int_value = shift_keying.wave_to_int(wave)

            # Add the value to the stream of potential values
            if (int_value != None):
                int_stream_raw.append(int_value)

            # Add the value to the stream of verified values
            if shift_keying.check_sent_deliberately(int_value, int_stream_raw) and shift_keying.check_not_added(int_value, int_stream):
                int_stream.append(int_value)

            # Convert list of integers back into text
            int_stream_no_gaps = data_conversion.remove_ints_gaps(int_stream)

            # Convert the int stream to bits
            bits = data_conversion.ints_to_bits(int_stream_no_gaps)

            # Display the text when it changes
            text_new = data_conversion.bits_to_text(bits)

            if text_new != text:
                text = text_new
                print(text)
    except KeyboardInterrupt:
        audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def record_and_save():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    data = audio.record_audio(stream_record, 2)
    audio_file.save_audio_file(pyaudio_instance, data)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def record_and_fourier():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    data = audio.record_audio(stream_record, 5)

    wave = np.frombuffer(data, dtype=np.int16)

    frequencies, fourier_wave = waves.generate_fourier_wave(wave)

    plt.plot(frequencies, fourier_wave)
    plt.show()

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def play_frequencies():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    seconds = 5
    w = waves.generate_flat_signal(0, seconds)

    freqs = [400,500,800]

    for f in freqs:
        new_w = waves.generate_wave(f, 1, 1, seconds)
        w = w + new_w

    w /= len(freqs)

    t = waves.generate_time_axis(seconds, 1)

    plt.grid(axis = "y")
    plt.plot(t, w)
    #plt.show()

    audio.play_wave(stream_play, w)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def receive():
    stream_play, stream_record = audio.start()

    x = 0
    freqs_max = (0,)*len(constants.CHANNELS)
    try:
        while True:
            # Record a chunk of audio and get its integer value
            data = audio.read_audio(stream_record)

            wave = data.flatten()

            frequencies, fourier_wave = waves.generate_fourier_wave(wave)

            #freq_max = int(shift_keying.get_loudest_frequency(frequencies, fourier_wave))
            freqs_max_prev = freqs_max
            freqs_max = shift_keying.get_loudest_frequencies(frequencies, fourier_wave, len(constants.CHANNELS))
            #print(freqs_max)

            for i, channel in enumerate(constants.CHANNELS):
                if (freqs_max[i] == channel[0] and freqs_max_prev[i] == channel[2]):
                    print(x, ": 0")
                    x += 1
                elif (freqs_max[i] == channel[1] and freqs_max_prev[i] == channel[2]):
                    print(x, ": 1")
                    x += 1

    except KeyboardInterrupt:
        print()

def send(text):
    stream_play, stream_record = audio.start()

    #data = "100000000000000000100101000101001010100001000010101110100000001001010111111101010000101"
    data = "111100101010101000010101111"
    #data = "10"*20
    data = data_conversion.pad_bits(data, len(constants.CHANNELS))
    print(data)

    wave = []

    l = 0
    while l < len(data):
        wave_data_segment = []
        wave_gap_segment = []

        channel = 0
        while channel < len(constants.CHANNELS):
            low_wave = waves.generate_wave(constants.CHANNELS[channel][0], 1, 1, constants.SEGMENT_TIME)
            high_wave = waves.generate_wave(constants.CHANNELS[channel][1], 1, 1, constants.SEGMENT_TIME)

            if data[l+channel] == "0":
                wave_segment_addition = low_wave
            if data[l+channel] == "1":
                wave_segment_addition = high_wave

            wave_gap_addition = waves.generate_wave(constants.CHANNELS[channel][2], 1, 1, constants.SEGMENT_TIME)

            # If there is no current data segment (or gap segment)
            if channel == 0:
                wave_data_segment = wave_segment_addition
                wave_gap_segment = wave_gap_addition
            else:
                wave_data_segment += wave_segment_addition
                wave_gap_segment += wave_gap_addition

            channel += 1

        wave_gap_segment /= len(constants.CHANNELS)
        wave = waves.combine_waves(wave, wave_gap_segment)

        wave_data_segment /= len(constants.CHANNELS)
        wave = waves.combine_waves(wave, wave_data_segment)

        l += len(constants.CHANNELS)
        
    #t = waves.generate_time_axis(constants.SEGMENT_TIME, len(wave))
    #plt.grid(axis = "y")
    #plt.plot(t, wave)
    #plt.show()

    #wave /= len(freqs) + 1

    audio.play_wave(stream_play, wave)

if __name__ == "__main__":
    if argv[1] == "send":
        send("hello")
    elif argv[1] == "receive":
        receive()
    elif argv[1] == "frequencies":
        play_frequencies()
    elif argv[1] == "fourier":
        record_and_fourier()