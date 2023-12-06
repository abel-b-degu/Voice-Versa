from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from transcribe import start_transcription
from flask_cors import CORS
from threading import Thread
import googletrans
from googletrans import Translator

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode='gevent')

translator = Translator()

@app.route('/')
def home():
    return render_template('index.html', languages=googletrans.LANGUAGES.items())

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        source_text = data.get('text', '')
        source_lang = data.get('source', '')
        target_lang = data.get('target', '')

        if not source_lang:
            # Auto-detect source language if not provided
            source_lang = translator.detect(source_text).lang

        translation = translator.translate(source_text, src=source_lang, dest=target_lang).text
        return jsonify({'translation': translation})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('start_transcription')
def handle_start_transcription():
    try:
        recognize_thread = Thread(target=start_transcription, args=(socketio,))
        recognize_thread.start()

    except Exception as e:
        emit('transcription_error', {'error': str(e)})


if __name__ == '__main__':
    socketio.run(app, debug=True)