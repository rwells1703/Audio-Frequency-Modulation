from matplotlib import pyplot as plt

import audio
import waves

bs = 1024
stream_play, stream_record = audio.start(bs)

wave = audio.record_audio(stream_record, 5, bs)

frequencies, fourier_wave = waves.generate_fourier_wave(wave)

plt.plot(frequencies, fourier_wave)
plt.show()