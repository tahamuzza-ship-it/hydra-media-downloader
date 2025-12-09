from flask import Flask, request, jsonify
import yt_dlp
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"status": "OK", "message": "Hydra funcionando (modo audio base64)."}

@app.route("/process-link", methods=["POST"])
def process_link():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL no proporcionada"}), 400

    # yt-dlp: descarga el audio en memoria (no en archivo)
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "outtmpl": "-",   # --- IMPORTANTE: NO genera archivo ---
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128"
        }],
    }

    try:
        buffer = BytesIO()

        def write_hook(d):
            if d['status'] == 'finished' and 'filepath' in d:
                with open(d['filepath'], 'rb') as f:
                    buffer.write(f.read())

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_path = f"{info['id']}.mp3"

        # Leer audio descargado
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        # Convertir a base64
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        # Respuesta lista para Whisper
        return jsonify({
            "status": "success",
            "audio_base64": audio_b64
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "8080"))
    print(f"Hydra audio-base64 en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
