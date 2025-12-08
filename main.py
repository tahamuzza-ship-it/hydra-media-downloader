from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import yt_dlp
import subprocess
import os
import traceback

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
    try:
        temp_path = "/tmp/audio"
        wav_path = temp_path + ".wav"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }

        # Descargar audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.url])

        # Verificar que WAV se generó
        if not os.path.exists(wav_path):
            return {
                "error": "No se generó el archivo WAV.",
                "trace": "yt-dlp no produjo el archivo .wav"
            }

        # Leer WAV como HEX
        with open(wav_path, "rb") as f:
            content = f.read()

        return {"wav_base64": content.hex()}

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
