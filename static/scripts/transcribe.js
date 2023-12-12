const transcription = document.getElementById('transcription');
const microphoneIcon = document.querySelector('.fa-microphone');
let isRecording = false;
let lastTranscription = ''

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;


recognition.onstart = function() {
    transcription.value = '';
    transcription.placeholder = 'Listening...';
    microphoneIcon.style.color = 'red';
};

recognition.onresult = function (event) {
    let interimTranscript = '';
    for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
            transcription.value = event.results[i][0].transcript + '\n';
            lastTranscription = transcription.value; // Update lastTranscription with the current value
            displayTranslation();
            // speakText();
        } else {
            interimTranscript += event.results[i][0].transcript;
            displayTranslation();
        }
    }
    // Update the transcription in real-time
    transcription.value = lastTranscription + interimTranscript;
};

recognition.onerror = function(event) {
    transcription.placeholder = 'Error occurred. Please try again.';
    microphoneIcon.style.color = '';
};

recognition.onend = function() {
    transcription.placeholder = 'Click "Start Recording" to begin.';
    microphoneIcon.style.color = ''; // Use an empty string to revert to default
    lastTranscription = transcription.value;
    speakText();
};

function toggleTranscription() {
    if (!isRecording) {
        // Start transcription
        recognition.start();
        transcription.value = '';
        isRecording = true;
    } else {
        // Stop transcription
        recognition.stop();
        isRecording = false;
    }
}
