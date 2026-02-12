from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

app = Flask(__name__)

# ---------------------------------------------------
# Extraer ID del video
# ---------------------------------------------------
def extract_video_id(url):
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?&]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# ---------------------------------------------------
# Endpoint principal
# ---------------------------------------------------
@app.route("/process-link", methods=["POST"])
def process_link():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 415

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL no proporcionada"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "No se pudo extraer el video_id"}), 400

    try:
        # Nueva forma correcta
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        full_text = " ".join([t.text for t in transcript])

        return jsonify({
            "status": "success",
            "video_id": video_id,
            "transcript": full_text
        })

    except Exception as e:
        return jsonify({
            "error": "No se pudo obtener transcript",
            "details": str(e)
        }), 500


# ---------------------------------------------------
# Health check
# ---------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return {
        "status": "OK",
        "message": "Hydra Transcript API funcionando correctamente."
    }


# ---------------------------------------------------
# Run
# ---------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
