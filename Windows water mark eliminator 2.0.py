import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

CACHE_DIR = "cache"
APP_NAME = "Gestor de Marcas de Agua Windows"
AUTHOR = "Creada por NiCaso14"

# Crear carpeta cache
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Inicializar archivos y scripts
files_and_contents = {
    "historial.txt": "",
    "recuperacion.txt": "",
    "eliminar_activar_windows.bat": "taskkill /f /im explorer.exe\nstart explorer.exe\n",
    "restaurar_activar_windows.bat": "taskkill /f /im explorer.exe\nstart explorer.exe\n",
    "eliminar_modo_prueba.bat": "bcdedit -set TESTSIGNING OFF\n",
    "restaurar_modo_prueba.bat": "bcdedit -set TESTSIGNING ON\n",
    "eliminar_insider_preview.bat": 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableInsiderPreviewWatermark /t REG_DWORD /d 1 /f\n',
    "restaurar_insider_preview.bat": 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableInsiderPreviewWatermark /t REG_DWORD /d 0 /f\n',
    "detectar_marca_agua.bat": """@echo off
setlocal
set resultado=
slmgr /xpr | findstr /i "not activated" >nul && set resultado=Activar Windows
bcdedit | findstr /i "testsigning yes" >nul && set resultado=%resultado% Modo de prueba
reg query "HKLM\\SOFTWARE\\Microsoft\\WindowsSelfHost\\UI" /v UIContent | findstr /i "insider" >nul && set resultado=%resultado% Insider Preview
if "%resultado%"=="" (echo No se detectó ninguna marca de agua común. > resultado.txt) else (echo Detectado: %resultado% > resultado.txt)
endlocal
"""
}
for fname, content in files_and_contents.items():
    fpath = os.path.join(CACHE_DIR, fname)
    if not os.path.exists(fpath):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

# Estado de anuncios
show_ads = True

def ejecutar_bat(nombre):
    path = os.path.join(CACHE_DIR, nombre)
    return subprocess.call(['cmd', '/c', path], shell=True)

def procesar_accion(accion, marca):
    from datetime import datetime
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = ""
    if accion == "Eliminar marca de agua":
        if marca == "Activar Windows":
            ejecutar_bat("eliminar_activar_windows.bat")
            resultado = "Intento de ocultar 'Activar Windows' realizado."
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a", encoding="utf-8") as f:
                f.write(f"{fecha} - Eliminado: Activar Windows\n")
            with open(os.path.join(CACHE_DIR, "recuperacion.txt"), "a", encoding="utf-8") as f:
                f.write(f"{fecha} - Para recuperar: Ejecutar restaurar_activar_windows.bat\n")
        elif marca == "Modo de prueba":
            ejecutar_bat("eliminar_modo_prueba.bat")
            resultado = "Modo de prueba desactivado."
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a", encoding="utf-8") as f:
                f.write(f"{fecha} - Eliminado: Modo de prueba\n")
            with open(os.path.join(CACHE_DIR, "recuperacion.txt"), "a", encoding="utf-8") as f:
                f.write(f"{fecha} - Para recuperar: Ejecutar restaurar_modo_prueba.bat\n")
        elif marca == "Insider Preview":
            ejecutar_bat("eliminar_insider_preview.bat")
            resultado = "Insider Preview desactivado."
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a", encoding="utf-8") as f:
                f.write(f"{fecha} - Eliminado: Insider Preview\n")
            with open(os.path.join(CACHE_DIR, "recuperacion.txt"), "a", encoding="utf-8") as f:
                f.write(f"{fecha} - Para recuperar: Ejecutar restaurar_insider_preview.bat\n")
    elif accion == "Restaurar marca de agua":
        if marca == "Activar Windows":
            ejecutar_bat("restaurar_activar_windows.bat")
            resultado = "'Activar Windows' restaurado."
        elif marca == "Modo de prueba":
            ejecutar_bat("restaurar_modo_prueba.bat")
            resultado = "'Modo de prueba' restaurado."
        elif marca == "Insider Preview":
            ejecutar_bat("restaurar_insider_preview.bat")
            resultado = "'Insider Preview' restaurado."
    elif accion == "Detectar automáticamente":
        ejecutar_bat("detectar_marca_agua.bat")
        resultado_path = os.path.join(CACHE_DIR, "resultado.txt")
        if os.path.exists(resultado_path):
            with open(resultado_path, "r", encoding="utf-8") as f:
                resultado = f.read()
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a", encoding="utf-8") as fhist:
                fhist.write(f"{fecha} - Detección automática: {resultado}\n")
    else:
        resultado = "Para otras marcas, consulta documentación técnica."
    resultado_var.set(resultado)

