import whisper
import torch
from pydub import AudioSegment
import subprocess
from pathlib import Path
import json
import config
import sys
import os
# Добавляем корень проекта в путь, если скрипт запускается напрямую
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
def extract_audio(video_path, output_audio_path):
    """Извлекает аудио из видео файла."""
    print(f"🎬 Извлечение аудио из {video_path}...")
    # Используем ffmpeg через subprocess для надежности
    command = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(output_audio_path)
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Аудио извлечено.")

def transcribe_audio(audio_path, output_json_path):
    """Транскрибирует аудио с таймингами."""
    print(f"🎙️ Транскрибация с использованием модели {config.WHISPER_MODEL}...")
    
    if not torch.cuda.is_available():
        print("⚠️ CUDA не найдена, работа на CPU (будет медленно).")
        device = "cpu"
    else:
        device = "cuda"

    model = whisper.load_model(config.WHISPER_MODEL, device=device)
    
    result = model.transcribe(
        str(audio_path),
        language="ru",
        word_timestamps=True, # Важно для синхронизации
        task="transcribe"
    )

    segments = []
    for segment in result['segments']:
        segments.append({
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text'].strip()
        })

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"✅ Транскрибация завершена. Сохранено в {output_json_path}")
    return segments

if __name__ == "__main__":
    if not config.INPUT_VIDEO_PATH.exists():
        print(f"❌ Ошибка: Видеофайл не найден по пути {config.INPUT_VIDEO_PATH}")
        exit(1)

    temp_audio = config.TEMP_DIR / "original_audio.wav"
    transcript_json = config.TEMP_DIR / "transcript.json"

    extract_audio(config.INPUT_VIDEO_PATH, temp_audio)
    transcribe_audio(temp_audio, transcript_json)