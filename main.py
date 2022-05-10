from matplotlib import pyplot as plt
import numpy as np
from sys import argv
import audio
import audio_file
import constants
import data_conversion
import shift_keying
import waves

def send(text):
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

def receive():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    int_stream_raw = [0] * (constants.CERTAINTY_SAMPLE_SIZE)
    int_stream = []
    text = ""

    try:
        while True:
            # Record a chunk of audio and get its integer value
            data = stream_record.read(constants.RECORDING_CHUNK_SIZE)

            # Convert microphone audio data into a waveform
            wave = waves.bytestring_audio_to_wave(data)

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

def record_and_fourier():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    data = audio.record_audio(stream_record, 5)

    int_data = data_conversion.bytestring_audio_to_ints(data)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

    freq, fourier_wave = waves.generate_fourier_wave(int_data)

    freq_subset = freq[1:int(constants.SAMPLE_RATE/4)]
    fourier_wave_subset = np.abs(fourier_wave)[1:int(constants.SAMPLE_RATE/4)]

    freq_max = freq_subset[np.argmax(fourier_wave_subset)]
    print(freq_max)

    plt.plot(freq_subset, fourier_wave_subset)
    plt.show()

def record_and_save():
    pyaudio_instance, stream_play, stream_record = audio.start_pyaudio()

    data = audio.record_audio(stream_record, 5)
    audio_file.save_audio_file(pyaudio_instance, data)

    audio.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

if __name__ == "__main__":
    if argv[1] == "send":
        send("hello")
    elif argv[1] == "receive":
        receive()