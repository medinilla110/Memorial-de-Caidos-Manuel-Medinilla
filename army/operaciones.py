# operaciones.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class OperacionesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Operaciones")
        self.geometry("700x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_operacion),
            ("Consultar",  self.consultar_operacion),
            ("Actualizar", self.actualizar_operacion),
            ("Eliminar",   self.eliminar_operacion)
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

        # --- Listbox de operaciones ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Operaciones (ID - Nombre - Código - Fechas):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todas las operaciones en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            # Ahora apuntamos a la tabla `operaciones`
            cur.execute("""
                SELECT operation_id, name, code_name, start_date, end_date
                  FROM `operaciones`
                  ORDER BY operation_id
            """)
            for oid, nombre, codigo, inicio, fin in cur.fetchall():
                ini = inicio or "-"
                fn  = fin or "-"
                self.listbox.insert(
                    tk.END,
                    f"{oid} - {nombre} ({codigo}) - {ini} to {fn}"
                )
        finally:
            conn.close()

    def agregar_operacion(self):
        """Pide datos y lo inserta en la BD."""
        nombre  = simpledialog.askstring("Agregar", "Nombre de la operación:")
        if not nombre:
            return
        codigo  = simpledialog.askstring("Agregar", "Código de la operación:")
        if codigo is None:
            return
        inicio  = simpledialog.askstring("Agregar", "Fecha inicio (YYYY-MM-DD):")
        if inicio is None:
            return
        fin     = simpledialog.askstring("Agregar", "Fecha fin (YYYY-MM-DD) o vacío:")
        fin = fin or None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO `operaciones` (name, code_name, start_date, end_date) VALUES (%s, %s, %s, %s)",
                (nombre, codigo, inicio, fin)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Operación '{nombre}' agregada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_operacion(self):
        """Pide ID y muestra todos los campos."""
        oid = simpledialog.askinteger("Consultar", "ID de la operación:")
        if oid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM `operaciones` WHERE operation_id = %s", (oid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos de la Operación", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe operación con ID {oid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_operacion(self):
        """Pide ID y nuevos datos para actualizar."""
        oid = simpledialog.askinteger("Actualizar", "ID de la operación:")
        if oid is None:
            return
        nuevo_nombre = simpledialog.askstring("Actualizar", "Nuevo nombre:")
        if not nuevo_nombre:
            return
        nuevo_codigo = simpledialog.askstring("Actualizar", "Nuevo código:")
        if nuevo_codigo is None:
            return
        nueva_inicio = simpledialog.askstring("Actualizar", "Nueva fecha inicio (YYYY-MM-DD):")
        if nueva_inicio is None:
            return
        nueva_fin    = simpledialog.askstring("Actualizar", "Nueva fecha fin (YYYY-MM-DD) o vacío:")
        nueva_fin = nueva_fin or None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE `operaciones` SET name=%s, code_name=%s, start_date=%s, end_date=%s WHERE operation_id=%s",
                (nuevo_nombre, nuevo_codigo, nueva_inicio, nueva_fin, oid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Operación {oid} actualizada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_operacion(self):
        """Pide ID y elimina el registro."""
        oid = simpledialog.askinteger("Eliminar", "ID de la operación a eliminar:")
        if oid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar operación {oid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM `operaciones` WHERE operation_id = %s", (oid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Operación {oid} eliminada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = OperacionesApp()
    app.mainloop()
