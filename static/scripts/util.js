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