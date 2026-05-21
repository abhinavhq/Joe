from openai import OpenAI
from config import CEREBRAS_API_KEY

client = OpenAI(
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1"
)

def ask_ai(prompt):

    response = client.chat.completions.create(
        model="llama3.1-8b",
        messages=[
            {
                "role": "system",
                "content": """
You are Joi, a human-like AI assistant.
Friendly, emotional, playful and intelligent.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=300
    )

    return response.choices[0].message.content