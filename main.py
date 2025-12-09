from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"status": "OK", "message": "Hydra Downloader funcionando."}

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL no proporcionada"}), 400

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_path = f"downloads/{info['id']}.mp3"

        return jsonify({
            "status": "success",
            "file": audio_path
        })

    except Exception as e:
        print("🔥 ERROR en descarga:", str(e))  # <- para ver errores en Railway
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Puerto seguro para Railway
    port = int(os.environ.get("PORT", "8080"))

    print(f"🚀 Iniciando Hydra Downloader en puerto {port}...")  # <- SE VERÁ EN LOGS
    app.run(host="0.0.0.0", port=port, debug=True)
