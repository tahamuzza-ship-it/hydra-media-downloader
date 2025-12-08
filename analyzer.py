import os
from openai import OpenAI

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    print("DEBUG: OPENAI_API_KEY =", api_key)  # ← DIAGNÓSTICO

    if not api_key:
        raise Exception("ERROR: OPENAI_API_KEY NOT FOUND in environment")

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
