# rangos.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class RangosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Rangos")
        self.geometry("650x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_rango),
            ("Consultar",  self.consultar_rango),
            ("Actualizar", self.actualizar_rango),
            ("Eliminar",   self.eliminar_rango)
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

        # --- Listbox de rangos ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Rangos (ID - Nombre - Branch_ID - Seniority):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los rangos en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            # Ahora apunta a la tabla `rangos`
            cur.execute("SELECT rank_id, name, branch_id, seniority FROM `rangos` ORDER BY rank_id")
            for rid, nombre, bid, senior in cur.fetchall():
                self.listbox.insert(
                    tk.END,
                    f"{rid} - {nombre} - {bid} - {senior}"
                )
        finally:
            conn.close()

    def agregar_rango(self):
        """Pide datos y lo inserta en la BD."""
        nombre   = simpledialog.askstring("Agregar", "Nombre del rango:")
        if not nombre:
            return
        branch_id = simpledialog.askinteger("Agregar", "ID de la rama (branch_id):")
        if branch_id is None:
            return
        seniority = simpledialog.askinteger("Agregar", "Nivel de seniority (entero):")
        if seniority is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            # También INSERT en `rangos`
            cur.execute(
                "INSERT INTO `rangos` (name, branch_id, seniority) VALUES (%s, %s, %s)",
                (nombre, branch_id, seniority)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Rango '{nombre}' agregado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_rango(self):
        """Pide ID y muestra todos los campos."""
        rid = simpledialog.askinteger("Consultar", "ID del rango:")
        if rid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM `rangos` WHERE rank_id = %s", (rid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos del Rango", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe rango con ID {rid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_rango(self):
        """Pide ID y nuevos datos para actualizar."""
        rid = simpledialog.askinteger("Actualizar", "ID del rango:")
        if rid is None:
            return
        nuevo_nombre   = simpledialog.askstring("Actualizar", "Nuevo nombre del rango:")
        if not nuevo_nombre:
            return
        new_branch_id  = simpledialog.askinteger("Actualizar", "Nuevo branch_id:")
        if new_branch_id is None:
            return
        new_seniority  = simpledialog.askinteger("Actualizar", "Nuevo seniority:")
        if new_seniority is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE `rangos` SET name=%s, branch_id=%s, seniority=%s WHERE rank_id=%s",
                (nuevo_nombre, new_branch_id, new_seniority, rid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Rango {rid} actualizado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_rango(self):
        """Pide ID y elimina el registro."""
        rid = simpledialog.askinteger("Eliminar", "ID del rango a eliminar:")
        if rid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar rango {rid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM `rangos` WHERE rank_id = %s", (rid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Rango {rid} eliminado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = RangosApp()
    app.mainloop()

