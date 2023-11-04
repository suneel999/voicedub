import os
from flask import Flask, request, render_template, send_file
from gradio_client import Client

app = Flask(__name__)
client = Client("https://fffiloni-videoretalking.hf.space/--replicas/8tzlv/")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the uploaded video and audio files
        video_file = request.files["video"]
        audio_file = request.files["audio"]

        # Save the files to the server
        video_path = "uploads/" + video_file.filename
        audio_path = "uploads/" + audio_file.filename
        video_file.save(video_path)
        audio_file.save(audio_path)

        # Open the saved files as file objects
        with open(video_path, "rb") as video_file, open(audio_path, "rb") as audio_file:
            # Pass the file objects to the Gradio API for prediction
            result = client.predict(
                {"video": video_file, "audio": audio_file},  # Dict(video: file object, audio: file object) in 'Source Video' and 'Audio Target' components
                api_name="/infer"
            )

        # Return the resulting video to the user
        return send_file(result["video"], as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
