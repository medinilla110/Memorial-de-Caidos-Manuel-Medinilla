import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from db_connection import get_connection
from PIL import Image, ImageTk

# Colores “militares”
BG_COLOR = '#556b2f'   # verde oliva oscuro
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'    # verde para los botones

# Mapeo etiqueta → script
SCRIPT_FILES = {
    'Soldados':                    'soldados.py',
    'Países':                      'paises.py',
    'Lugares':                     'lugares.py',
    'Ramas':                       'ramas.py',
    'Rangos':                      'rangos.py',
    'Causas de Muerte':            'causas_de_muerte.py',
    'Unidades':                    'unidades.py',
    'Medallas':                    'medallas.py',
    'Operaciones':                 'operaciones.py',
    'Batallas':                    'batallas.py',
    'Transportes':                 'transportes.py',
    'Entierros':                   'entierros.py',
    # Estos dos irán en la segunda fila:
    'Membresías':                  'membresias.py',
    'Consulta Completa Soldado':   'consulta_completa_soldado.py',
}

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memorial de Soldados Caídos")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)

        # --- Primera fila de botones (todas menos Membresías y Consulta Completa) ---
        first_row = [k for k in SCRIPT_FILES if k not in ('Membresías','Consulta Completa Soldado')]
        toolbar1 = tk.Frame(self, bg=BG_COLOR)
        toolbar1.pack(fill=tk.X, pady=(10,0))
        for label in first_row:
            btn = tk.Button(
                toolbar1,
                text=label,
                bg=BTN_BG, fg=FG_COLOR,
                relief=tk.FLAT,
                width=12,
                command=lambda l=label: self.launch_script(l)
            )
            btn.pack(side=tk.LEFT, padx=3, pady=4)

        # --- Segunda fila de botones (solo Membresías y Consulta Completa) ---
        second_row = ['Membresías','Consulta Completa Soldado']
        toolbar2 = tk.Frame(self, bg=BG_COLOR)
        toolbar2.pack(fill=tk.X, pady=(2,0))
        for label in second_row:
            btn = tk.Button(
                toolbar2,
                text=label,
                bg=BTN_BG, fg=FG_COLOR,
                relief=tk.FLAT,
                width=20,
                command=lambda l=label: self.launch_script(l)
            )
            btn.pack(side=tk.LEFT, padx=6, pady=4)

        # --- Título ---
        lbl = tk.Label(
            self,
            text="Bienvenido al Sistema de Memoria Histórica",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 16, "bold")
        )
        lbl.pack(pady=(20, 10))

        # --- Logo ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path  = os.path.join(script_dir, "logos.jpg")
        try:
            img = Image.open(logo_path)
            img = img.resize((200, 200), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(img)
            logo_lbl = tk.Label(self, image=self.logo, bg=BG_COLOR)
            logo_lbl.pack(pady=(0,20))
        except Exception as e:
            messagebox.showerror(
                "Error cargando logo",
                f"No se pudo abrir:\n{logo_path}\n\n{e}"
            )

    def launch_script(self, label):
        """Ejecuta en un nuevo proceso el script asociado a la etiqueta."""
        script_name = SCRIPT_FILES[label]
        script_dir  = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, script_name)

        if not os.path.isfile(script_path):
            messagebox.showerror("Error", f"No se encontró el archivo:\n{script_path}")
            return

        try:
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            messagebox.showerror("Error al lanzar script", str(e))


if __name__ == "__main__":
    # Verificar conexión al iniciar
    conn = get_connection()
    if not conn:
        messagebox.showwarning("Conexión", "No se pudo conectar a la base de datos.")
    else:
        conn.close()

    app = MainApp()
    app.mainloop()
