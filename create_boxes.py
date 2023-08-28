# Artur Dwornik
# MIT License

# Easy to use GUI to create bounding boxes for object detection
# Usage: python create_boxes.py
# Controls:
#   - Left click and drag to create a bounding box
#   - Press 'D' to go to the next image
#   - Press 'A' to go to the previous image
#   - Press 'Backspace' to delete the last bounding box

# The bounding boxes are saved in a text file with the same name as the image
# Bounding box format: left_x top_y right_x bottom_y

import tkinter as tk
import os
from tkinter import filedialog
from PIL import Image, ImageTk

class CreateBoudningBoxes:
    def __init__(self, root):
        self.root = root
        self.button_frame = tk.Frame(self.root)
        self.root.title("Easy Bounding Boxes")
        self.directory_label = tk.Label(
            root, text="No directory selected", padx=10, pady=10
        )

        self.select_button = tk.Button(
            root, text="Select Directory", command=self.select_directory
        )

        self.canvas = tk.Canvas(self.root)

        self.next_button = tk.Button(
            self.button_frame, text="Next Image (D)", command=self.next_image
        )

        self.previous_button = tk.Button(
            self.button_frame, text="Previous Image (A)", command=self.previous_image
        )

        self.delete_button = tk.Button(
            self.button_frame, text="Delete Last Box", command=self.delete_last_box
        )

        self.bounding_boxes = []
        self.current_image = None
        self.current_image_path = None

        self.directory_label.pack()
        self.select_button.pack()
        self.canvas.pack()
        self.button_frame.pack(pady=10)
        self.previous_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.RIGHT)
        self.delete_button.pack()  

        self.canvas.bind("<ButtonPress-1>", self.start_box)
        self.canvas.bind("<B1-Motion>", self.draw_box)
        self.canvas.bind("<ButtonRelease-1>", self.end_box)
        self.root.bind("a", lambda event: self.previous_image())
        self.root.bind("d", lambda event: self.next_image())
        self.root.bind("<BackSpace>", lambda event: self.delete_last_box())

    def next_image(self):
        if self.current_image_path:
            current_dir = os.path.dirname(self.current_image_path)
            files = os.listdir(current_dir)
            current_index = files.index(os.path.basename(self.current_image_path))
            while current_index < len(files) - 1:
                if files[current_index + 1].endswith(
                    (".jpg", ".png", ".jpeg", ".JPG", ".PNG", ".JPEG")
                ):
                    self.load_image(os.path.join(current_dir, files[current_index + 1]))
                    break
                else:
                    current_index += 1

    def delete_last_box(self):
        if self.bounding_boxes:
            removed_box = self.bounding_boxes.pop()
            with open(self.current_image_path + ".txt", "r") as f:
                lines = f.readlines()
            with open(self.current_image_path + ".txt", "w") as f:
                f.writelines(lines[:-1])
            self.canvas.delete(removed_box)
            # Reload the image to remove the box
            self.load_image(
                self.current_image_path
            )  

    def previous_image(self):
        if self.current_image_path:
            current_dir = os.path.dirname(self.current_image_path)
            files = os.listdir(current_dir)
            current_index = files.index(os.path.basename(self.current_image_path))
            while current_index > 0:
                if files[current_index - 1].endswith(
                    (".jpg", ".png", ".jpeg", ".JPG", ".PNG", ".JPEG")
                ):
                    self.load_image(os.path.join(current_dir, files[current_index - 1]))
                    break
                else:
                    current_index -= 1

    def select_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.directory_label.config(text=f"Selected Directory: {selected_dir}")
            self.load_images(selected_dir)
        else:
            self.directory_label.config(text="No directory selected")

    def load_images(self, selected_dir):
        files = os.listdir(selected_dir)
        for file in files:
            if file.endswith(".jpg"):
                self.load_image(os.path.join(selected_dir, file))
                break

    def load_image(self, file_path):
        self.current_image_path = file_path
        pil_image = Image.open(file_path)
        self.canvas.config(width=pil_image.width, height=pil_image.height)
        self.current_image = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, image=self.current_image, anchor=tk.NW)
        self.bounding_boxes = []
        if os.path.exists(file_path + ".txt"):
            with open(file_path + ".txt", "r") as f:
                for line in f.readlines():
                    box = tuple(map(int, line.split()))
                    self.bounding_boxes.append(box)
                    self.canvas.create_rectangle(box, outline="red")

    def start_box(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_box = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red"
        )

    def draw_box(self, event):
        self.canvas.coords(
            self.current_box, self.start_x, self.start_y, event.x, event.y
        )

    def end_box(self, event):
        self.bounding_boxes.append((self.start_x, self.start_y, event.x, event.y))
        self.save_box()

    def save_box(self):
        if self.current_image_path and self.bounding_boxes:
            with open(self.current_image_path + ".txt", "w") as f:
                for box in self.bounding_boxes:
                    f.write(" ".join(map(str, box)) + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = CreateBoudningBoxes(root)
    root.mainloop()
