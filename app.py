from flask import Flask, render_template, request, jsonify
from transcribe import transcribe_audio
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        transcription_thread = Thread(
            target=transcribe_audio, args=(audio_file,)
        )
        transcription_thread.start()
        return jsonify({'message': 'Transcription started'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)