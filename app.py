from Flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# Default download folder (inside the Downloads directory)
DEFAULT_DOWNLOAD_FOLDER = os.path.expanduser("~/Downloads/YT_Videos")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    video_url = data.get("video_url")
    storage_path = data.get("storage_path", DEFAULT_DOWNLOAD_FOLDER)  # Default path if none provided

    if not video_url:
        return jsonify({"status": "error", "message": "Missing video URL"}), 400

    # Ensure the folder exists
    os.makedirs(storage_path, exist_ok=True)

    # yt-dlp options
    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(storage_path, "%(title)s.%(ext)s"),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get("title", "video")
            video_extension = info.get("ext", "mp4")
            video_file = f"{video_title}.{video_extension}"
            video_path = os.path.join(storage_path, video_file)

        # Send the file for download in the browser
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)