import cv2
import os
import glob
import time

def create_slideshow(image_folder, output_path, transition_duration=1.0):
    image_files = sorted(glob.glob(os.path.join(image_folder, '*.jpg')))


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    frame_width = cv2.imread(image_files[0]).shape[1]
    frame_height = cv2.imread(image_files[0]).shape[0]
    video_writer = cv2.VideoWriter(os.path.join(output_path, 'slideshow.avi'), cv2.VideoWriter_fourcc(*'XVID'), 1, (frame_width, frame_height))

    for i in range(len(image_files) - 1):
        img1 = cv2.imread(image_files[i])
        img2 = cv2.imread(image_files[i + 1])

        img1 = cv2.resize(img1, (frame_width, frame_height))
        img2 = cv2.resize(img2, (frame_width, frame_height))

        alpha = 1.0
        start_time = time.time()

        while alpha > 0:
            blended_frame = cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)

            cv2.imshow('Slideshow', blended_frame)
            cv2.waitKey(1)

            elapsed_time = time.time() - start_time
            alpha = max(0, 1 - elapsed_time / transition_duration)

            time.sleep(0.02)

        video_writer.write(blended_frame)

    video_writer.release()
    cv2.destroyAllWindows()

image_folder = 'images'
output_path = '../slideshow'
create_slideshow(image_folder, output_path, transition_duration=1.0)
