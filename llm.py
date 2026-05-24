from openai import OpenAI
from config import CEREBRAS_API_KEY

client = OpenAI(
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1"
)

def ask_ai_stream(prompt):

    stream = client.chat.completions.create(
        model="llama-3.1-8b",
        messages=[
            {
                "role": "system",
                "content": """
You are Joi, a human-like assistant.
Friendly, emotional, playful and natural.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=300,
        stream=True
    )

    full_reply = ""

    for chunk in stream:

        delta = chunk.choices[0].delta.content

        if delta:

            print(delta, end="", flush=True)

            full_reply += delta

    print()

    return full_reply