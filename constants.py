import numpy as np

# Define audio stream parameters
SAMPLE_RATE = 48000
CHANNELS = 1
FORMAT_RECORD = "int16"
RECORD_BITS = 16

# Time taken for a single segment to play
BFSK_SEGMENT_TIME = 0.2
MFSK_SEGMENT_TIME = 0.2

# The number of bits in a recorded audio block
BFSK_RECORDING_BLOCK_SIZE = int(SAMPLE_RATE * (BFSK_SEGMENT_TIME / 8))
MFSK_RECORDING_BLOCK_SIZE = 1024

# Define the frequency channels for BFSK
BFSK_CHANNELS = [(1000,1200,3000), (1400,1600,3200), (1800, 2000, 3400)]
BFSK_CHANNEL_COUNT = len(BFSK_CHANNELS)

# The proportion of values within a sample group (of CERTAINTY_SAMPLE_SIZE) that should be identical, before storing the value
# e.g. 80% or more of the values in the sample should be equal to 1 (or perhaps [0,1,1] in BFSK), otherwise the value will not be stored
BFSK_CERTAINTY = 5
BFSK_CERTAINTY_SAMPLE_SIZE = 10

MFSK_CERTAINTY = 6
MFSK_CERTAINTY_SAMPLE_SIZE = 9

# Define the number of bits per segment used for MFSK
MFSK_SEGMENT_BITS = 7

# Increments by the step at which recoreded frequencies are quantized
MFSK_RECORD_FREQ_STEP = SAMPLE_RATE/MFSK_RECORDING_BLOCK_SIZE

# The frequency range used for MFSK
MFSK_MIN_FREQ = 600
MFSK_MIN_FREQ = MFSK_MIN_FREQ - (MFSK_MIN_FREQ%MFSK_RECORD_FREQ_STEP)
MFSK_MAX_FREQ = MFSK_MIN_FREQ+(2**MFSK_SEGMENT_BITS)*MFSK_RECORD_FREQ_STEP
MFSK_FREQ_RANGE = np.arange(start=MFSK_MIN_FREQ, stop=MFSK_MAX_FREQ, step=MFSK_RECORD_FREQ_STEP)