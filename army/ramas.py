# ramas.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class RamasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Ramas")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_rama),
            ("Consultar",  self.consultar_rama),
            ("Actualizar", self.actualizar_rama),
            ("Eliminar",   self.eliminar_rama)
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

        # --- Listbox de ramas ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Ramas (ID - Nombre):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todas las ramas en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT branch_id, name FROM branch ORDER BY branch_id")
            for bid, nombre in cur.fetchall():
                self.listbox.insert(tk.END, f"{bid} - {nombre}")
        finally:
            conn.close()

    def agregar_rama(self):
        """Pide nombre de la rama y lo inserta en la BD."""
        nombre = simpledialog.askstring("Agregar", "Nombre de la rama:")
        if not nombre:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO branch (name) VALUES (%s)",
                (nombre,)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Rama '{nombre}' agregada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_rama(self):
        """Pide ID y muestra todos los campos."""
        bid = simpledialog.askinteger("Consultar", "ID de la rama:")
        if not bid:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM branch WHERE branch_id = %s", (bid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos de la Rama", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe rama con ID {bid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_rama(self):
        """Pide ID y nuevo nombre para actualizar."""
        bid = simpledialog.askinteger("Actualizar", "ID de la rama:")
        if not bid:
            return
        nuevo_nombre = simpledialog.askstring("Actualizar", "Nuevo nombre de la rama:")
        if not nuevo_nombre:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE branch SET name = %s WHERE branch_id = %s",
                (nuevo_nombre, bid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Rama {bid} actualizada a '{nuevo_nombre}'.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_rama(self):
        """Pide ID y elimina el registro."""
        bid = simpledialog.askinteger("Eliminar", "ID de la rama a eliminar:")
        if not bid:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar rama {bid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM branch WHERE branch_id = %s", (bid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Rama {bid} eliminada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = RamasApp()
    app.mainloop()
