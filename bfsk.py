import numpy as np

import audio
import data_conversion
import verification
import waves

class BFSK:
    # Time taken for a single segment to play (a segment is c bits, where c is the number of channels) 
    SEGMENT_TIME = 0.2
    
    # The value marking the end of a data segment
    END_SEGMENT_VALUE = 9

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

        # Convert the text into bits
        bits = data_conversion.text_to_bits(text)
        bits_padded = data_conversion.pad_bits(bits, BFSK.CHANNEL_COUNT)
        
        # Converts padded input bits into a modulated audio waveform
        wave = self.bits_to_wave(bits_padded)

        # Play the modulated wave as a sound
        audio.play_wave(stream_play, wave)

    def receive(self):
        stream_play, stream_record = audio.start(BFSK.RECORDING_BLOCK_SIZE)

        data_stream_raw = []
        data_stream = []

        previous_text = ""

        while True:
            # Record a chunk of audio and get its waveform
            wave = audio.read_wave(stream_record, BFSK.RECORDING_BLOCK_SIZE)

            # Fourier transform the waveform to get its constituent frequencies
            frequencies, fourier_wave = waves.generate_fourier_wave(wave)

            # Get a list of the top n loudest frequencies (where n is the number of channels)
            freqs_max = self.get_loudest_frequencies(frequencies, fourier_wave, BFSK.CHANNEL_COUNT)

            # Clear the data buffer
            data = [None,] * BFSK.CHANNEL_COUNT

            # If any of the frequencies corresponding to a channel are playing,
            # the bit corresponding to that frequency is set
            for i, channel in enumerate(BFSK.CHANNELS):
                if channel[0] in freqs_max:
                    data[i] = 0
                if channel[1] in freqs_max:
                    data[i] = 1
                if channel[2] in freqs_max:
                    data[i] = BFSK.END_SEGMENT_VALUE
            
            # Verify single bit in the segment was received at once
            if not None in data:
                data_stream_raw.append(data)

                # Add the segment to the stream of verified segment
                if verification.check_sent_deliberately(data, data_stream_raw, BFSK.CERTAINTY, BFSK.CERTAINTY_SAMPLE_SIZE) and verification.check_not_added(data, data_stream):
                    data_stream.append(data)

            # Converts the data stream into readable text
            bits = self.data_stream_to_bits(data_stream)
            text = data_conversion.bits_to_text(bits)

            # If the text has changed since the last iteration, display the new text
            if previous_text != text:
                print(text)
                previous_text = text
    
    # Takes a list of bits, and converts them into a modulated audio waveform using BFSK
    def bits_to_wave(self, bits):
        wave = []

        i = 0
        while i < len(bits):
            channel = 0
            while channel < BFSK.CHANNEL_COUNT:
                # Define the waves used for representing 1 and 0 (on this channel)
                low_wave = waves.generate_wave(BFSK.CHANNELS[channel][0], 1, 1, BFSK.SEGMENT_TIME)
                high_wave = waves.generate_wave(BFSK.CHANNELS[channel][1], 1, 1, BFSK.SEGMENT_TIME)

                # Add either the high or low frequency wave
                if bits[i+channel] == "0":
                    wave_segment_addition = low_wave
                if bits[i+channel] == "1":
                    wave_segment_addition = high_wave

                # Define the wave used to symbolise the end of a segment (on this channel)
                wave_gap_addition = waves.generate_wave(BFSK.CHANNELS[channel][2], 1, 1, BFSK.SEGMENT_TIME)

                # If there is no current data segment (or gap segment)
                if channel == 0:
                    # Create a new wave
                    wave_data_segment = wave_segment_addition
                    wave_gap_segment = wave_gap_addition
                else:
                    # Otherwise, add (elementwise) it to the current wave
                    wave_data_segment += wave_segment_addition
                    wave_gap_segment += wave_gap_addition

                channel += 1

            # Combine the actual data wave, with the end of segment wave
            wave_segment = waves.combine_waves(wave_data_segment, wave_gap_segment)

            # Combine this with the overall wave
            wave = waves.combine_waves(wave, wave_segment)

            i += BFSK.CHANNEL_COUNT

        # Normalise the resultant wave, so that it does not produce audio clipping
        # (clipping means loosing data, as fourier transform produces unexpected results)
        wave /= BFSK.CHANNEL_COUNT

        return wave

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

    # Converts the array of bit segments into a string of bits
    def data_stream_to_bits(self, data_stream):
        bit_array = np.array(data_stream).flatten()
        bits_with_end_val = "".join([str(x) for x in bit_array])
        bits = bits_with_end_val.replace(str(BFSK.END_SEGMENT_VALUE),"")

        return bits