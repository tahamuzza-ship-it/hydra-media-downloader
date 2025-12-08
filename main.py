import traceback

@app.post("/process-link")
async def process_link(link: Link):
    try:
        video_path = "/tmp/input.mp4"
        audio_path = "/tmp/output.wav"

        # 1. Descargar el video (formato seguro compatible con YouTube en Railway)
        ydl_opts = {
            'format': 'mp4',  # evita bestvideo+bestaudio que falla con algunos videos y contenedores
            'outtmpl': video_path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link.url])

        # Verificar que el archivo se descargó
        if not os.path.exists(video_path) or os.path.getsize(video_path) < 1000:
            return {
                "error": "El archivo no se descargó correctamente.",
                "trace": "input.mp4 no existe o está vacío."
            }

        # 2. Convertir a WAV
        result = subprocess.run(
            ["ffmpeg", "-i", video_path, audio_path, "-y"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "error": "Error ejecutando ffmpeg.",
                "trace": result.stderr
            }

        # Verificar que el WAV exista
        if not os.path.exists(audio_path):
            return {
                "error": "ffmpeg no generó el archivo WAV.",
                "trace": "output.wav no encontrado."
            }

        # 3. Leer WAV como HEX
        with open(audio_path, "rb") as f:
            content = f.read()

        return {"wav_base64": content.hex()}

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }
