import googletrans
from googletrans import Translator

# print(googletrans.LANGUAGES)


translator = Translator()

source_text = input("Enter the text you want to translate: ")

# Ask user if they know the source language or want to auto-detect it
source_lang = input("Enter the source language code (e.g., 'en' for English) or press Enter to auto-detect: ").lower().strip()

# Ask user for the target language
target_lang = input("Enter the target language code (e.g., 'es' for Spanish): ").lower().strip()

# If source language is not provided, googletrans will auto-detect it
translation = translator.translate(source_text, src=source_lang if source_lang else None, dest=target_lang)

# Print the translated text
print(f"Translated text ({translation.src} to {target_lang}): {translation.text}")
