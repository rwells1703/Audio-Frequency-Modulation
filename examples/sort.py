import numpy as np

n = 5

freqs =        [235, 5344, 7432, 2522, 240, 1318, 543, 921, 5341]
fourier_wave = [1,   6,    2,    5,    3,   8,    1,   9,   6]

ind = np.argsort(fourier_wave)

sorted_freqs = []
for i in ind:
    sorted_freqs.append(freqs[i])
sorted_freqs = np.flip(sorted_freqs)

rounded_freqs = list(map(lambda f : round(f, -1), sorted_freqs))

unique_values = []
i = 0
c = n
while i < len(rounded_freqs) and c > 0:
    if not rounded_freqs[i] in unique_values:
        unique_values.append(rounded_freqs[i])
        c -= 1
    i += 1

print(unique_values)