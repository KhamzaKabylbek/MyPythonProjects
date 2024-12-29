import cv2

input_video = ('car.mp4')


def vid_inf(vid_path):
    cap = cv2.VideoCapture(vid_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = "output_recorded_2.mp4"

    out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    backSub = cv2.createBackgroundSubtractorMOG2()

    if not cap.isOpened():
        print("Error opening video file")
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            fg_mask = backSub.apply(frame)

            retval, mask_thresh = cv2.threshold(fg_mask, 180, 255, cv2.THRESH_BINARY)

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)

            contours, hierarchy = cv2.findContours(mask_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_contour_area = 500
            large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
            frame_out = frame.copy()
            for cnt in large_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                frame_out = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 200), 3)

            out.write(frame_out)

            cv2.imshow("Frame_final", frame_out)

            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


vid_inf(input_video)
