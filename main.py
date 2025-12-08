from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import yt_dlp
import subprocess
import base64
import os

app = FastAPI()

class Link(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "HYDRA Media Downloader activo."}

@app.post("/process-link")
def process_link(link: Link):
    video_path = "/tmp/video.mp4"
    audio_path = "/tmp/audio.wav"

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": video_path,
            "noplaylist": True,
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.url])

        subprocess.run(["ffmpeg", "-i", video_path, audio_path, "-y"], check=True)

        with open(audio_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        return {
            "filename": "audio.wav",
            "audio_base64": encoded
        }

    except Exception as e:
        return {"error": str(e)}
