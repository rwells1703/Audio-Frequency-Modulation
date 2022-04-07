import generic_shift_keying
import binary_shift_keying
import utils

def main():
    time, wave = generic_shift_keying.shift_keying([0,2,5,6,4,4,6,1,1,1,7,7,7,7,5,4,3,2,2,2,5,7], 0.2)
    #time, wave = binary_shift_keying.frequency_shift_keying([0,1,0,0,0,0,1,1,0,1], 0.2)

    utils.plot_wave(time, wave)
    utils.play_wave(wave)
    
if __name__ == "__main__":
    main()