import numpy as np
from matplotlib import pyplot as plt

import audio
import data_conversion
import verification
import waves

class HOFSK:
    # Time taken for a single segment to play
    SEGMENT_TIME = 0.1

    # The number of bits in a recorded audio block
    RECORDING_BLOCK_SIZE =  1024

    # The proportion of segments within a sample group that should be identical, before storing the segment
    # e.g. 3 out of 6 segment should be equal to 1 otherwise the segment will not be stored
    CERTAINTY = 4
    CERTAINTY_SAMPLE_SIZE = 7

    # The number of bits per segment
    SEGMENT_BITS = 4

    # Increments by the step at which recoreded frequencies are quantized
    RECORD_FREQ_STEP = audio.SAMPLE_RATE / RECORDING_BLOCK_SIZE

    # The range of frequency quantizations used
    MIN_FREQ = 600
    MIN_FREQ = MIN_FREQ - (MIN_FREQ % RECORD_FREQ_STEP)
    MAX_FREQ = MIN_FREQ + (2**SEGMENT_BITS+2) * (RECORD_FREQ_STEP)
    FREQ_RANGE = np.arange(start=MIN_FREQ, stop=MAX_FREQ, step=RECORD_FREQ_STEP)

    def send(self, text):
        stream_play, stream_record = audio.start(HOFSK.RECORDING_BLOCK_SIZE)

        # Convert the text into bits
        bits = data_conversion.text_to_bits(text)

        # Convert the bits into an array of integers
        int_stream = self.bits_to_ints(bits)

        int_stream_gaps = self.add_ints_gaps(int_stream)
        #print(int_stream_gaps)

        # Modulate the data
        wave = self.ints_to_wave(int_stream_gaps)

        # Plot the waves
        #self.plot_sent_waves(bits, int_stream, int_stream_gaps, wave)

        # Play the modulated wave as a sound
        audio.play_wave(stream_play, wave)

    def receive(self):
        stream_play, stream_record = audio.start(HOFSK.RECORDING_BLOCK_SIZE)

        # Buffers storing ints
        int_stream_raw = []
        int_stream = []
        text = ""
        g = 0

        while True:
            # Record a chunk of audio and get its waveform
            wave = audio.read_wave(stream_record, HOFSK.RECORDING_BLOCK_SIZE)

            # Extract integer values from the audio wave
            int_value = self.wave_to_int(wave)

            # Add the value to the stream of potential values
            if (int_value != None):
                int_stream_raw.append(int_value)
                #print(int_value)

            # Add the value to the stream of verified values
            if verification.check_sent_deliberately(int_value, int_stream_raw, HOFSK.CERTAINTY, HOFSK.CERTAINTY_SAMPLE_SIZE, g) and verification.check_not_added(int_value, int_stream):
                int_stream.append(int_value)
                int_stream.append(g)
                g = (g+1)%2
                #print(int_stream)

                # Convert list of integers back into text
                int_stream_no_gaps = self.remove_ints_gaps(int_stream)

                # Convert the int stream to bits
                bits = self.ints_to_bits(int_stream_no_gaps)

                # Display the text when it changes
                text_new = data_conversion.bits_to_text(bits)

                # If the text has changed since the last iteration, display the new text
                if text_new != text:
                    text = text_new
                    print(text)

    # Converts a string of bits to an array of integers representing them
    def bits_to_ints(self, bits):
        start = 0
        end = HOFSK.SEGMENT_BITS
        
        bits = data_conversion.pad_bits(bits, HOFSK.SEGMENT_BITS)

        integers = []

        # Loop through the bits and convert sections to an integer
        while end <= len(bits):
            bits_segment = bits[start:end]
            integers.append(int(bits_segment, 2) + 2)
            
            start += HOFSK.SEGMENT_BITS
            end += HOFSK.SEGMENT_BITS

        return integers

    # Convert integers to a string of bits
    def ints_to_bits(self, int_stream):
        bits = ""

        for i in int_stream:
            bits += bin(i-2)[2:].zfill(HOFSK.SEGMENT_BITS)
        
        return bits

    # Interlace zeros between the integer values to symbolise the end of each symbol
    def add_ints_gaps(self, int_stream):
        output = []

        # Value for gap value fluctuates between 0 and 1
        g = 0
        for i in int_stream:
            output.append(g)
            output.append(i)

            g = (g+1)%2


        return output

    # Remove interlaced zeros between the integer values to symbolise the end of each symbol
    def remove_ints_gaps(self, int_stream):
        output = []

        for i in int_stream:
            # Remove any gap values
            if i != 0 and i != 1:
                output.append(i)

        return output

    # Performs shift keying on amplitude, frequency and phase concurrently
    def ints_to_wave(self, ints):
        wave = []

        # Loop through the input data
        for i in ints:
            # Get frequency values for that section of wave
            frequency = HOFSK.FREQ_RANGE[i]

            # Generate that section of wave and append it to the overall wave
            wave_segment = waves.generate_wave(frequency, 1, 1, HOFSK.SEGMENT_TIME)
            wave = waves.combine_waves(wave, wave_segment)

        return wave

    # Takes a chunk of audio data, and gets the integer value it corresponds to
    def wave_to_int(self, wave):
        frequencies, fourier_wave = waves.generate_fourier_wave(wave)

        freq_max = self.get_loudest_frequency(frequencies, fourier_wave)

        if self.clip_frequency(freq_max):
            return None
        
        int_value = self.match_frequency(freq_max)

        #print(int_value, ": ", freq_max)

        return int_value

    # Rejects any frequency higher or lower than the clipping bounds
    def clip_frequency(self, frequency):
        if frequency > HOFSK.MAX_FREQ or frequency < HOFSK.MIN_FREQ:
            return True

        return False

    # Finds the correct integer data point for a given approximate frequency
    def match_frequency(self, frequency):
        # Get the corresponding integer value for that frequency
        int_values_matched = np.where(HOFSK.FREQ_RANGE == frequency)[0]
        if len(int_values_matched) > 0:
            return int_values_matched[0]

        # No integer value matches this frequency
        return None

    # Returns the loudest frequency present within the fourier fransform
    def get_loudest_frequency(self, frequencies, fourier_wave):
        return frequencies[np.argmax(fourier_wave)]

    # Plot the waves on a pyplot graph
    def plot_sent_waves(self, bits, int_stream, int_stream_gaps, wave):
        # Generate a time axis for the modulated audio wave
        wave_time = waves.generate_time_axis(len(wave) / audio.SAMPLE_RATE, len(wave))

        # Convert the binary string into a digital wave
        digital_wave = waves.generate_digital_wave(bits)

        # Turn the data into a square signal wave
        square_wave = waves.generate_square_wave(int_stream, HOFSK.SEGMENT_TIME)
        square_wave_time = waves.generate_time_axis(len(int_stream) * HOFSK.SEGMENT_TIME, len(int_stream) * HOFSK.SEGMENT_TIME * audio.SAMPLE_RATE)

        # Turn the data into a square signal wave
        square_wave_gapped = waves.generate_square_wave(int_stream_gaps, HOFSK.SEGMENT_TIME)
        square_wave_gapped_time = waves.generate_time_axis(len(int_stream_gaps) * HOFSK.SEGMENT_TIME, len(int_stream_gaps) * HOFSK.SEGMENT_TIME * audio.SAMPLE_RATE)

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

        # Display the graphs
        plt.show()