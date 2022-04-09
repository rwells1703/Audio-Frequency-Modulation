from matplotlib import pyplot as plt

import generic_shift_keying
import utils
import data_conversion

def main():
    pyaudio_instance, stream = utils.start_pyaudio()

    # Text to be converted
    text = "hello world"

    # Convert the text into a binary string
    binary_data = data_conversion.text_to_bit_string(text)

    # Convert the binary string into an array of integers
    data = data_conversion.bits_to_integers(binary_data, 4)

    # Time segment between each modulation
    segment_time = 0.2

    # Convert the binary string into a digital wave
    digital_wave = []
    # Duplicate the first value, otherwise the graph will be plotted incorrectly
    digital_wave.append(int(binary_data[0]))
    # Loop through the binary data and convert it into an array of ints
    for b in binary_data:
        digital_wave.append(int(b))
    
    # Turn the data into a square signal wave
    square_wave = utils.generate_square_wave(data, segment_time)

    # Modulate the data
    wave = generic_shift_keying.shift_keying(data, segment_time)

    # Create a time axis
    time = utils.generate_time_axis(segment_time, len(data))


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
    utils.play_wave(stream, wave)

    utils.stop_pyaudio(pyaudio_instance, stream)

if __name__ == "__main__":
    main()