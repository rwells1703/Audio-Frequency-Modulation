from matplotlib import pyplot as plt

import audio
import constants
import data_conversion
import shift_keying
import waves

def send(text):
    stream_play, stream_record = audio.start(constants.MFSK_RECORDING_BLOCK_SIZE)

    # Convert the text into bits
    bits = data_conversion.text_to_bits(text)

    # Convert the bits into an array of integers
    int_stream = data_conversion.bits_to_ints(bits)
    int_stream_gaps = data_conversion.add_ints_gaps(int_stream)
    
    # Modulate the data
    wave = shift_keying.ints_to_wave(int_stream_gaps)
    wave_time = waves.generate_time_axis(len(wave) / constants.SAMPLE_RATE, len(wave))

    # Convert the binary string into a digital wave
    digital_wave = waves.generate_digital_wave(bits)

    # Turn the data into a square signal wave
    square_wave = waves.generate_square_wave(int_stream, constants.MFSK_SEGMENT_TIME)
    square_wave_time = waves.generate_time_axis(len(int_stream) * constants.MFSK_SEGMENT_TIME, len(int_stream) * constants.MFSK_SEGMENT_TIME * constants.SAMPLE_RATE)

    # Turn the data into a square signal wave
    square_wave_gapped = waves.generate_square_wave(int_stream_gaps, constants.MFSK_SEGMENT_TIME)
    square_wave_gapped_time = waves.generate_time_axis(len(int_stream_gaps) * constants.MFSK_SEGMENT_TIME, len(int_stream_gaps) * constants.MFSK_SEGMENT_TIME * constants.SAMPLE_RATE)

    # Plot the waves on a graph
    plt.subplot(4,1,1)
    plt.step(range(0, len(digital_wave)), digital_wave)

    plt.subplot(4,1,2)
    plt.grid(axis = "y")
    plt.plot(square_wave_time, square_wave)

    plt.subplot(4,1,3)
    plt.grid(axis = "y")
    plt.plot(square_wave_gapped_time, square_wave_gapped)

    plt.subplot(4,1,4)
    plt.grid(axis = "y")
    plt.plot(wave_time, wave)

    plt.show()

    # Play the modulated wave as a sound
    audio.play_wave(stream_play, wave)

def receive():
    stream_play, stream_record = audio.start(constants.MFSK_RECORDING_BLOCK_SIZE)

    int_stream_raw = [0] * (constants.MFSK_CERTAINTY_SAMPLE_SIZE)
    int_stream = []
    text = ""

    while True:
        # Record a chunk of audio and get its waveform
        wave = audio.read_wave(stream_record, constants.MFSK_RECORDING_BLOCK_SIZE)

        # Extract integer values from the audio wave
        int_value = shift_keying.wave_to_int(wave)

        # Add the value to the stream of potential values
        if (int_value != None):
            int_stream_raw.append(int_value)

        # Add the value to the stream of verified values
        if shift_keying.check_sent_deliberately(int_value, int_stream_raw, constants.MFSK_CERTAINTY, constants.MFSK_CERTAINTY_SAMPLE_SIZE) and shift_keying.check_not_added(int_value, int_stream):
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