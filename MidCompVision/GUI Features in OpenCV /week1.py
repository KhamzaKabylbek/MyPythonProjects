import cv2

# Загрузка изображения с диска
image = cv2.imread('Apple.jpg')

if image is None:
    print("Не удалось загрузить изображение.")
else:
    # Отображение изображения
    cv2.imshow('Исходное изображение', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Сохранение изображения (если нужно)
    cv2.imwrite('новый_файл.jpg', image)
