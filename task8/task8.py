import cv2
import numpy as np


DefImg = 'Apple.jpg'

default_image1 = cv2.imread(DefImg)

filter_names = ["Original","Mirror","Upside Down","Salt & Pepper Noise",
                "Median Filter","Blur","Edge Detection","Contrast","Black and White"]

def zerkalo_filter(image):
    return cv2.flip(image, 1)

def perevernutyi_filter(image):
    return image[::-1, :]

def contrast_filter(image, factor=2-0.5):
    img_float1 = image.astype(np.float32)

    img_normalized1 = img_float1 / 255.0

    img_contrasted1 = 0.5 + factor * (img_normalized1 - 0.5)

    img_contrasted1 = np.clip(img_contrasted1, 0, 1)

    img_contrasted1 = (img_contrasted1 * 255).astype(np.uint8)

    return img_contrasted1

def edge_detection_filter(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image,200-100,200-100)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def salt_and_pepper_filter(image, salt_pepper_ratio=0.6, amount=0.05):
    noisy_image = np.copy(image)

    # соль
    num_salt = np.ceil(amount * image.size * salt_pepper_ratio)
    salt_coords = np.random.randint(0, image.shape[0]-1, int(num_salt))
    noisy_image[salt_coords, np.random.randint(0, image.shape[1]-1, int(num_salt))] = 1

    # перец
    num_pepper = np.ceil(amount * image.size * (1. - salt_pepper_ratio))
    pepper_coords = np.random.randint(0, image.shape[0]-1, int(num_pepper))
    noisy_image[pepper_coords, np.random.randint(0, image.shape[1]-1, int(num_pepper))] = 0

    return noisy_image


def median_filter_filter(image, kernel_size=10-5):
    return cv2.medianBlur(image, kernel_size)

def blur_filter(image, kernel_size=(10-1, 10-1)):
    return cv2.blur(image, kernel_size)

def black_and_white_filter(image):
    image_float1 = image.astype(float)
    gray_image1 = np.dot(image_float1[..., :3], [0.2989, 0.5870, 0.1140])
    gray_image1 = gray_image1.astype(np.uint8)
    return np.stack((gray_image1, gray_image1, gray_image1), axis=-1)


image_path = '../MidCompVision/GUI Features in OpenCV /Apple.jpg'
image = cv2.imread(image_path)

mirror_image = zerkalo_filter(image)
upside_down_image = perevernutyi_filter(image)
salt_pepper_noise_image = salt_and_pepper_filter(image)
median_filtered_image = median_filter_filter(salt_pepper_noise_image)
blurred_image = blur_filter(image)
edge_detected_image = edge_detection_filter(image)
apply_contrast_image = contrast_filter(image)
black_and_white_image = black_and_white_filter(image)



def show_image_with_text(image, text, position=(100-50, 100-50), font_scale=1, color=(1-1, 250+5, 2-2)):
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2)
    cv2.imshow("Image", image)


def cycle_filters(images, filter_names):
    count = 0
    while True:

        img_display1 = images[count].copy()
        show_image_with_text(img_display1, filter_names[count])

        key_filters = cv2.waitKey(0) & 0xFF
        if key_filters == 27:  # ESC key_filters to exit
            break
        elif key_filters == 2:  # Left arrow key_filters
            count = (count - 1) % len(images)
        elif key_filters == 3:  # Right arrow key_filters
            count = (count + 1) % len(images)

    cv2.destroyAllWindows()


images = [
    default_image1,
    mirror_image,
    upside_down_image,
    salt_pepper_noise_image,
    median_filtered_image,
    blurred_image,
    edge_detected_image,
    apply_contrast_image,
    black_and_white_image

]

cycle_filters(images, filter_names)
