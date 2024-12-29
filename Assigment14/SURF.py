import cv2

# Загрузка изображения
image_path = 'IMG_9566-720x404.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Инициализация детектора SURF
surf = cv2.xfeatures2d.SURF_create()

# Обнаружение ключевых точек и вычисление их дескрипторов
keypoints, descriptors = surf.detectAndCompute(image, None)

# Рисование ключевых точек на изображении
image_with_keypoints = cv2.drawKeypoints(image, keypoints, None, (255, 0, 0), 4)

# Вывод изображения с ключевыми точками
cv2.imshow('SURF Keypoints', image_with_keypoints)
cv2.waitKey(1)
cv2.destroyAllWindows()
