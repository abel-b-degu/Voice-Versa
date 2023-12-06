import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from queue import Queue, Full
from flask_socketio import SocketIO

from config import watson_auth_key

# Flask-SocketIO instance
# socketio = SocketIO(message_queue='redis://', async_mode='gevent')
socketio = None

# Initialize queue to store the recordings
CHUNK = 1024
BUF_MAX_SIZE = CHUNK * 10
q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

# Create an instance of AudioSource
audio_source = AudioSource(q, True, True)

# Initialize speech to text service
authenticator = IAMAuthenticator(watson_auth_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)

class MyRecognizeCallback(RecognizeCallback):
    def on_transcription(self, transcript):
        transcription = transcript[0]['transcript']
        socketio.emit('transcription', {'transcription': transcription})

    def on_connected(self):
        print('Connection was successful')

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data[0]['transcript'])

    def on_close(self):
        print("Connection closed")

def recognize_using_websocket():
    mycallback = MyRecognizeCallback()
    speech_to_text.recognize_using_websocket(audio=audio_source,
                                             content_type='audio/l16; rate=44100',
                                             recognize_callback=mycallback,
                                             interim_results=True)

def pyaudio_callback(in_data, frame_count, time_info, status):
    try:
        q.put(in_data)
    except Full:
        pass  # discard
    return (None, pyaudio.paContinue)

def start_transcription():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=pyaudio_callback,
        start=False
    )

    stream.start_stream()

    try:
        recognize_thread = Thread(target=recognize_using_websocket, args=())
        recognize_thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_source.completed_recording()

def set_socketio_instance(si):
    global socketio
    socketio = si