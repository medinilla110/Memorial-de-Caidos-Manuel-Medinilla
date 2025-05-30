# membresias.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class MembresiasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Membresías")
        self.geometry("650x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Registrar Usuario", self.registrar_usuario),
            ("Listar Usuarios",   self.listar_usuarios)
        ]
        for texto, cmd in acciones:
            b = tk.Button(
                btn_frame,
                text=texto,
                command=cmd,
                bg=BTN_BG, fg=FG_COLOR,
                width=18,
                font=("Helvetica", 11, "bold"),
                relief=tk.FLAT
            )
            b.pack(side=tk.LEFT, padx=10)

        # --- Listbox de usuarios ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Usuarios (Email - Nombre - País_ID - Fecha de registro):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

    def registrar_usuario(self):
        """Pide datos y lo inserta en la tabla member."""
        email      = simpledialog.askstring("Registrar", "Correo electrónico:")
        if not email:
            return
        nombre     = simpledialog.askstring("Registrar", "Nombre completo:")
        if not nombre:
            return
        country_id = simpledialog.askinteger("Registrar", "ID de país (country_id):")
        # country_id puede quedar None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos.")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO member (email, full_name, country_id) VALUES (%s, %s, %s)",
                (email, nombre, country_id)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario '{email}' registrado.")
        except Exception as e:
            messagebox.showerror("Error al registrar", str(e))
        finally:
            conn.close()

    def listar_usuarios(self):
        """Carga y muestra todos los registros de member."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT email, full_name, country_id, joined_at
                  FROM member
                  ORDER BY joined_at DESC
            """)
            for email, nombre, cid, joined in cur.fetchall():
                cid_disp = cid if cid is not None else "-"
                self.listbox.insert(
                    tk.END,
                    f"{email} - {nombre} - País_ID: {cid_disp} - Registrado: {joined}"
                )
        finally:
            conn.close()

if __name__ == "__main__":
    app = MembresiasApp()
    app.mainloop()
