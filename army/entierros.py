# entierros.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class EntierrosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Entierros")
        self.geometry("700x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_entierro),
            ("Consultar",  self.consultar_entierro),
            ("Actualizar", self.actualizar_entierro),
            ("Eliminar",   self.eliminar_entierro)
        ]
        for texto, cmd in acciones:
            b = tk.Button(
                btn_frame,
                text=texto,
                command=cmd,
                bg=BTN_BG, fg=FG_COLOR,
                width=14,
                font=("Helvetica", 11, "bold"),
                relief=tk.FLAT
            )
            b.pack(side=tk.LEFT, padx=8)

        # --- Listbox de entierros ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Entierros (Soldier_ID - Place_ID - Cementerio - Parcela - Is_Unknown):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los registros de entierro."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT soldier_id, place_id, cemetery, plot, is_unknown
                  FROM burial
                  ORDER BY soldier_id
            """)
            for sid, pid, cem, plot, unk in cur.fetchall():
                unk_disp = 'Sí' if unk else 'No'
                self.listbox.insert(
                    tk.END,
                    f"{sid} - {pid} - {cem} - {plot} - Desconocido: {unk_disp}"
                )
        finally:
            conn.close()

    def agregar_entierro(self):
        """Pide datos y lo inserta en la BD."""
        sid = simpledialog.askinteger("Agregar", "ID del soldado (soldier_id):")
        if sid is None: return
        pid = simpledialog.askinteger("Agregar", "ID del lugar (place_id):")
        if pid is None: return
        cem = simpledialog.askstring("Agregar", "Nombre del cementerio:")
        if cem is None: return
        plot = simpledialog.askstring("Agregar", "Parcela/tumba:")
        if plot is None: return
        unk = messagebox.askyesno("Agregar", "¿Se desconoce el lugar exacto de inhumación?")

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO burial (soldier_id, place_id, cemetery, plot, is_unknown) VALUES (%s, %s, %s, %s, %s)",
                (sid, pid, cem, plot, int(unk))
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Entierro de soldado {sid} agregado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_entierro(self):
        """Pide soldier_id y muestra todos los campos."""
        sid = simpledialog.askinteger("Consultar", "ID del soldado:")
        if sid is None: return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM burial WHERE soldier_id = %s", (sid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                # Mostrar is_unknown como Sí/No
                info = info.replace("is_unknown: 1", "is_unknown: Sí").replace("is_unknown: 0", "is_unknown: No")
                messagebox.showinfo("Datos del Entierro", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe entierro para soldier_id {sid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_entierro(self):
        """Pide soldier_id y nuevos datos para actualizar."""
        sid = simpledialog.askinteger("Actualizar", "ID del soldado:")
        if sid is None: return
        pid = simpledialog.askinteger("Actualizar", "Nuevo place_id:")
        if pid is None: return
        cem = simpledialog.askstring("Actualizar", "Nuevo cementerio:")
        if cem is None: return
        plot = simpledialog.askstring("Actualizar", "Nueva parcela/tumba:")
        if plot is None: return
        unk = messagebox.askyesno("Actualizar", "¿Se desconoce el lugar exacto de inhumación?")

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE burial SET place_id=%s, cemetery=%s, plot=%s, is_unknown=%s WHERE soldier_id=%s",
                (pid, cem, plot, int(unk), sid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Entierro de soldado {sid} actualizado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_entierro(self):
        """Pide soldier_id y elimina el registro."""
        sid = simpledialog.askinteger("Eliminar", "ID del soldado a eliminar entierro:")
        if sid is None: return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar entierro de soldado {sid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM burial WHERE soldier_id = %s", (sid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Entierro de soldado {sid} eliminado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()

if __name__ == "__main__":
    app = EntierrosApp()
    app.mainloop()
