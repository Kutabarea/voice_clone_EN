import subprocess
import config
import os

def run_lipsync(video_path, audio_path, output_path):
    """Запускает Wav2Lip для синхронизации губ."""
    print("👄 Запуск синхронизации губ (Wav2Lip)...")
    
    # Проверка наличия модели
    if not os.path.exists(config.LIPSYNC_MODEL_PATH):
        print(f"❌ Модель Wav2Lip не найдена: {config.LIPSYNC_MODEL_PATH}")
        print("💡 Скачайте wav2lip_gan.pth и положите в папку checkpoints/")
        print("🔗 Ссылка: https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EbN1OaZLzDxMjU9M051F_q4B856Q4kX9vZ8J7z8J7z8J7w?e=4r9g8t")
        return False

    # Команда для запуска inference.py из репозитория Wav2Lip
    # Предполагается, что репозиторий Wav2Lip клонирован рядом или путь настроен
    # Это упрощенный вызов, в реальности может потребоваться активация специфичного окружения для Wav2Lip
    
    command = [
        "python", "inference.py",
        "--checkpoint_path", config.LIPSYNC_MODEL_PATH,
        "--face", str(video_path),
        "--audio", str(audio_path),
        "--outfile", str(output_path),
        "--pads", "0", "10", "0", "0", # Подстройка области рта
        "--face_det_batch_size", "16"
    ]
    
    try:
        # Примечание: inference.py должен быть доступен в PYTHONPATH или текущей директории
        # В реальном проекте лучше подключить Wav2Lip как подмодуль
        subprocess.run(command, check=True)
        print(f"✅ Липсинк готов: {output_path}")
        return True
    except FileNotFoundError:
        print("❌ Файл inference.py не найден. Убедитесь, что клонировали репозиторий Wav2Lip.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении Wav2Lip: {e}")
        return False

if __name__ == "__main__":
    # Этот шаг требует наличия установленного репозитория Wav2Lip
    # Для простоты здесь заглушка логики
    print("⚠️ Шаг липсинка требует отдельной установки Wav2Lip.")
    print("📝 Инструкции по установке добавлены в README.")
    
    # Если бы все было установлено:
    # run_lipsync(config.INPUT_VIDEO_PATH, config.OUTPUTS_DIR / "dubbed_audio.wav", config.OUTPUTS_DIR / config.FINAL_OUTPUT_NAME