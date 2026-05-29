from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

tts.tts_to_file(
    text="hey abhinav... good to see you again",
    file_path="output.wav"
)

print("done")