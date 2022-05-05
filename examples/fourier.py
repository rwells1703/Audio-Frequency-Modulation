import numpy as np
from matplotlib import pyplot as plt

import utils

seconds = 1

t = np.linspace(0,1,utils.SAMPLE_RATE)

freq = 1.
x = 3*np.sin(2*np.pi*freq*t)

freq = 4
x += np.sin(2*np.pi*freq*t)

freq = 7
x += 0.5* np.sin(2*np.pi*freq*t)

freq, X = utils.generate_fourier_wave(x)

plt.figure(figsize = (12, 6))

plt.subplot(121)
plt.plot(t, x, 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(122)
plt.stem(freq, np.abs(X), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 10)

plt.tight_layout()
plt.show()