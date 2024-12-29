from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont

class PhotoEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Photo Editor App")

        self.image = None
        self.filtered_image = None

        # Widgets
        self.canvas = Canvas(master, width=500, height=500)
        self.canvas.pack()

        self.load_button = Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.filter_button = Button(master, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack()

        self.crop_button = Button(master, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()

        self.add_text_button = Button(master, text="Add Text", command=self.add_text)
        self.add_text_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.show_image(self.image)

    def show_image(self, image):
        # Resize the image to 150x150
        image = image.resize((150, 150))

        # Resize the canvas to match the size of the resized image
        self.canvas.config(width=150, height=150)

        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Draw a border around the image
        border_width = 2
        border_color = 'black'
        self.canvas.create_rectangle(
            border_width, border_width,
            150 + border_width,
            150 + border_width,
            outline=border_color,
            width=border_width
        )

    def apply_filter(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.BLUR)
            self.show_image(self.  filtered_image)

    def crop_image(self):
        if self.image:
            self.image = self.image.crop((100, 100, 400, 400))  # Example cropping
            self.show_image(self.image)

    def add_text(self):
        if self.image:
            draw = ImageDraw.Draw(self.image)
            font = ImageFont.truetype("arial.ttf", 40)
            draw.text((50, 50), "Hello, World!", fill="red", font=font)
            self.show_image(self.image)

root = Tk()
app = PhotoEditorApp(root)
root.mainloop()
