import numpy as np

import audio
import data_conversion
import shift_keying
import waves

class BFSK:
    # Time taken for a single segment to play (a segment is c bits, where c is the number of channels) 
    SEGMENT_TIME = 0.2

    # The number of bits in a recorded audio block (based upon segment time)
    RECORDING_BLOCK_SIZE = int(audio.SAMPLE_RATE * (SEGMENT_TIME / 8))

    # The proportion of segments within a sample group that should be identical, before storing the segment
    # e.g. 3 out of 6 segment should be equal to 101011 otherwise the segment will not be stored
    CERTAINTY = 5
    CERTAINTY_SAMPLE_SIZE = 10

    # The frequency channels used for transmission
    CHANNELS = [(1000, 1200, 3000), (1400, 1600, 3200), (1800, 2000, 3400)]
    CHANNEL_COUNT = len(CHANNELS)

    def send(self, text):
        stream_play, stream_record = audio.start(BFSK.RECORDING_BLOCK_SIZE)

        bits = data_conversion.text_to_bits(text)
        bits = data_conversion.pad_bits(bits, BFSK.CHANNEL_COUNT)

        wave = []

        l = 0
        while l < len(bits):
            wave_data_segment = []
            wave_gap_segment = []

            channel = 0
            while channel < BFSK.CHANNEL_COUNT:
                low_wave = waves.generate_wave(BFSK.CHANNELS[channel][0], 1, 1, BFSK.SEGMENT_TIME)
                high_wave = waves.generate_wave(BFSK.CHANNELS[channel][1], 1, 1, BFSK.SEGMENT_TIME)

                if bits[l+channel] == "0":
                    wave_segment_addition = low_wave
                if bits[l+channel] == "1":
                    wave_segment_addition = high_wave

                wave_gap_addition = waves.generate_wave(BFSK.CHANNELS[channel][2], 1, 1, BFSK.SEGMENT_TIME)

                # If there is no current data segment (or gap segment)
                if channel == 0:
                    wave_data_segment = wave_segment_addition
                    wave_gap_segment = wave_gap_addition
                else:
                    wave_data_segment += wave_segment_addition
                    wave_gap_segment += wave_gap_addition

                channel += 1

            wave_gap_segment /= BFSK.CHANNEL_COUNT
            wave = waves.combine_waves(wave, wave_gap_segment)

            wave_data_segment /= BFSK.CHANNEL_COUNT
            wave = waves.combine_waves(wave, wave_data_segment)

            l += BFSK.CHANNEL_COUNT

        audio.play_wave(stream_play, wave)

    def receive(self):
        stream_play, stream_record = audio.start(BFSK.RECORDING_BLOCK_SIZE)

        data_stream_raw = []
        data_stream = []
        previous_text = ""

        while True:
            # Record a chunk of audio and get its waveform
            wave = audio.read_wave(stream_record, BFSK.RECORDING_BLOCK_SIZE)

            frequencies, fourier_wave = waves.generate_fourier_wave(wave)

            freqs_max = self.get_loudest_frequencies(frequencies, fourier_wave, BFSK.CHANNEL_COUNT)

            data = [None,] * BFSK.CHANNEL_COUNT

            for i, channel in enumerate(BFSK.CHANNELS):
                if channel[0] in freqs_max:
                    data[i] = 0
                if channel[1] in freqs_max:
                    data[i] = 1
                if channel[2] in freqs_max:
                    data[i] = 9
            
            if not None in data:
                data_stream_raw.append(data)

                if shift_keying.check_sent_deliberately(data, data_stream_raw, BFSK.CERTAINTY, BFSK.CERTAINTY_SAMPLE_SIZE) and shift_keying.check_not_added(data, data_stream):
                    data_stream.append(data)

            bits = np.array(data_stream).flatten()
            bit_string = "".join([str(x) for x in bits])
            bit_string = bit_string.replace("9","")
            text = data_conversion.bits_to_text(bit_string)

            if previous_text != text:
                print(text)
                previous_text = text
    
    # Returns the n loudest frequencies present within the fourier fransform
    def get_loudest_frequencies(self, frequencies, fourier_wave, n):
        sorted_inds = np.argsort(fourier_wave)
        sorted_freqs = np.flip(frequencies[sorted_inds].astype(int))

        # Round the frequencies to the nearest 100
        rounded_freqs = list(map(lambda f : round(f, -2), sorted_freqs))

        # Remove any duplicated occurences of frequencies
        # these occur when there are several similar frequencies in the loudest frequency list
        # which are then rounded to the same value
        unique_freqs = []
        i = 0
        c = n
        while i < len(rounded_freqs) and c > 0:
            if not rounded_freqs[i] in unique_freqs:
                unique_freqs.append(rounded_freqs[i])
                c -= 1
            i += 1

        return unique_freqs