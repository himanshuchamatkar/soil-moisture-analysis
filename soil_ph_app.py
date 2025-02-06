import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np

class SoilPHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Determination of Soil pH")
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Input Image Section
        self.input_image_label = tk.Label(root, text="INPUT IMAGE")
        self.input_image_label.grid(row=0, column=1)

        self.input_image_canvas = tk.Canvas(root, width=300, height=300, bg='white')
        self.input_image_canvas.grid(row=1, column=1)
        self.input_image_canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.input_image_canvas.bind("<B1-Motion>", self.on_move_press)
        self.input_image_canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Cropped Image Section
        self.cropped_image_label = tk.Label(root, text="CROPPED IMAGE")
        self.cropped_image_label.grid(row=2, column=1)

        self.cropped_image_canvas = tk.Canvas(root, width=300, height=300, bg='white')
        self.cropped_image_canvas.grid(row=3, column=1)

        # Buttons
        self.browse_button = tk.Button(root, text="Browse Test Image", command=self.load_image)
        self.browse_button.grid(row=1, column=0)

        self.crop_button = tk.Button(root, text="Crop Image", command=self.crop_image)
        self.crop_button.grid(row=3, column=0)

        self.ph_label = tk.Label(root, text="FINAL OUTPUT (Ph)")
        self.ph_label.grid(row=4, column=0)

        self.ph_value = tk.Entry(root)
        self.ph_value.grid(row=4, column=1)

        self.rgb_label = tk.Label(root, text="RGB INDEX VALUES")
        self.rgb_label.grid(row=5, column=0)

        self.rgb_value = tk.Entry(root)
        self.rgb_value.grid(row=5, column=1)

        self.find_crops_button = tk.Button(root, text="Find Suitable Crops", command=self.find_crops)
        self.find_crops_button.grid(row=6, column=1)

        # Variables
        self.image = None
        self.cropped_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image, self.input_image_canvas)

    def display_image(self, image, canvas):
        image.thumbnail((300, 300))
        self.tk_image = ImageTk.PhotoImage(image)
        canvas.create_image(150, 150, image=self.tk_image)
        canvas.image = self.tk_image

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.input_image_canvas.delete(self.rect)
        self.rect = self.input_image_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.input_image_canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        pass

    def crop_image(self):
        if self.image:
            x1, y1, x2, y2 = self.input_image_canvas.coords(self.rect)
            x1 = int(x1 * self.image.width / 300)
            y1 = int(y1 * self.image.height / 300)
            x2 = int(x2 * self.image.width / 300)
            y2 = int(y2 * self.image.height / 300)

            self.cropped_image = self.image.crop((x1, y1, x2, y2))
            self.display_image(self.cropped_image, self.cropped_image_canvas)
            self.calculate_ph_moisture(self.cropped_image)

    def calculate_ph_moisture(self, image):
        if image:
            image_array = np.array(image)
            r_mean = np.mean(image_array[:, :, 0])
            g_mean = np.mean(image_array[:, :, 1])
            b_mean = np.mean(image_array[:, :, 2])
            ph_value = 7 + (r_mean - g_mean) / 100
            self.ph_value.delete(0, tk.END)
            self.ph_value.insert(0, f"{ph_value:.2f}")
            self.rgb_value.delete(0, tk.END)
            self.rgb_value.insert(0, f"R: {r_mean:.2f}, G: {g_mean:.2f}, B: {b_mean:.2f}")
            moisture_value = (r_mean + g_mean + b_mean) / 3
            messagebox.showinfo("Moisture Value", f"Estimated Soil Moisture: {moisture_value:.2f}")

    def find_crops(self):
        ph = float(self.ph_value.get())
        crops = "Example crop list based on pH"
        messagebox.showinfo("Suitable Crops", crops)

if __name__ == "__main__":
    root = tk.Tk()
    app = SoilPHApp(root)
    root.mainloop()
