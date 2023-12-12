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

function checkEnterKey(event) {
    if (event.key === 'Enter') {
        displayTranslation();
        // Prevent the default newline in the textarea
        event.preventDefault();
    }
}