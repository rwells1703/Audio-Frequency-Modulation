import numpy as np
from matplotlib import pyplot as plt

import utils

pyaudio_instance, stream_play, stream_record = utils.start_pyaudio()

data = utils.record_audio(stream_record, 1)
wave = utils.wav_data_to_wave(data)

utils.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

freq, fourier_wave = utils.generate_fourier_wave(wave)

plt.plot(freq[1:500], np.abs(fourier_wave[1:500]))
plt.show()