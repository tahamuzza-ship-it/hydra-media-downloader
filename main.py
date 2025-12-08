from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import subprocess
import os
import base64
import shutil

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HYDRA + Whisper listo."}

class Link(BaseModel):
    url: str

@app.post("/process-link")
async def process_link(link: Link):
    try:
        # Paths
        video_path = "/tmp/input.mp4"
        wav_path = "/tmp/output.wav"

        # LIMPIAR ARCHIVOS ANTES
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

        # OPCIONES para evitar postprocesadores de FFmpeg
        ydl_opts = {
            "format": "mp4",
            "outtmpl": video_path,
            "postprocessors": []  # 🚫 NO usar NINGÚN postprocessor
        }

        # DESCARGA SIN PROCESAR
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.url])

        # 🔥 CONVERTIR A WAV usando el FFmpeg del sistema
        subprocess.run(
            ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", wav_path, "-y"],
            check=True
        )

        # LEER WAV COMO BASE64
        with open(wav_path, "rb") as f:
            wav_bytes = f.read()
            wav_base64 = base64.b64encode(wav_bytes).decode("utf-8")

        return {
            "filename": "audio.wav",
            "audio_base64": wav_base64
        }

    except Exception as e:
        return {"error": str(e)}
