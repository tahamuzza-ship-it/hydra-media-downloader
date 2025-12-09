from flask import Flask, request, jsonify
import requests
import base64
import re
import subprocess
import tempfile
import os

app = Flask(__name__)

def extract_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    return match.group(1) if match else None

@app.route("/process-link", methods=["POST"])
def process_link():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL no proporcionada"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "No se pudo extraer el video_id"}), 400

    # Obtener info de streaming (LEGAL)
    info_url = f"https://www.youtube.com/get_video_info?video_id={video_id}&el=detailpage"
    info = requests.get(info_url).text

    if "adaptive_fmts" not in info:
        return jsonify({"error": "YouTube no devolvió streams de audio"}), 500

    # Extraer streams disponibles
    import urllib.parse
    parsed = urllib.parse.parse_qs(info)
    fmts = parsed.get("adaptive_fmts", [None])[0]

    # Buscar stream de audio
    audio_url = None
    for fmt in fmts.split(","):
        if "audio" in fmt:
            parts = fmt.split("&")
            for p in parts:
                if p.startswith("url="):
                    audio_url = urllib.parse.unquote(p[4:])
                    break
            if audio_url:
                break

    if not audio_url:
        return jsonify({"error": "No se encontró un stream de audio"}), 500

    # Descargar el audio stream legalmente
    audio_bytes = requests.get(audio_url).content

    # Guardar en archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        f.write(audio_bytes)
        temp_path = f.name

    # Convertir a WAV usando ffmpeg
    wav_path = temp_path + ".wav"
    subprocess.run(["ffmpeg", "-i", temp_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", wav_path])

    # Leer WAV y convertir a B64
    with open(wav_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    # Limpiar archivos
    os.remove(temp_path)
    os.remove(wav_path)

    return jsonify({
        "status": "success",
        "audio_base64": audio_b64,
        "format": "wav"
    })


@app.route("/", methods=["GET"])
def home():
    return {"status": "OK", "message": "Hydra Downloader funcionando legalmente."}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
