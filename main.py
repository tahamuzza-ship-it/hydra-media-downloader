from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import subprocess
import os
import base64

app = FastAPI()

class Link(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "HYDRA + Whisper listo."}

@app.post("/process-link")
async def process_link(link: Link):
    try:
        video_path = "/tmp/input.webm"
        wav_path = "/tmp/output.wav"

        # ─────────────────────────────────────
        # 1. DESCARGA SOLO AUDIO (webm)
        # ─────────────────────────────────────
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": video_path,
            "postprocessors": [
                {"key": "FFmpegCopyAudio", "preferredcodec": "webm"}
            ]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.url])

        # ─────────────────────────────────────
        # 2. CONVERTIR WEBM → WAV (si existe ffmpeg)
        # ─────────────────────────────────────
        try:
            subprocess.run(
                ["ffmpeg", "-i", video_path, wav_path, "-y"],
                check=True
            )
            wav_exists = True
        except Exception:
            wav_exists = False

        # ─────────────────────────────────────
        # 3. LEER ARCHIVOS COMO BASE64
        # ─────────────────────────────────────
        with open(video_path, "rb") as f:
            webm_base64 = base64.b64encode(f.read()).decode()

        wav_base64 = None
        if wav_exists:
            with open(wav_path, "rb") as f:
                wav_base64 = base64.b64encode(f.read()).decode()

        return {
            "status": "ok",
            "webm_base64": webm_base64,
            "wav_base64": wav_base64,
            "ffmpeg": wav_exists
        }

    except Exception as e:
        return {"error": str(e)}
