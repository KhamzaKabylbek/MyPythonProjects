import cv2
import gradio as gr
import numpy as np



def vid_inf(vid_path):
    cap = cv2.VideoCapture(vid_path)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = "output_recorded.mp4"

    out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    backSub = cv2.createBackgroundSubtractorMOG2()

    if not cap.isOpened():
        print("Error opening video file")
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            fg_mask = backSub.apply(frame)
            retval, mask_thresh = cv2.threshold(
                fg_mask, 180, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            mask_eroded = cv2.morphologyEx(mask_thresh, cv2.MORPH_OPEN, kernel)
            contours, hierarchy = cv2.findContours(
                mask_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_contour_area = 2000
            large_contours = [
                cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
            frame_out = frame.copy()
            for cnt in large_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                frame_out = cv2.rectangle(
                    frame, (x, y), (x+w, y+h), (0, 0, 200), 3)
            frame_out_display = cv2.cvtColor(frame_out, cv2.COLOR_BGR2RGB)
            vid = out.write(frame_out)

            if not count % 12:
                yield frame_out_display, None
            count += 1

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    yield None, output_video



input_video = gr.Video(label="Input Video")
output_frames = gr.Image(label="Output Frames")
output_video_file = gr.Video(label="Output video")

app = gr.Interface(
    fn=vid_inf,
    inputs=[input_video],
    outputs=[output_frames, output_video_file],
    title=f"MotionScope",
    description=f'A gradio app for dynamic video analysis tool that leverages advanced background subtraction and contour detection techniques to identify and track moving objects in real-time.',
    allow_flagging="never",
    examples=[["sample/car.mp4"]],
)
app.queue().launch()