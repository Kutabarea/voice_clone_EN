from pydub import AudioSegment
import json
from pathlib import Path
import config
import os
import sys
import os
# Добавляем корень проекта в путь, если скрипт запускается напрямую
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
def assemble_audio(transcript_json, segments_dir, output_path):
    """Собирает аудиофайлы в один трек с учетом таймингов."""
    print("🧩 Сборка финального аудиотрека...")

    with open(transcript_json, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    # Определяем общую длительность по последнему сегменту
    total_duration_ms = int(segments[-1]['end'] * 1000) + 1000 # +1 сек запас
    final_track = AudioSegment.silent(duration=total_duration_ms)

    for i, seg in enumerate(segments):
        filename = f"segment_{i:04d}.wav"
        filepath = segments_dir / filename
        
        if not filepath.exists():
            print(f"⚠️ Пропущен файл {filename}, вставляем тишину.")
            continue

        segment_audio = AudioSegment.from_wav(str(filepath))
        
        # Обрезаем, если сегмент длиннее отведенного времени (редко, но бывает)
        duration_ms = (seg['end'] - seg['start']) * 1000
        if len(segment_audio) > duration_ms:
            segment_audio = segment_audio[:duration_ms]
        
        # Накладываем на позицию start
        start_ms = int(seg['start'] * 1000)
        final_track = final_track.overlay(segment_audio, position=start_ms)

    # Нормализация громкости (чтобы не было слишком тихо или громко)
    final_track = final_track.normalize()
    
    # Экспорт
    final_track.export(str(output_path), format="wav")
    print(f"✅ Аудиотрек собран: {output_path}")

if __name__ == "__main__":
    transcript_json = config.TEMP_DIR / "translated.json"
    segments_dir = config.TEMP_DIR / "audio_segments"
    output_audio = config.OUTPUTS_DIR / "dubbed_audio.wav"

    assemble_audio(transcript_json, segments_dir, output_audio)