from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import yt_dlp
import subprocess
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "HYDRA Media Downloader activo."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

class Link(BaseModel):
    url: str

@app.post("/process-link")
async def process_link(link: Link):
    video_path = "/tmp/input.mp4"
    audio_path = "/tmp/output.wav"

    # 1. Descargar el video
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': video_path,
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link.url])

    # 2. Convertir a WAV
    subprocess.run(["ffmpeg", "-i", video_path, audio_path, "-y"], check=True)

    # 3. Leer WAV como HEX
    with open(audio_path, "rb") as f:
        content = f.read()

    return {"wav_base64": content.hex()}
