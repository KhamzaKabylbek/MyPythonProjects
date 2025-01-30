import os
import sys
from urllib import request

def download_models():
    # URL для загрузки моделей
    models = {
        "models/MobileNetSSD_deploy.prototxt": "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt",
        "models/MobileNetSSD_deploy.caffemodel": "https://drive.google.com/uc?export=download&id=0B3gersZ2cHIxRm5PMWRoTkdHdHc"
    }
    
    # Создаем директорию models если её нет
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Загружаем каждый файл
    for file_path, url in models.items():
        if not os.path.exists(file_path):
            print(f"Скачивание {file_path}...")
            try:
                request.urlretrieve(url, file_path)
                print(f"Файл {file_path} успешно скачан")
            except Exception as e:
                print(f"Ошибка при скачивании {file_path}: {e}")
                print("Попробуйте скачать файл вручную")
                return False
    return True

if __name__ == "__main__":
    if download_models():
        print("Все модели успешно загружены")
    else:
        print("Произошла ошибка при загрузке моделей")
