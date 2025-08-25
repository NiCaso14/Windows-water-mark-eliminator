import os
import tkinter as tk
from tkinter import Toplevel, Canvas, NW
from PIL import Image, ImageTk
import pyttsx3
import threading
import time

ASSISTANT_CACHE = os.path.join("cache", "assistant")
ASSETS_DIR = "assets"

# Crear cache si no existe
if not os.path.exists(ASSISTANT_CACHE):
    os.makedirs(ASSISTANT_CACHE)

class AssistantWindow:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Asistente Virtual")
        self.window.geometry("320x340")
        self.window.resizable(False, False)
        self.window.configure(bg="#e6eaf3")
        self.canvas = Canvas(self.window, width=320, height=280, bg="#e6eaf3", highlightthickness=0)
        self.canvas.pack()
        # Cargar imágenes (personaje principal, parpadeo, boca abierta/cerrada)
        self.img_body = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, "body.png"))) # cuerpo sin boca
        self.img_eye_closed = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, "eye_closed.png"))) # parpadeo
        self.img_mouth_open = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, "mouth_open.png")))
        self.img_mouth_closed = ImageTk.PhotoImage(Image.open(os.path.join(ASSETS_DIR, "mouth_closed.png")))
        # Bocadillo
        self.bubble = self.canvas.create_rectangle(60, 10, 260, 60, fill="#fff", outline="#3D91C9", width=2)
        self.bubble_text = self.canvas.create_text(70, 20, anchor=NW, text="", font=("Segoe UI", 10), fill="#3D91C9")
        self.canvas.itemconfig(self.bubble, state='hidden')
        self.canvas.itemconfig(self.bubble_text, state='hidden')
        # Inicialmente dibujar personaje con boca cerrada y ojos abiertos
        self.body_id = self.canvas.create_image(80, 60, anchor=NW, image=self.img_body)
        self.mouth_id = self.canvas.create_image(150, 170, anchor=NW, image=self.img_mouth_closed)
        self.eyes_id = None
        self.animating = True
        self.parpadeo()
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def parpadeo(self):
        # Parpadea cada 3-6 segundos
        def blink():
            while self.animating:
                time.sleep(3)
                self.canvas.delete(self.eyes_id) if self.eyes_id else None
                self.eyes_id = self.canvas.create_image(135, 140, anchor=NW, image=self.img_eye_closed)
                time.sleep(0.18)
                self.canvas.delete(self.eyes_id)
                self.eyes_id = None
        threading.Thread(target=blink, daemon=True).start()

    def hablar(self, texto):
        # Mostrar bocadillo con texto
        self.canvas.itemconfig(self.bubble, state='normal')
        self.canvas.itemconfig(self.bubble_text, state='normal')
        self.canvas.itemconfig(self.bubble_text, text=texto)
        # Animar boca (mueve labios mientras habla)
        def anim_boca():
            for _ in range(len(texto)*2):
                self.canvas.itemconfig(self.mouth_id, image=self.img_mouth_open)
                time.sleep(0.18)
                self.canvas.itemconfig(self.mouth_id, image=self.img_mouth_closed)
                time.sleep(0.18)
            # Ocultar bocadillo después de hablar
            self.canvas.itemconfig(self.bubble, state='hidden')
            self.canvas.itemconfig(self.bubble_text, state='hidden')

        threading.Thread(target=anim_boca, daemon=True).start()

        # Decir el texto (voz)
        def voz():
            engine = pyttsx3.init()
            engine.say(texto)
            engine.runAndWait()
        threading.Thread(target=voz, daemon=True).start()

    def close(self):
        self.animating = False
        self.window.destroy()

def launch_assistant(master, texto):
    aw = AssistantWindow(master)
    aw.hablar(texto)
