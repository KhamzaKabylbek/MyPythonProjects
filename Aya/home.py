#import pyaudio
import numpy as np

def detect_sound():
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)
    
    data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
    amplitude = np.max(np.abs(data))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return amplitude

def smart_home():
    threshold = 0.1  # порог для определения хлопка
    print("Слушаю хлопки... (Для выхода нажмите Ctrl+C)")
    
    while True:
        try:
            amplitude = detect_sound()
            if amplitude > threshold:
                print("off")
            else:
                print("on")
                
        except KeyboardInterrupt:
            print("\nПрограмма завершена")
            break

if __name__ == "__main__":
    print("Система умного дома запущена")
    print("Проверка микрофона...")
    smart_home()
