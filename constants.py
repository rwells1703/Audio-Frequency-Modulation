import numpy as np
import pyaudio

SEGMENT_TIME = 0.1

# Define pyaudio stream parameters
SAMPLE_RATE = 48000
FORMAT_PLAY = pyaudio.paFloat32
FORMAT_RECORD = pyaudio.paInt16
RECORDING_BLOCK_SIZE = int(SAMPLE_RATE * (SEGMENT_TIME / 2))
AUDIO_CHANNELS = 1

CHANNELS = [(1000,1200,600), (1400,1600,800), (1800,2000,1000)]

# Define the number of bits used in various places
SEGMENT_BITS = 1
PLAY_BITS = 32
RECORD_BITS = 16



# The proportion of values within a sample group (of CERTAINTY_SAMPLE_SIZE) that should be identical, before storing the value
# e.g. 80% or more of the values in [1,1,1,9,1,2,1,1] should be equal to 1, otherwise the value will not be stored
CERTAINTY = 6
CERTAINTY_SAMPLE_SIZE = 9



# Increments by the step at which recoreded frequencies are quantized
RECORD_FREQ_STEP = SAMPLE_RATE/RECORDING_BLOCK_SIZE

# Full frequency spectrum values available from mic (from 0 to 44100 Hz)
RECORD_FREQ_RANGE = np.arange(stop=SAMPLE_RATE, step=RECORD_FREQ_STEP)

MIN_FREQ = 600
MIN_FREQ = MIN_FREQ - (MIN_FREQ%RECORD_FREQ_STEP)
MAX_FREQ = MIN_FREQ+RECORD_FREQ_STEP
CLIPPED_FREQ_RANGE = np.arange(start=MIN_FREQ, stop=MAX_FREQ, step=RECORD_FREQ_STEP)