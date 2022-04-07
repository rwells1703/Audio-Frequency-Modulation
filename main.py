import binary_shift_keying
import utils

def main():
    time, amplitude = binary_shift_keying.frequency_shift_keying([0,1,1,0,0,0,0,0,1,0,1,1,1,0,0,1,1,1,1])

    utils.plot_wave(time, amplitude)
    utils.play_wave(amplitude)
    
if __name__ == "__main__":
    main()