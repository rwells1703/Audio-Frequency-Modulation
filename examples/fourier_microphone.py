from matplotlib import pyplot as plt

import audio
import waves

stream_play, stream_record = audio.start()

wave = audio.record_audio(stream_record, 5, 1024)

#wave = np.frombuffer(data, dtype=np.int16)

frequencies, fourier_wave = waves.generate_fourier_wave(wave)

plt.plot(frequencies, fourier_wave)
plt.show()