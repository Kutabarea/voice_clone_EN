from faster_whisper import WhisperModel
import json

# Параметры
VIDEO_PATH = "input_video.mp4"  # Замените на путь к вашему видео
MODEL_SIZE = "large-v3"         # Лучшее качество для русского языка
DEVICE = "cuda"                 # Используйте 'cpu', если нет GPU (будет медленно)

def transcribe_audio(video_path):
    print(f"Загрузка модели Whisper ({MODEL_SIZE})...")
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="float16")

    print(f"Транскрибация аудио из {video_path}...")
    # Извлекаем аудио автоматически через ffmpeg внутри whisper или предварительно
    # faster-whisper принимает путь к видео напрямую
    segments, info = model.transcribe(video_path, language="ru", vad_filter=True)

    result = []
    for segment in segments:
        result.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

    # Сохраняем результат в JSON для следующего шага
    with open("transcription_ru.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("Транскрибация завершена. Результат сохранен в transcription_ru.json")

if __name__ == "__main__":
    # Убедитесь, что файл input_video.mp4 существует в папке запуска
    if not os.path.exists(VIDEO_PATH):
        # Создадим заглушку для теста, если файла нет (удалите этот блок в реальном использовании)
        print(f"Ошибка: Файл {VIDEO_PATH} не найден.")
    else:
        transcribe_audio(VIDEO_PATH)