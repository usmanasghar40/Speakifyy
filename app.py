from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from pydub import AudioSegment
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'static/combined_audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('book-upload')
    if file:
        file.save(f'uploads/{file.filename}')
        return redirect(url_for('next_page'))
    return redirect(url_for('home'))

# This will show nextpage with or without combined audio
@app.route('/nextpage', methods=['GET'])
def next_page():
    return render_template('nextpage.html', combined_audio=None)

# Audio combiner route will process POST, then redirect back to /nextpage
@app.route('/combine', methods=['POST'])
def combine_audio():
    audio_files = request.files.getlist('audio_files')
    if not audio_files:
        return redirect(url_for('next_page'))

    combined = None
    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined = audio if combined is None else combined + audio

    filename = f"combined_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    output_path = os.path.join(UPLOAD_FOLDER, filename)
    combined.export(output_path, format="mp3")

    return render_template('nextpage.html', combined_audio=filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
