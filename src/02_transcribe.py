import json
from deep_translator import GoogleTranslator
from pathlib import Path
import config
import time
import sys
import os
# Добавляем корень проекта в путь, если скрипт запускается напрямую
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
def translate_text(text, source, target):
    """Переводит текст с сохранением структуры."""
    translator = GoogleTranslator(source=source, target=target)
    try:
        # Небольшие задержки, чтобы не заблокировали
        time.sleep(0.5) 
        return translator.translate(text)
    except Exception as e:
        print(f"⚠️ Ошибка перевода: {e}")
        return text

def process_transcript(input_json, output_json):
    """Читает транскрипт, переводит и сохраняет."""
    print("🌐 Перевод текста...")
    
    with open(input_json, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    translated_segments = []
    
    for i, seg in enumerate(segments):
        original = seg['text']
        # Пропускаем пустые или слишком короткие (шум)
        if len(original) < 2:
            continue
            
        translated = translate_text(original, config.SOURCE_LANGUAGE, config.TARGET_LANGUAGE)
        
        translated_segments.append({
            "start": seg['start'],
            "end": seg['end'],
            "original": original,
            "translated": translated
        })
        
        print(f"[{i+1}/{len(segments)}] RU: {original[:30]}... -> EN: {translated[:30]}...")

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(translated_segments, f, ensure_ascii=False, indent=2)

    print(f"✅ Перевод завершен. Сохранено в {output_json}")

if __name__ == "__main__":
    input_file = config.TEMP_DIR / "transcript.json"
    output_file = config.TEMP_DIR / "translated.json"
    
    if not input_file.exists():
        print("❌ Сначала запустите 01_transcribe.py")
        exit(1)
        
    process_transcript(input_file, output_file)