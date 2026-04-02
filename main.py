import subprocess
import sys
from pathlib import Path
import config

def run_script(script_name):
    """Запускает указанный скрипт."""
    script_path = config.BASE_DIR / "src" / script_name
    print(f"\n▶️ Запуск {script_name}...")
    
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"✅ {script_name} завершен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка выполнения {script_name}: {e}")
        sys.exit(1)

def main():
    print("🚀 Запуск пайплайна AI Dubbing...")
    print(f"📂 Рабочая директория: {config.BASE_DIR}")
    
    # Проверка входных файлов
    if not config.INPUT_VIDEO_PATH.exists():
        print(f"❌ Ошибка: Видеофайл {config.INPUT_VIDEO_PATH} не найден!")
        print("💡 Положите видео в папку assets/ и обновите config.py")
        return

    # Этап 1: Транскрибация
    run_script("01_transcribe.py")
    
    # Этап 2: Перевод
    run_script("02_translate.py")
    
    # Этап 3: Клонирование голоса
    run_script("03_clone_voice.py")
    
    # Этап 4: Сборка аудио
    run_script("04_postprocess.py")
    
    # Этап 5: Липсинк (опционально, требует доп. настроек)
    # run_script("05_lipsync.py") 
    
    print("\n🎉 Пайплайн завершен!")
    print(f"📁 Результат (аудио): {config.OUTPUTS_DIR / 'dubbed_audio.wav'}")
    print("📝 Для получения видео с липсинком раскомментируйте шаг 5 в main.py и установите Wav2Lip.")

if __name__ == "__main__":
    main()