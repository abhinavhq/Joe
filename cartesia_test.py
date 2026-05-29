from cartesia import Cartesia

client = Cartesia(
    api_key="sk_car_MmRpUuXpfqmrUNw4y4BXyq"
)

audio = client.tts.bytes(
    model_id="sonic-2",
    transcript="hey abhinav... good to see you again.",
    voice={
        "mode": "id",
        "id": "694f9389-aac1-45b6-b726-9d9369183238"
    },
    language="en",
    output_format={
        "container": "wav",
        "encoding": "pcm_f32le",
        "sample_rate": 44100,
    },
)

with open("output.wav", "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("DONE 😭🔥")