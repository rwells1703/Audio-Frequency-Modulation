from matplotlib import pyplot as plt

import generic_shift_keying
import binary_shift_keying
import utils

def main():
    data = [0,2,5,6,4,4,6,1,1,1,7,7,7,7,5,4,3,2,2,2,5,7]
    #data = [0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,0]

    segment_time = 0.2

    # Turn the data into a digital signal wave
    digital_wave = utils.generate_digital_wave(data, segment_time)
    
    # Modulate the data
    wave = generic_shift_keying.shift_keying(data, segment_time)
    #wave = binary_shift_keying.phase_shift_keying(data, segment_time, 5, 10)
    
    # Create a time axis
    time = utils.generate_time_axis(segment_time, len(data))


    # Plot the waves on a graph
    plt.subplot(1,2,1)
    plt.grid(axis = 'y')
    plt.plot(time, digital_wave)

    plt.subplot(1,2,2)
    plt.plot(time, wave)

    plt.show()

    utils.play_wave(wave)

if __name__ == "__main__":
    main()