import sounddevice as sd

fs = 44100

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

print(sd.query_devices())

try:
    with sd.Stream(samplerate=fs, dtype='float32', latency=None, channels=1, callback=callback):
        input()
except KeyboardInterrupt:
    pass