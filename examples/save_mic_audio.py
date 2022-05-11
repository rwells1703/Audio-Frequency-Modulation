import audio
import audio_file

stream_play, stream_record = audio.start()

data = audio.record_audio(stream_record, 2)
audio_file.save_audio_file(data)