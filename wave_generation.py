import numpy as np
import simpleaudio

def main():
    sample_rate = 44100
    seconds = 5
    time = np.linspace(0, seconds, seconds * sample_rate, False)
    note = np.sin(440 * time * 2 * np.pi)

    audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = audio.astype(np.int16)

    play_obj = simpleaudio.play_buffer(audio, 1, 2, sample_rate)

    play_obj.wait_done()

if __name__ == "__main__":
    main()