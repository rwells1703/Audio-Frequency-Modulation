
from matplotlib import pyplot as plt
import audio
import waves

stream_play, stream_record = audio.start()

seconds = 5
w = waves.generate_flat_signal(0, seconds)

freqs = [400,500,800]

for f in freqs:
    new_w = waves.generate_wave(f, 1, 1, seconds)
    w = w + new_w

w /= len(freqs)

t = waves.generate_time_axis(seconds, 1)

plt.grid(axis = "y")
plt.plot(t, w)
plt.show()

audio.play_wave(stream_play, w)