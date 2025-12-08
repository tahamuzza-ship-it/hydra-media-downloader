from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import yt_dlp
import base64
import os
from openai import OpenAI
from analyzer import analyze_transcript

client = OpenAI()
app = FastAPI()

class Link(BaseModel):
    url: str

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "wav"}
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.exists("audio.wav"):
        with open("audio.wav", "rb") as f:
            audio_bytes = f.read()
        return audio_bytes
    else:
        return None

@app.post("/process-link")
def process_link(link: Link):
    try:
        audio_bytes = download_audio(link.url)

        if audio_bytes is None:
            return {"error": "No se pudo descargar el audio"}

        # Convertimos audio a base64
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        # Guardamos temporalmente
        with open("temp.wav", "wb") as f:
            f.write(audio_bytes)

        # --- TRANSCRIPCIÓN WHISPER ---
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=open("temp.wav", "rb")
        )

        transcript_text = transcript.text

        # --- ANALYSIS ---
        analysis_json = analyze_transcript(transcript_text)

        return {
            "filename": "audio.wav",
            "audio_base64": audio_b64,
            "transcript": transcript_text,
            "analysis": analysis_json
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
