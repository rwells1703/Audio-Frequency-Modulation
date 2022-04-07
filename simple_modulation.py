import numpy as np

import utils

# Generates two sine waves of different frequencies and appends them along the time axis
def generate_dual_freq_wave(seconds, frequency1, frequency2):
    time1, wave1 = utils.generate_wave(seconds/2, frequency1, 1)
    time2, wave2 = utils.generate_wave(seconds/2, frequency2, 1)
    
    time = np.linspace(0, seconds, np.ceil(seconds * utils.SAMPLE_RATE).astype(int), False)
    wave = np.append(wave1, wave2)

    return time, wave