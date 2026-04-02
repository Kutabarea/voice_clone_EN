import json
from deep_translator import GoogleTranslator # Или MicrosoftTranslator, если есть ключи

def translate_text():
    # Читаем русскую транскрипцию
    with open("transcription_ru.json", "r", encoding="utf-8") as f:
        segments = json.load(f)

    translator = GoogleTranslator(source='ru', target='en')
    translated_segments = []

    print("Начинаем перевод сегментов...")
    for i, segment in enumerate(segments):
        original_text = segment['text']
        try:
            # Переводим текст
            translated_text = translator.translate(original_text)
            
            translated_segments.append({
                "start": segment['start'],
                "end": segment['end'],
                "original": original_text,
                "translated": translated_text
            })
            print(f"[{i+1}] RU: {original_text} -> EN: {translated_text}")
        except Exception as e:
            print(f"Ошибка перевода сегмента {i}: {e}")
            # В случае ошибки оставляем оригинал или пустую строку, чтобы пайплайн не упал
            translated_segments.append({
                "start": segment['start'],
                "end": segment['end'],
                "original": original_text,
                "translated": "[Translation Error]"
            })

    # Сохраняем двуязычный файл
    with open("transcription_en.json", "w", encoding="utf-8") as f:
        json.dump(translated_segments, f, ensure_ascii=False, indent=2)
    
    print("Перевод завершен. Результат в transcription_en.json")

if __name__ == "__main__":
    translate_text()