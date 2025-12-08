from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import yt_dlp
import subprocess
import os
import uvicorn

app = FastAPI()

# ---------- RUTA PRINCIPAL ----------
@app.get("/")
def root():
    return {"message": "HYDRA Media Downloader activo."}

# ---------- ENDPOINT PARA ARCHIVOS (OPCIONAL) ----------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

# ---------- ENDPOINT PARA ENLACES ----------
class Link(BaseModel):
    url: str

@app.post("/process-link")
async def process_link(link: Link):
    video_path = "input.mp4"
    audio_path = "output.wav"

    # --- 1. Descargar video de YouTube ---
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': video_path,
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link.url])

    # --- 2. Convertir a WAV ---
    subprocess.run(["ffmpeg", "-i", video_path, audio_path, "-y"])

    # --- 3. Devolver WAV como base64 HEX ---
    with open(audio_path, "rb") as f:
        content = f.read()

    return {"wav_base64": content.hex()}

# ---------- INICIAR UVICORN CORRECTO PARA RAILWAY ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
