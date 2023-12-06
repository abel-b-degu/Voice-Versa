from flask import Flask, render_template, request, jsonify
import googletrans
from googletrans import Translator

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)