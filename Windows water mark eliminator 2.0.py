import tkinter as tk
from tkinter import ttk
from assistant import launch_assistant

def main():
    root = tk.Tk()
    root.title("Gestor de Marcas de Agua Windows")
    root.geometry("400x240")
    root.configure(bg="#222C3C")
    ttk.Label(root, text="Gestor de Marcas de Agua Windows", font=("Segoe UI", 18, "bold")).pack(pady=14)
    ttk.Label(root, text="Creada por NiCaso14", font=("Segoe UI", 11, "italic")).pack(pady=4)
    ttk.Button(root, text="Abrir asistente virtual", command=lambda: launch_assistant(root, "¡Hola! ¿En qué puedo ayudarte hoy?")).pack(pady=30)
    root.mainloop()

if __name__ == "__main__":
    main()
