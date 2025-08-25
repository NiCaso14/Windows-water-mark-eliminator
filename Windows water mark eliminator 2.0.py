import os
import subprocess
from tkinter import Tk, Label, Button, StringVar, OptionMenu

# Crear carpeta cache
CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Inicializar archivos
for fname in [
    "historial.txt", "recuperacion.txt",
    "eliminar_activar_windows.bat", "restaurar_activar_windows.bat",
    "eliminar_modo_prueba.bat", "restaurar_modo_prueba.bat",
    "eliminar_insider_preview.bat", "restaurar_insider_preview.bat",
    "detectar_marca_agua.bat"
]:
    fpath = os.path.join(CACHE_DIR, fname)
    if not os.path.exists(fpath):
        with open(fpath, "w") as f:
            if "eliminar_activar_windows" in fname or "restaurar_activar_windows" in fname:
                f.write("taskkill /f /im explorer.exe\nstart explorer.exe\n")
            elif "eliminar_modo_prueba" in fname:
                f.write("bcdedit -set TESTSIGNING OFF\n")
            elif "restaurar_modo_prueba" in fname:
                f.write("bcdedit -set TESTSIGNING ON\n")
            elif "eliminar_insider_preview" in fname:
                f.write('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableInsiderPreviewWatermark /t REG_DWORD /d 1 /f\n')
            elif "restaurar_insider_preview" in fname:
                f.write('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableInsiderPreviewWatermark /t REG_DWORD /d 0 /f\n')
            elif "detectar_marca_agua.bat" in fname:
                f.write("""@echo off
setlocal
set resultado=
slmgr /xpr | findstr /i "not activated" >nul && set resultado=Activar Windows
bcdedit | findstr /i "testsigning yes" >nul && set resultado=%resultado% Modo de prueba
reg query "HKLM\\SOFTWARE\\Microsoft\\WindowsSelfHost\\UI" /v UIContent | findstr /i "insider" >nul && set resultado=%resultado% Insider Preview
if "%resultado%"=="" (echo No se detectó ninguna marca de agua común. > resultado.txt) else (echo Detectado: %resultado% > resultado.txt)
endlocal
""")

def ejecutar_bat(nombre):
    path = os.path.join(CACHE_DIR, nombre)
    return subprocess.call(['cmd', '/c', path])

def procesar_accion(accion, marca):
    fecha = subprocess.getoutput("echo %DATE% %TIME%")
    resultado = ""
    if accion == "Eliminar marca de agua":
        if marca == "Activar Windows":
            ejecutar_bat("eliminar_activar_windows.bat")
            resultado = "Intento de ocultar 'Activar Windows' realizado."
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a") as f:
                f.write(f"{fecha} - Eliminado: Activar Windows\n")
            with open(os.path.join(CACHE_DIR, "recuperacion.txt"), "a") as f:
                f.write(f"{fecha} - Para recuperar: Ejecutar restaurar_activar_windows.bat\n")
        elif marca == "Modo de prueba":
            ejecutar_bat("eliminar_modo_prueba.bat")
            resultado = "Modo de prueba desactivado."
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a") as f:
                f.write(f"{fecha} - Eliminado: Modo de prueba\n")
            with open(os.path.join(CACHE_DIR, "recuperacion.txt"), "a") as f:
                f.write(f"{fecha} - Para recuperar: Ejecutar restaurar_modo_prueba.bat\n")
        elif marca == "Insider Preview":
            ejecutar_bat("eliminar_insider_preview.bat")
            resultado = "Insider Preview desactivado."
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a") as f:
                f.write(f"{fecha} - Eliminado: Insider Preview\n")
            with open(os.path.join(CACHE_DIR, "recuperacion.txt"), "a") as f:
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
            with open(resultado_path, "r") as f:
                resultado = f.read()
            with open(os.path.join(CACHE_DIR, "historial.txt"), "a") as fhist:
                fhist.write(f"{fecha} - Detección automática: {resultado}\n")
    else:
        resultado = "Para otras marcas, consulta documentación técnica."
    resultado_var.set(resultado)

# Interfaz gráfica
root = Tk()
root.title("Gestor de Marcas de Agua Windows")

Label(root, text="Selecciona la acción:").pack()
accion_var = StringVar(root)
accion_var.set("Eliminar marca de agua")
accion_menu = OptionMenu(root, accion_var, "Eliminar marca de agua", "Restaurar marca de agua", "Detectar automáticamente", "Otra")
accion_menu.pack()

Label(root, text="Selecciona la marca de agua:").pack()
marca_var = StringVar(root)
marca_var.set("Activar Windows")
marca_menu = OptionMenu(root, marca_var, "Activar Windows", "Modo de prueba", "Insider Preview")
marca_menu.pack()

resultado_var = StringVar(root)
Label(root, textvariable=resultado_var, fg="blue").pack()

Button(root, text="Ejecutar", command=lambda: procesar_accion(accion_var.get(), marca_var.get())).pack()

root.mainloop()