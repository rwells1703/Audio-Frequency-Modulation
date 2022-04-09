import numpy as np
from matplotlib import pyplot as plt

import utils

pyaudio_instance, stream_play, stream_record = utils.start_pyaudio()

frames = utils.record_audio(stream_record)

utils.save_audio_file(pyaudio_instance, frames)
wave = utils.audio_frames_to_wave(frames)

utils.stop_pyaudio(pyaudio_instance, stream_play, stream_record)

plt.plot(np.linspace(0, 1, len(wave)), wave)

plt.show()