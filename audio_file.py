import wave as w

import audio

# Save the recorded audio frames to a wav file
def save_audio_file(frames):
    with w.open("sound.wav", 'wb') as file:
        # Set the parameters for the audio file
        file.setnchannels(audio.CHANNELS)
        file.setsampwidth(audio.RECORD_BITS)
        file.setframerate(audio.SAMPLE_RATE)
        file.writeframes(frames)

# Read the audio file and output the data in bytes
def read_audio_file():
    with w.open("sound.wav") as file:
        frame_number = file.getnframes()
        data = file.readframes(frame_number)

    return data