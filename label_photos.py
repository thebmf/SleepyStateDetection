import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageLabeler:
    def __init__(self, master, image_folder, output_folder):
        self.master = master
        self.image_folder = image_folder
        self.output_folder = output_folder
        self.images = sorted([os.path.join(self.image_folder, img) for img in os.listdir(image_folder)],
                             key=lambda x: (not x.startswith(os.path.join(image_folder, 'awake')), x))
        self.current_image = None
        self.index = 0
        self.total_processed_count = 0
        self.rect = None
        self.start_x = None
        self.start_y = None

        self.canvas = tk.Canvas(master, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.category_progress_label = tk.Label(master, text="0/20 awake photos processed")
        self.category_progress_label.pack(side=tk.TOP, fill=tk.X)
        self.total_progress_label = tk.Label(master, text="0/40 photos processed")
        self.total_progress_label.pack(side=tk.TOP, fill=tk.X)

        top_frame = tk.Frame(master)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        self.clear_button = ctk.CTkButton(top_frame, text="Clear Selection", height=35, fg_color="#008500", hover_color="#007F16", command=self.clear_selection)
        self.clear_button.pack(side=tk.TOP, fill=tk.X, expand=True, pady=(0, 5))

        btn_frame = tk.Frame(master)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.awake_button = ctk.CTkButton(btn_frame, text="Awake", height=40, fg_color="#A60000", hover_color="#A0000F", command=lambda: self.save_label("awake", 10))
        self.awake_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.sleepy_button = ctk.CTkButton(btn_frame, text="Sleepy", height=40, fg_color="#06266F", hover_color="#071D70", command=lambda: self.save_label("sleepy", 11))
        self.sleepy_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.load_image()

    def load_image(self):
        if self.index < len(self.images):
            image_path = self.images[self.index]
            self.current_image = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas.config(width=self.current_image.width, height=self.current_image.height)
        else:
            self.category_progress_label.config(text="No more images to process")
            self.total_progress_label.config(text=f"{self.index}/40 photos processed")

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='red')

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def save_label(self, label, class_id):
        if self.index < len(self.images):
            image_path = self.images[self.index]
            basename = os.path.basename(image_path)
            
            label_filename = f'{basename.replace(".jpg", "")}.txt'
            output_label_path = os.path.join(self.output_folder, label_filename)
            
            self.total_processed_count += 1
            self.update_progress(label)

            if self.rect:
                x1, y1, x2, y2 = self.canvas.coords(self.rect)
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                x_center /= self.current_image.width
                y_center /= self.current_image.height
                width /= self.current_image.width
                height /= self.current_image.height

                with open(output_label_path, 'w') as file:
                    file.write(f'{class_id} {x_center} {y_center} {width} {height}\n')
                
                print(f"Label saved for {label}: {output_label_path}")

            self.index += 1
            self.update_progress(label)

            category_count = sum(1 for img in self.images[:self.index] if label in img)
            if category_count == 20:
                if label == "awake":
                    messagebox.showinfo("Category Complete", "All awake photos processed. Switching to sleepy category.")
                    self.load_next_category("sleepy")
                else:
                    messagebox.showinfo("Completion", "All images processed")
                    self.master.quit()
            else:
                self.load_image()
        else:
            messagebox.showinfo("Completion", "All images processed")
            self.master.quit()
            
    def load_next_category(self, next_category):
        self.index = 0
        self.images = [img for img in self.images if next_category in img]
        self.load_image()

    def update_progress(self, label):
        current_label_count = sum(1 for img in self.images[:self.index] if label in img)
        self.category_progress_label.config(text=f"{current_label_count}/20 {label} photos processed")
        self.total_progress_label.config(text=f"{self.total_processed_count}/40 photos processed")  # Обновление общего прогресса

    def clear_selection(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

def main():
    root = tk.Tk()
    app = ImageLabeler(root, 'data/images', 'data/labels')
    root.mainloop()

if __name__ == "__main__":
    main()