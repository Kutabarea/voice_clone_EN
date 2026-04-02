import os
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUTS_DIR = BASE_DIR / "outputs"
TEMP_DIR = BASE_DIR / "temp"

# Создаем директории, если их нет
for directory in [ASSETS_DIR, OUTPUTS_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# --- Input Files ---
# Положите исходное видео сюда и укажите имя файла
INPUT_VIDEO_NAME = "input_video.mp4" 
INPUT_VIDEO_PATH = ASSETS_DIR / INPUT_VIDEO_NAME
REFERENCE_AUDIO_PATH = ASSETS_DIR / "reference_voice.wav" # Чистый образец голоса (15-30 сек)

# --- Model Settings ---
WHISPER_MODEL = "large-v3"  # Варианты: tiny, base, small, medium, large-v3
XTTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cuda"  # Или "cpu", если нет видеокарты

# --- Translation Settings ---
TARGET_LANGUAGE = "en"  # Целевой язык (en, de, fr, es...)
SOURCE_LANGUAGE = "ru"

# --- LipSync Settings ---
LIPSYNC_MODEL_PATH = "checkpoints/wav2lip_gan.pth" # Путь к модели Wav2Lip (нужно скачать отдельно)

# --- Output Settings ---
FINAL_OUTPUT_NAME = "ruslan_dubbed_en.mp4"