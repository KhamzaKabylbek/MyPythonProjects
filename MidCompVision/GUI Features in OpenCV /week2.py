# import cv2
# import numpy as np
#
# # Создаем изображение
# image = np.zeros((500, 500, 3), dtype=np.uint8)
#
# # Рисуем линию (цвет в формате BGR)
# cv2.line(image, (100, 100), (400, 400), (0, 255, 0), 2)
#
# # Отображаем изображение
# cv2.imshow('Line', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
##########################################################################
# import cv2
# import numpy as np
#
# # Создаем изображение
# image = np.zeros((500, 500, 3), dtype=np.uint8)
#
# # Рисуем прямоугольник (цвет в формате BGR)
# cv2.rectangle(image, (100, 100), (400, 300), (0, 255, 0), 2)
#
# # Отображаем изображение
# cv2.imshow('Rectangle', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

##########################################################################

# import cv2
# import numpy as np
#
# # Создаем изображение
# image = np.zeros((500, 500, 3), dtype=np.uint8)
#
# # Рисуем эллипс (цвет в формате BGR)
# cv2.ellipse(image, (250, 250), (150, 100), 30, 0, 180, (0, 255, 0), 2)
#
# # Отображаем изображение
# cv2.imshow('Ellipse', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

##########################################################################

# import cv2
# import numpy as np
#
# # Создаем изображение
# image = np.zeros((500, 500, 3), dtype=np.uint8)
#
# # Задаем координаты вершин многоугольника
# points = np.array([[100, 100], [200, 300], [400, 200], [300, 100]], np.int32)
# points = points.reshape((-1, 1, 2))
#
# # Рисуем многоугольник (цвет в формате BGR)
# cv2.polylines(image, [points], True, (0, 255, 0), 2)
#
# # Отображаем изображение
# cv2.imshow('Polygon', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


