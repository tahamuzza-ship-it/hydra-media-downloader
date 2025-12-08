import os
from openai import OpenAI

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not found in environment!")
    return OpenAI(api_key=api_key)

def analyze_transcript(text: str):
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un analizador experto."},
            {"role": "user", "content": text},
        ]
    )

    return response.choices[0].message["content"]
