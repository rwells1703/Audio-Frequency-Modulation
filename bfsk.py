import numpy as np

import audio
import constants
import data_conversion
import shift_keying
import waves

def send(text):
    stream_play, stream_record = audio.start(constants.BFSK_RECORDING_BLOCK_SIZE)

    bits = data_conversion.text_to_bits(text)
    bits = data_conversion.pad_bits(bits, constants.BFSK_CHANNEL_COUNT)

    wave = []

    l = 0
    while l < len(bits):
        wave_data_segment = []
        wave_gap_segment = []

        channel = 0
        while channel < constants.BFSK_CHANNEL_COUNT:
            low_wave = waves.generate_wave(constants.BFSK_CHANNELS[channel][0], 1, 1, constants.BFSK_SEGMENT_TIME)
            high_wave = waves.generate_wave(constants.BFSK_CHANNELS[channel][1], 1, 1, constants.BFSK_SEGMENT_TIME)

            if bits[l+channel] == "0":
                wave_segment_addition = low_wave
            if bits[l+channel] == "1":
                wave_segment_addition = high_wave

            wave_gap_addition = waves.generate_wave(constants.BFSK_CHANNELS[channel][2], 1, 1, constants.BFSK_SEGMENT_TIME)

            # If there is no current data segment (or gap segment)
            if channel == 0:
                wave_data_segment = wave_segment_addition
                wave_gap_segment = wave_gap_addition
            else:
                wave_data_segment += wave_segment_addition
                wave_gap_segment += wave_gap_addition

            channel += 1

        wave_gap_segment /= constants.BFSK_CHANNEL_COUNT
        wave = waves.combine_waves(wave, wave_gap_segment)

        wave_data_segment /= constants.BFSK_CHANNEL_COUNT
        wave = waves.combine_waves(wave, wave_data_segment)

        l += constants.BFSK_CHANNEL_COUNT

    audio.play_wave(stream_play, wave)

def receive():
    stream_play, stream_record = audio.start(constants.BFSK_RECORDING_BLOCK_SIZE)

    data_stream_raw = []
    data_stream = []
    previous_text = ""

    while True:
        # Record a chunk of audio and get its waveform
        wave = audio.read_wave(stream_record, constants.BFSK_RECORDING_BLOCK_SIZE)

        frequencies, fourier_wave = waves.generate_fourier_wave(wave)

        freqs_max = shift_keying.get_loudest_frequencies(frequencies, fourier_wave, constants.BFSK_CHANNEL_COUNT)

        data = [None,]*constants.BFSK_CHANNEL_COUNT

        for i, channel in enumerate(constants.BFSK_CHANNELS):
            if channel[0] in freqs_max:
                data[i] = 0
            if channel[1] in freqs_max:
                data[i] = 1
            if channel[2] in freqs_max:
                data[i] = 9
        
        if not None in data:
            data_stream_raw.append(data)

            if shift_keying.check_sent_deliberately(data, data_stream_raw, constants.BFSK_CERTAINTY, constants.BFSK_CERTAINTY_SAMPLE_SIZE) and shift_keying.check_not_added(data, data_stream):
                data_stream.append(data)

        bits = np.array(data_stream).flatten()
        bit_string = "".join([str(x) for x in bits])
        bit_string = bit_string.replace("9","")
        text = data_conversion.bits_to_text(bit_string)

        if previous_text != text:
            print(text)
            previous_text = text