def quitar_anuncios():
    global show_ads
    show_ads = False
    ads_frame.pack_forget()
    messagebox.showinfo("Gracias", "Has quitado los anuncios. ¡Gracias por tu apoyo!")

root = tk.Tk()
root.title(APP_NAME)
root.geometry("560x410")
root.resizable(False, False)
root.configure(bg="#222C3C")

# Título
title_label = tk.Label(root, text=APP_NAME, font=("Segoe UI", 24, "bold"), fg="#3D91C9", bg="#222C3C")
title_label.pack(pady=(18, 5))

author_label = tk.Label(root, text=AUTHOR, font=("Segoe UI", 12, "italic"), fg="#B3C2D6", bg="#222C3C")
author_label.pack(pady=(0, 16))

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)

# Interfaz avanzada
style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#f4f7fc")
style.configure("TLabel", background="#f4f7fc", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TCombobox", font=("Segoe UI", 10))

ttk.Label(main_frame, text="Selecciona la acción:").grid(row=0, column=0, sticky="e", padx=6, pady=8)
accion_var = tk.StringVar()
accion_combobox = ttk.Combobox(main_frame, textvariable=accion_var, state="readonly", width=23)
accion_combobox["values"] = ("Eliminar marca de agua", "Restaurar marca de agua", "Detectar automáticamente", "Otra")
accion_combobox.current(0)
accion_combobox.grid(row=0, column=1, sticky="w", padx=6)

ttk.Label(main_frame, text="Selecciona la marca de agua:").grid(row=1, column=0, sticky="e", padx=6, pady=8)
marca_var = tk.StringVar()
marca_combobox = ttk.Combobox(main_frame, textvariable=marca_var, state="readonly", width=23)
marca_combobox["values"] = ("Activar Windows", "Modo de prueba", "Insider Preview")
marca_combobox.current(0)
marca_combobox.grid(row=1, column=1, sticky="w", padx=6)

resultado_var = tk.StringVar()
resultado_label = ttk.Label(main_frame, textvariable=resultado_var, foreground="#266f26", font=("Segoe UI", 11, "bold"))
resultado_label.grid(row=3, column=0, columnspan=2, pady=(18, 0))

ejecutar_btn = ttk.Button(main_frame, text="Ejecutar", command=lambda: procesar_accion(accion_var.get(), marca_var.get()))
ejecutar_btn.grid(row=2, column=0, columnspan=2, pady=(14, 0))

# Anuncios (simulados)
ads_frame = tk.Frame(root, bg="#FDF3DE", height=60)
ads_text = tk.Label(ads_frame, text="Anuncio: ¡Consigue Windows totalmente activado en nuestro sitio! 😄\nQuita los anuncios pagando.", font=("Segoe UI", 10), bg="#FDF3DE", fg="#6B4F1D")
ads_text.pack(side="left", padx=18, pady=7)
ads_btn = tk.Button(ads_frame, text="Quitar anuncios", command=quitar_anuncios, bg="#F6E7C1", fg="#6B4F1D", font=("Segoe UI", 10, "bold"))
ads_btn.pack(side="right", padx=18)
if show_ads:
    ads_frame.pack(fill="x", side="bottom", pady=(0, 0))

root.mainloop()
