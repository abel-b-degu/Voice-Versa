// Function to exchange source and target languages
function exchangeLanguages() {
    var sourceLang = document.getElementById('source-lang').value;
    var sourceText = document.getElementById('transcription').value;
    var targetLang = document.getElementById('target-lang').value;
    var targetText = document.getElementById('translation').value;


    document.getElementById('source-lang').value = targetLang;
    document.getElementById('transcription').value = targetText;
    document.getElementById('target-lang').value = sourceLang;
    document.getElementById('translation').value = sourceText;
}

// Function to translate text
function displayTranslation() {
    var sourceText = document.getElementById('transcription').value;
    var sourceLang = document.getElementById('source-lang').value;
    var targetLang = document.getElementById('target-lang').value;

    getTranslation(sourceText, sourceLang, targetLang)
    .then(translation => {
        document.getElementById('translation').value = translation;
    })
    .catch(error => {
        console.error('Translation error:', error);
    });
}

// Function to perform translation on the server
function getTranslation(sourceText, sourceLang, targetLang) {
    return fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: sourceText, source: sourceLang, target: targetLang }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        return data.translation;
    })
    .catch(error => {
        console.error('Translation error:', error);
        throw error;
    });
}

// Function to copy text to clipboard using Clipboard API
function copyText(id) {
    var textArea = id == 'transcription' ? document.getElementById('transcription') : document.getElementById('translation')
    var textToCopy = textArea.value;

    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            console.log('Text successfully copied to clipboard');
        })
        .catch(err => {
            console.error('Unable to copy text to clipboard', err);
        });
}

function speakText() {
    var textToSpeak = document.getElementById('translation').value;
    var langDropdown = document.getElementById('target-lang');

    var language = langDropdown.options[langDropdown.selectedIndex].value;

    var utterance = new SpeechSynthesisUtterance(textToSpeak);

    utterance.lang = language;

    speechSynthesis.speak(utterance);
}