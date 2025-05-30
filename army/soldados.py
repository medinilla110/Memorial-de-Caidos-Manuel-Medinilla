# soldados.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class SoldadosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Soldados")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_soldado),
            ("Consultar",  self.consultar_soldado),
            ("Actualizar", self.actualizar_soldado),
            ("Eliminar",   self.eliminar_soldado)
        ]
        for texto, cmd in acciones:
            b = tk.Button(
                btn_frame,
                text=texto,
                command=cmd,
                bg=BTN_BG, fg=FG_COLOR,
                width=12,
                font=("Helvetica", 11, "bold"),
                relief=tk.FLAT
            )
            b.pack(side=tk.LEFT, padx=10)

        # (Opcional) Un listbox para mostrar IDs actuales
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))
        tk.Label(lb_frame, text="Lista de Soldados (ID - Nombre Apellido):",
                 bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "underline"))\
            .pack(anchor="w")
        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los soldados en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT soldier_id, first_name, last_name FROM soldier")
            for sid, fn, ln in cur.fetchall():
                self.listbox.insert(tk.END, f"{sid} - {fn} {ln}")
        finally:
            conn.close()

    def agregar_soldado(self):
        """Pide nombre y apellido y lo inserta en la BD."""
        nombre   = simpledialog.askstring("Agregar", "Nombre:")
        apellido = simpledialog.askstring("Agregar", "Apellido:")
        if not nombre or not apellido:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO soldier (first_name, last_name) VALUES (%s, %s)",
                (nombre, apellido)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Soldado '{nombre} {apellido}' agregado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_soldado(self):
        """Pide ID y muestra todos los campos."""
        sid = simpledialog.askinteger("Consultar", "ID del soldado:")
        if not sid:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM soldier WHERE soldier_id = %s", (sid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos del Soldado", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe soldado con ID {sid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_soldado(self):
        """Pide ID y nuevos datos básicos para actualizar."""
        sid = simpledialog.askinteger("Actualizar", "ID del soldado:")
        if not sid:
            return
        nuevo_nombre   = simpledialog.askstring("Actualizar", "Nuevo nombre:")
        nuevo_apellido = simpledialog.askstring("Actualizar", "Nuevo apellido:")
        if not nuevo_nombre or not nuevo_apellido:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE soldier SET first_name = %s, last_name = %s WHERE soldier_id = %s",
                (nuevo_nombre, nuevo_apellido, sid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Soldado {sid} actualizado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_soldado(self):
        """Pide ID y elimina el registro."""
        sid = simpledialog.askinteger("Eliminar", "ID del soldado a eliminar:")
        if not sid:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar soldado {sid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM soldier WHERE soldier_id = %s", (sid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Soldado {sid} eliminado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = SoldadosApp()
    app.mainloop()
