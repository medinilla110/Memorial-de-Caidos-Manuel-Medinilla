# unidades.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class UnidadesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Unidades")
        self.geometry("700x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_unidad),
            ("Consultar",  self.consultar_unidad),
            ("Actualizar", self.actualizar_unidad),
            ("Eliminar",   self.eliminar_unidad)
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

        # --- Listbox de unidades ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Unidades (ID - Nombre - Tipo - Parent_ID):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los registros de la tabla `unit`."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT unit_id, name, unit_type, parent_unit_id
                  FROM `unit`
                  ORDER BY unit_id
            """)
            for uid, nombre, utype, pid in cur.fetchall():
                pid_display = pid if pid is not None else "-"
                self.listbox.insert(
                    tk.END,
                    f"{uid} - {nombre} - {utype} - {pid_display}"
                )
        finally:
            conn.close()

    def agregar_unidad(self):
        """Pide datos y lo inserta en la BD."""
        nombre = simpledialog.askstring("Agregar", "Nombre de la unidad:")
        if not nombre:
            return

        utype = simpledialog.askstring(
            "Agregar",
            "Tipo de unidad (Division, Regiment, Battalion, Company, Platoon):"
        )
        if not utype:
            return

        pid = simpledialog.askinteger(
            "Agregar",
            "ID de unidad padre (parent_unit_id), o dejar vacío si no aplica:"
        )
        # pid puede ser None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return

        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO `unit` (name, unit_type, parent_unit_id) VALUES (%s, %s, %s)",
                (nombre, utype, pid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Unidad '{nombre}' agregada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_unidad(self):
        """Pide ID y muestra todos los campos."""
        uid = simpledialog.askinteger("Consultar", "ID de la unidad:")
        if uid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM `unit` WHERE unit_id = %s", (uid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos de la Unidad", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe unidad con ID {uid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_unidad(self):
        """Pide ID y nuevos datos para actualizar."""
        uid = simpledialog.askinteger("Actualizar", "ID de la unidad:")
        if uid is None:
            return
        nuevo_nombre = simpledialog.askstring("Actualizar", "Nuevo nombre de la unidad:")
        if not nuevo_nombre:
            return
        nuevo_utype = simpledialog.askstring(
            "Actualizar",
            "Nuevo tipo (Division, Regiment, Battalion, Company, Platoon):"
        )
        if not nuevo_utype:
            return
        nuevo_pid = simpledialog.askinteger(
            "Actualizar",
            "Nuevo parent_unit_id (ID de unidad padre) o dejar vacío:"
        )

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE `unit` SET name=%s, unit_type=%s, parent_unit_id=%s WHERE unit_id=%s",
                (nuevo_nombre, nuevo_utype, nuevo_pid, uid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Unidad {uid} actualizada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_unidad(self):
        """Pide ID y elimina el registro."""
        uid = simpledialog.askinteger("Eliminar", "ID de la unidad a eliminar:")
        if uid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar unidad {uid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM `unit` WHERE unit_id = %s", (uid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Unidad {uid} eliminada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = UnidadesApp()
    app.mainloop()
