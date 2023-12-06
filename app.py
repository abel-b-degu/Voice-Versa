from flask import Flask, render_template, request
from flask_socketio import SocketIO
from transcribe import start_transcription, set_socketio_instance
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

set_socketio_instance(socketio)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('start_transcription')
def handle_start_transcription():
    try:
        start_transcription()
    except Exception as e:
        socketio.emit('transcription_error', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)