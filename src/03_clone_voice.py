import torch
from TTS.api import TTS
import json
import os
from pathlib import Path
import config
from pydub import AudioSegment
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def generate_cloned_audio(transcript_json, output_dir):
    """Генерирует аудио для каждой фразы с клонированием голоса."""
    print("🤖 Инициализация модели XTTS v2...")
    
    if not torch.cuda.is_available():
        print("⚠️ Внимание: Работа на CPU будет очень медленной!")
        device = "cpu"
    else:
        device = "cuda"

    # Инициализация модели
    tts = TTS(config.XTTS_MODEL_NAME).to(device)

    with open(transcript_json, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    reference_speaker = str(config.REFERENCE_AUDIO_PATH)
    
    if not os.path.exists(reference_speaker):
        print(f"❌ Файл образца голоса не найден: {reference_speaker}")
        print("💡 Положите файл 'reference_voice.wav' в папку assets/")
        exit(1)

    print(f"🗣️ Генерация речи (образец: {reference_speaker})...")

    for i, seg in enumerate(segments):
        text = seg['translated']
        output_filename = f"segment_{i:04d}.wav"
        output_path = output_dir / output_filename
        
        print(f"Generating [{i+1}/{len(segments)}]: {text[:40]}...")
        
        try:
            tts.tts_to_file(
                text=text,
                speaker_wav=reference_speaker,
                language=config.TARGET_LANGUAGE,
                file_path=str(output_path)
            )
        except Exception as e:
            print(f"❌ Ошибка генерации сегмента {i}: {e}")
            # Создаем тишину вместо пропуска, чтобы не сбить тайминги
            silence = AudioSegment.silent(duration=(seg['end'] - seg['start']) * 1000)
            silence.export(str(output_path), format="wav")

    print("✅ Генерация всех сегментов завершена.")

if __name__ == "__main__":
    input_json = config.TEMP_DIR / "translated.json"
    audio_segments_dir = config.TEMP_DIR / "audio_segments"
    audio_segments_dir.mkdir(exist_ok=True)

    if not input_json.exists():
        print("❌ Сначала запустите 02_translate.py")
        exit(1)

    generate_cloned_audio(input_json, audio_segments_dir)