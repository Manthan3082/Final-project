from deep_translator import GoogleTranslator

# Default translation function
def translate_text(text, target_lang="en"):
    if target_lang == "en":
        return text
    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"[Translation Error] {text}"