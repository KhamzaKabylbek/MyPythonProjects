# import numpy as np
# import cv2 as cv
# def nothing(x):
#     pass
# # Create a black image, a window
# img = np.zeros((300,512,3), np.uint8)
# cv.namedWindow('image')
# # create trackbars for color change
# cv.createTrackbar('R','image',0,255,nothing)
# cv.createTrackbar('G','image',0,255,nothing)
# cv.createTrackbar('B','image',0,255,nothing)
# # create switch for ON/OFF functionality
# switch = '0 : OFF \n1 : ON'
# cv.createTrackbar(switch, 'image',0,1,nothing)
# while(1):
#     cv.imshow('image',img)
#     k = cv.waitKey(1) & 0xFF
#     if k == 27:
#         break
#     # get current positions of four trackbars
#     r = cv.getTrackbarPos('R','image')
#     g = cv.getTrackbarPos('G','image')
#     b = cv.getTrackbarPos('B','image')
#     s = cv.getTrackbarPos(switch,'image')
#     if s == 0:
#         img[:] = 0
#     else:
#         img[:] = [b,g,r]
# cv.destroyAllWindows()
#
#
#
#
# import tkinter as tk
#
# class DrawingApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Простое окно для рисования")
#
#         self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
#         self.canvas.pack()
#
#         self.canvas.bind("<B1-Motion>", self.paint)
#         self.canvas.bind("<Button-1>", self.set_start_point)
#
#         self.start_x = None
#         self.start_y = None
#
#     def set_start_point(self, event):
#         self.start_x = event.x
#         self.start_y = event.y
#
#     def paint(self, event):
#         if self.start_x is not None and self.start_y is not None:
#             x1, y1 = (self.start_x - 1), (self.start_y - 1)
#             x2, y2 = (event.x + 1), (event.y + 1)
#             self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=2)
#             self.start_x, self.start_y = event.x, event.y
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = DrawingApp(root)
#     root.mainloop()


import numpy as np
import cv2 as cv
import tkinter as tk
from threading import Thread
import threading

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Простое окно для рисования")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.set_start_point)

        self.start_x = None
        self.start_y = None
        self.color = "black"
        self.color_lock = threading.Lock()
        self.lock = threading.Lock()

        # Create OpenCV window with trackbars
        cv.namedWindow('Color Selection')
        cv.createTrackbar('R', 'Color Selection', 0, 255, self.nothing)
        cv.createTrackbar('G', 'Color Selection', 0, 255, self.nothing)
        cv.createTrackbar('B', 'Color Selection', 0, 255, self.nothing)
        cv.createTrackbar('Switch', 'Color Selection', 0, 1, self.nothing)

        # Start a thread for Tkinter event loop
        tk_thread = Thread(target=self.tk_event_loop)
        tk_thread.start()

        # Start a thread for OpenCV event loop
        cv_thread = Thread(target=self.cv_event_loop)
        cv_thread.start()

    def nothing(self, x):
        pass

    def set_start_point(self, event):
        with self.lock:
            self.start_x = event.x
            self.start_y = event.y

    def paint(self, event):
        with self.lock:
            if self.start_x is not None and self.start_y is not None:
                x1, y1 = (self.start_x - 1), (self.start_y - 1)
                x2, y2 = (event.x + 1), (event.y + 1)
                self.canvas.create_line(x1, y1, x2, y2, fill=self.get_color(), width=2)
                self.start_x, self.start_y = event.x, event.y

    def get_color(self):
        r = cv.getTrackbarPos('R', 'Color Selection')
        g = cv.getTrackbarPos('G', 'Color Selection')
        b = cv.getTrackbarPos('B', 'Color Selection')
        s = cv.getTrackbarPos('Switch', 'Color Selection')

        if s == 0:
            return "black"
        else:
            # Convert BGR to RGB format and format as hexadecimal
            return "#{:02X}{:02X}{:02X}".format(b, g, r)

    def tk_event_loop(self):
        while True:
            self.root.update_idletasks()
            self.root.update()

    def cv_event_loop(self):
        while True:
            with self.color_lock:
                self.color = self.get_color()

            with self.lock:
                k = cv.waitKey(1) & 0xFF
                if k == 27:
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
    cv.destroyAllWindows()
