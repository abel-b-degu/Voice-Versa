function speakText() {
    var textToSpeak = document.getElementById('translation').value;
    var langDropdown = document.getElementById('target-lang');

    var language = langDropdown.options[langDropdown.selectedIndex].value;

    var utterance = new SpeechSynthesisUtterance(textToSpeak);

    utterance.lang = language;

    speechSynthesis.speak(utterance);
}