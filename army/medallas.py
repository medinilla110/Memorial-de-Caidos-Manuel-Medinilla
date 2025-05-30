# medallas.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class MedallasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Medallas")
        self.geometry("650x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_medalla),
            ("Consultar",  self.consultar_medalla),
            ("Actualizar", self.actualizar_medalla),
            ("Eliminar",   self.eliminar_medalla)
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

        # --- Listbox de medallas ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Medallas (ID - Nombre - País_ID):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todas las medallas en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT medal_id, name, country_id
                  FROM medal
                  ORDER BY medal_id
            """)
            for mid, nombre, cid in cur.fetchall():
                cid_display = cid if cid is not None else "-"
                self.listbox.insert(
                    tk.END,
                    f"{mid} - {nombre} - {cid_display}"
                )
        finally:
            conn.close()

    def agregar_medalla(self):
        """Pide datos y la inserta en la BD."""
        nombre = simpledialog.askstring("Agregar", "Nombre de la medalla:")
        if not nombre:
            return
        descripcion = simpledialog.askstring("Agregar", "Descripción:")
        if descripcion is None:
            return
        country_id = simpledialog.askinteger("Agregar", "ID del país (country_id) o dejar vacío:")
        # country_id puede ser None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO medal (name, description, country_id) VALUES (%s, %s, %s)",
                (nombre, descripcion, country_id)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Medalla '{nombre}' agregada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_medalla(self):
        """Pide ID y muestra todos los campos."""
        mid = simpledialog.askinteger("Consultar", "ID de la medalla:")
        if mid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM medal WHERE medal_id = %s", (mid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos de la Medalla", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe medalla con ID {mid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_medalla(self):
        """Pide ID y nuevos datos para actualizar."""
        mid = simpledialog.askinteger("Actualizar", "ID de la medalla:")
        if mid is None:
            return
        nuevo_nombre = simpledialog.askstring("Actualizar", "Nuevo nombre:")
        if not nuevo_nombre:
            return
        nueva_desc = simpledialog.askstring("Actualizar", "Nueva descripción:")
        if nueva_desc is None:
            return
        nuevo_cid = simpledialog.askinteger("Actualizar", "Nuevo country_id o dejar vacío:")

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE medal SET name=%s, description=%s, country_id=%s WHERE medal_id=%s",
                (nuevo_nombre, nueva_desc, nuevo_cid, mid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Medalla {mid} actualizada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_medalla(self):
        """Pide ID y elimina el registro."""
        mid = simpledialog.askinteger("Eliminar", "ID de la medalla a eliminar:")
        if mid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar medalla {mid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM medal WHERE medal_id = %s", (mid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Medalla {mid} eliminada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = MedallasApp()
    app.mainloop()
