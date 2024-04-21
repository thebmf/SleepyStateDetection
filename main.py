import tkinter as tk
from PIL import Image, ImageTk
import cv2
import torch
import time
import pygame

class Application:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/weights/last.pt', force_reload=True)
        self.cap = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_quit = tk.Button(window, text="Quit", width=10, command=self.window.destroy)
        self.btn_quit.pack(pady=20)

        self.sleepy_probability = 0
        self.awake_probability = 0
        self.is_playing_sleepy_audio = False
        
        pygame.mixer.init()
        self.sleepy_audio = pygame.mixer.Sound('clock-alarm.mp3')

        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(frame)
            print(results)

            df = results.pandas().xyxy[0]
            sleepy_probability = df[df["name"] == "sleepy"]["confidence"].sum()
            awake_probability = df[df["name"] == "awake"]["confidence"].sum()

            self.sleepy_probability = sleepy_probability
            self.awake_probability = awake_probability

            if self.sleepy_probability > self.awake_probability and not self.is_playing_sleepy_audio:
                self.play_sleepy_audio()
                self.is_playing_sleepy_audio = True

            if self.sleepy_probability <= self.awake_probability and self.is_playing_sleepy_audio:
                self.stop_sleepy_audio()
                self.is_playing_sleepy_audio = False

            frame = results.render()[0]
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)


    def play_sleepy_audio(self):
        self.sleepy_audio.play()

    def stop_sleepy_audio(self):
        self.sleepy_audio.stop()

root = tk.Tk()
app = Application(root, "YOLOv5 Object Detection")