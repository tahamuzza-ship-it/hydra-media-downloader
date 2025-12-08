from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import os
import traceback

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HYDRA Media Downloader activo."}

class Link(BaseModel):
    url: str

@app.post("/process-link")
async def process_link(link: Link):
    try:
        # Archivo final: audio puro sin procesar
        audio_path = "/tmp/audio.webm"

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_path,
            "postprocessors": []  # <---- IMPORTANTE: SIN FFMPEG
        }

        # Descargar audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.url])

        # Leer archivo descargado
        if not os.path.exists(audio_path):
            return {"error": "No se descargó el audio."}

        with open(audio_path, "rb") as f:
            content = f.read()

        return {
            "filename": "audio.webm",
            "audio_base64": content.hex()
        }

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
