import cv2 as cv
import numpy as np

SZ = 20
bin_n = 16

affine_flags = cv.WARP_INVERSE_MAP | cv.INTER_LINEAR


def deskew(img):
    m = cv.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11'] / m['mu02']
    M = np.float32([[1, skew, -0.5 * SZ * skew], [0, 1, 0]])
    img = cv.warpAffine(img, M, (SZ, SZ), flags=affine_flags)
    return img


def hog(img):
    gx = cv.Sobel(img, cv.CV_32F, 1, 0)
    gy = cv.Sobel(img, cv.CV_32F, 0, 1)
    mag, ang = cv.cartToPolar(gx, gy)
    bins = np.int32(bin_n * ang / (2 * np.pi))
    bin_cells = bins[:10, :10], bins[10:, :10], bins[:10, 10:], bins[10:, 10:]
    mag_cells = mag[:10, :10], mag[10:, :10], mag[:10, 10:], mag[10:, 10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)
    return hist


def preprocess_image(img):
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

    kernel = np.ones((2, 2), np.uint8)
    img = cv.erode(img, kernel, iterations=1)
    img = cv.dilate(img, kernel, iterations=1)

    return img


def pixels_to_hog_20(pixel_array):
    hog_featuresData = []
    for img in pixel_array:
        img = preprocess_image(img)

        fd = hog(img, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
        hog_featuresData.append(fd)
    hog_features = np.array(hog_featuresData, 'float64')
    return np.float32(hog_features)


def classify_digit(your_digit_img):
    deskewed_img = deskew(your_digit_img)
    hog_features = hog(deskewed_img)
    testData = np.float32(hog_features).reshape(-1, bin_n * 4)

    svm = cv.ml.SVM_load('svm_data.dat')

    result = svm.predict(testData)[1]

    return int(result[0][0])


if __name__ == '__main__':
    your_digit_img = cv.imread('2_2.png', 0)

    prediction = classify_digit(your_digit_img)

    print("result", prediction)
