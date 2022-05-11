from matplotlib import pyplot as plt
import numpy as np
from sys import argv

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
    stream_play, stream_record = audio.start()

    wave = audio.record_audio(stream_record, 5)

    #wave = np.frombuffer(data, dtype=np.int16)

    frequencies, fourier_wave = waves.generate_fourier_wave(wave)

    plt.plot(frequencies, fourier_wave)
    plt.show()

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
    plt.show()

    audio.play_wave(stream_play, w)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

def receive():
    stream_play, stream_record = audio.start()

    data_stream_raw = []
    data_stream = []
    previous_text = ""

    try:
        while True:
            # Record a chunk of audio and get its integer value
            wave = audio.read_audio(stream_record)

            frequencies, fourier_wave = waves.generate_fourier_wave(wave)

            freqs_max = shift_keying.get_loudest_frequencies(frequencies, fourier_wave, len(constants.CHANNELS))

            data = [None,]*len(constants.CHANNELS)

            for i, channel in enumerate(constants.CHANNELS):
                if channel[0] in freqs_max:
                    data[i] = 0
                if channel[1] in freqs_max:
                    data[i] = 1
                if channel[2] in freqs_max:
                    data[i] = 9
            
            if not None in data:
                data_stream_raw.append(data)

                if shift_keying.check_sent_deliberately(data, data_stream_raw) and shift_keying.check_not_added(data, data_stream):
                    data_stream.append(data)

            bits = np.array(data_stream).flatten()
            bit_string = "".join([str(x) for x in bits])
            bit_string = bit_string.replace("9","")
            text = data_conversion.bits_to_text(bit_string)

            if previous_text != text:
                print(text)
                previous_text = text

    except KeyboardInterrupt:
        exit()

def send(text):
    stream_play, stream_record = audio.start()

    bits = data_conversion.text_to_bits(text)
    bits = data_conversion.pad_bits(bits, len(constants.CHANNELS))

    wave = []

    l = 0
    while l < len(bits):
        wave_data_segment = []
        wave_gap_segment = []

        channel = 0
        while channel < len(constants.CHANNELS):
            low_wave = waves.generate_wave(constants.CHANNELS[channel][0], 1, 1, constants.SEGMENT_TIME)
            high_wave = waves.generate_wave(constants.CHANNELS[channel][1], 1, 1, constants.SEGMENT_TIME)

            if bits[l+channel] == "0":
                wave_segment_addition = low_wave
            if bits[l+channel] == "1":
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

    audio.play_wave(stream_play, wave)

if __name__ == "__main__":
    if argv[1] == "send":
        message = input("Enter message> ")
        send(message)
    elif argv[1] == "receive":
        receive()
    elif argv[1] == "frequencies":
        play_frequencies()
    elif argv[1] == "fourier":
        record_and_fourier()