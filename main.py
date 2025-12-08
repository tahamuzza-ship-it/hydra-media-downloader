from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "OK", "message": "HYDRA Media Downloader is running."})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"downloads/{info['id']}.mp3"

        return jsonify({"status": "success", "file": filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
