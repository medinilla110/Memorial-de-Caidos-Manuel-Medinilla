# batallas.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class BatallasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Batallas")
        self.geometry("750x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_batalla),
            ("Consultar",  self.consultar_batalla),
            ("Actualizar", self.actualizar_batalla),
            ("Eliminar",   self.eliminar_batalla)
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

        # --- Listbox de batallas ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Batallas (ID - Nombre - Operación_ID - País_ID - Fechas):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todas las batallas en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT battle_id, name, operation_id, country_id, start_date, end_date
                  FROM `batallas`
                  ORDER BY battle_id
            """)
            for bid, nombre, opid, cid, ini, fin in cur.fetchall():
                ini = ini or "-"
                fin = fin or "-"
                self.listbox.insert(
                    tk.END,
                    f"{bid} - {nombre} - Op:{opid} - País:{cid} - {ini} to {fin}"
                )
        finally:
            conn.close()

    def agregar_batalla(self):
        """Pide datos y lo inserta en la BD."""
        nombre  = simpledialog.askstring("Agregar", "Nombre de la batalla:")
        if not nombre:
            return
        opid    = simpledialog.askinteger("Agregar", "ID de la operación (operation_id):")
        if opid is None:
            return
        cid     = simpledialog.askinteger("Agregar", "ID del país (country_id):")
        if cid is None:
            return
        ini     = simpledialog.askstring("Agregar", "Fecha inicio (YYYY-MM-DD):")
        if ini is None:
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
                "INSERT INTO `batallas` (name, operation_id, country_id, start_date, end_date) "
                "VALUES (%s,%s,%s,%s,%s)",
                (nombre, opid, cid, ini, fin)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Batalla '{nombre}' agregada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_batalla(self):
        """Pide ID y muestra todos los campos."""
        bid = simpledialog.askinteger("Consultar", "ID de la batalla:")
        if bid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM `batallas` WHERE battle_id = %s", (bid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos de la Batalla", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe batalla con ID {bid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_batalla(self):
        """Pide ID y nuevos datos para actualizar."""
        bid = simpledialog.askinteger("Actualizar", "ID de la batalla:")
        if bid is None:
            return
        nombre  = simpledialog.askstring("Actualizar", "Nuevo nombre de la batalla:")
        if not nombre:
            return
        opid    = simpledialog.askinteger("Actualizar", "Nuevo operation_id:")
        if opid is None:
            return
        cid     = simpledialog.askinteger("Actualizar", "Nuevo country_id:")
        if cid is None:
            return
        ini     = simpledialog.askstring("Actualizar", "Nueva fecha inicio (YYYY-MM-DD):")
        if ini is None:
            return
        fin     = simpledialog.askstring("Actualizar", "Nueva fecha fin (YYYY-MM-DD) o vacío:")
        fin = fin or None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE `batallas` SET name=%s, operation_id=%s, country_id=%s, start_date=%s, end_date=%s "
                "WHERE battle_id=%s",
                (nombre, opid, cid, ini, fin, bid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Batalla {bid} actualizada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_batalla(self):
        """Pide ID y elimina el registro."""
        bid = simpledialog.askinteger("Eliminar", "ID de la batalla a eliminar:")
        if bid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar batalla {bid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM `batallas` WHERE battle_id = %s", (bid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Batalla {bid} eliminada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = BatallasApp()
    app.mainloop()
