from flask import Flask, request
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

YOUTUBE_STREAM_URL = "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Hentikan stream sebelumnya (opsional)
    subprocess.run(['pkill', 'ffmpeg'])

    # Mulai stream loop dengan ffmpeg
    subprocess.Popen([
        'ffmpeg',
        '-stream_loop', '-1',
        '-re',
        '-i', filepath,
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-maxrate', '3000k',
        '-bufsize', '6000k',
        '-pix_fmt', 'yuv420p',
        '-g', '50',
        '-c:a', 'aac',
        '-b:a', '160k',
        '-f', 'flv',
        YOUTUBE_STREAM_URL
    ])

    return "Video diupload & streaming dimulai!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
