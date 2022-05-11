import sounddevice as sd
import time

x = 0

def callback(indata, frames, time, status):
    global x
    if status:
        print(status)
    
    print(x)
    x += 1
    #outdata[:] = indata


stream_record = sd.InputStream(
    samplerate=44800,
    channels=1,
    dtype="int16",
    blocksize=int(44800*0.001),
    callback=callback)

stream_record.start()

with stream_record:
    input()
#while True:
    #d = stream_record.read(1024)[0]
    #print(stream_record.latency)