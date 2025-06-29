from flask import Flask, request, send_file, jsonify
import requests
import os
import uuid

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        spotify_url = data.get("spotify_url")

        if not spotify_url:
            return jsonify({"error": "Missing Spotify URL"}), 400

        # Fetch from SpotifyDown API
        api_url = f"https://api.spotifydown.com/download?url={spotify_url}"
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch from SpotifyDown"}), 500

        json_data = response.json()
        download_link = json_data.get("link")

        if not download_link:
            return jsonify({"error": "Download link not found"}), 500

        # Download the file
        file_data = requests.get(download_link)
        temp_filename = f"/tmp/{uuid.uuid4().hex}.mp3"
        with open(temp_filename, "wb") as f:
            f.write(file_data.content)

        return send_file(temp_filename, as_attachment=True, download_name="spotify_song.mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)