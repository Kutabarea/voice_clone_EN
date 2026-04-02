import torch
from TTS.api import TTS
import json
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Пути
REFERENCE_AUDIO = "reference_audio.wav"  # Чистый голос Руслана (10-20 сек)
TRANSLATION_FILE = "transcription_en.json"
OUTPUT_DIR = "generated_audio_parts"

def generate_voice():
    if not os.path.exists(REFERENCE_AUDIO):
        print(f"Ошибка: Файл {REFERENCE_AUDIO} не найден! Пожалуйста, создайте чистый сэмпл голоса.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Инициализация модели XTTS v2
    print("Загрузка модели XTTS v2... (это может занять время при первом запуске)")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

    with open(TRANSLATION_FILE, "r", encoding="utf-8") as f:
        segments = json.load(f)

    print("Генерация аудио по сегментам...")
    audio_files = []
    
    for i, segment in enumerate(segments):
        text = segment['translated']
        if not text or text == "[Translation Error]":
            continue
            
        output_filename = f"{OUTPUT_DIR}/part_{i:03d}.wav"
        
        print(f"Генерация сегмента {i}: {text[:50]}...")
        
        try:
            # Генерация аудио с клонированием голоса
            tts.tts_to_file(
                text=text,
                speaker_wav=REFERENCE_AUDIO,
                language="en",
                file_path=output_filename,
                speed=1.0  # Можно регулировать скорость, если английский короче/длиннее
            )
            audio_files.append((output_filename, segment['start'], segment['end']))
        except Exception as e:
            print(f"Ошибка генерации сегмента {i}: {e}")

    print("Все сегменты сгенерированы. Переходим к сборке...")
    assemble_audio(audio_files)

def assemble_audio(audio_data):
    # Создаем пустой аудиофайл длительностью как оригинал (примерно)
    # Для простоты склеим последовательно, но в идеале нужно расставлять по таймкодам
    
    # Получаем оригинальное аудио для определения общей длины
    # Примечание: здесь мы просто склеиваем части подряд для демонстрации.
    # Для точного попадания в тайминги нужна более сложная логика наложения.
    
    combined = AudioSegment.empty()
    for path, start, end in audio_data:
        part = AudioSegment.from_wav(path)
        combined += part
        
    combined.export("generated_full_audio.wav", format="wav")
    print("Аудио собрано в generated_full_audio.wav")

if __name__ == "__main__":
    generate_voice()