import numpy as np
import cv2 as cv


def add_damage_to_image(img, num_circles=5, radius=20):
    damaged_img = img.copy()
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    h, w = img.shape[:2]

    for _ in range(num_circles):
        center = (np.random.randint(radius, w - radius), np.random.randint(radius, h - radius))
        cv.circle(damaged_img, center, radius, (0, 0, 0), -1)
        cv.circle(mask, center, radius, 255, -1)

    return damaged_img, mask


def inpaint_image(original_img, damaged_img, mask):
    inpainted_img = cv.inpaint(damaged_img, mask, 3, cv.INPAINT_TELEA)
    return inpainted_img


def save_images(original, damaged, repaired, path_prefix):
    cv.imwrite(f'{path_prefix}_original.jpg', original)
    cv.imwrite(f'{path_prefix}_damaged.jpg', damaged)
    cv.imwrite(f'{path_prefix}_repaired.jpg', repaired)


if __name__ == '__main__':
    img = cv.imread('images.jpeg')
    if img is None:
        raise ValueError("Image not found or the format is unsupported")

    damaged_img, mask = add_damage_to_image(img)

    repaired_img = inpaint_image(img, damaged_img, mask)

    cv.imshow('Original Image', img)
    cv.imshow('Damaged Image', damaged_img)
    cv.imshow('Repaired Image', repaired_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    save_images(img, damaged_img, repaired_img, 'inpaint_test')


