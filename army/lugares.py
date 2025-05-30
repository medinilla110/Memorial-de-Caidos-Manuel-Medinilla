# lugares.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class LugaresApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Lugares")
        self.geometry("650x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_lugar),
            ("Consultar",  self.consultar_lugar),
            ("Actualizar", self.actualizar_lugar),
            ("Eliminar",   self.eliminar_lugar)
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

        # --- Listbox de lugares ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Lugares (ID - País_ID - Estado/Provincia - Ciudad):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los lugares en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT place_id, country_id, state_province, city 
                FROM place
                ORDER BY place_id
            """)
            for pid, cid, estado, ciudad in cur.fetchall():
                self.listbox.insert(
                    tk.END,
                    f"{pid} - {cid} - {estado or ''} - {ciudad or ''}"
                )
        finally:
            conn.close()

    def agregar_lugar(self):
        """Pide datos y lo inserta en la BD."""
        cid     = simpledialog.askinteger("Agregar", "ID del país (country_id):")
        if cid is None:
            return
        estado  = simpledialog.askstring("Agregar", "Estado o provincia:")
        ciudad  = simpledialog.askstring("Agregar", "Ciudad:")
        lat     = simpledialog.askfloat("Agregar", "Latitud (decimal):")
        lon     = simpledialog.askfloat("Agregar", "Longitud (decimal):")
        if estado is None or ciudad is None or lat is None or lon is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO place
                  (country_id, state_province, city, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cid, estado, ciudad, lat, lon)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Lugar '{ciudad}' agregado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_lugar(self):
        """Pide ID y muestra todos los campos."""
        pid = simpledialog.askinteger("Consultar", "ID del lugar:")
        if pid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM place WHERE place_id = %s", (pid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos del Lugar", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe lugar con ID {pid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_lugar(self):
        """Pide ID y nuevos datos para actualizar."""
        pid = simpledialog.askinteger("Actualizar", "ID del lugar:")
        if pid is None:
            return
        cid     = simpledialog.askinteger("Actualizar", "Nuevo país (country_id):")
        estado  = simpledialog.askstring("Actualizar", "Nuevo estado/provincia:")
        ciudad  = simpledialog.askstring("Actualizar", "Nueva ciudad:")
        lat     = simpledialog.askfloat("Actualizar", "Nueva latitud (decimal):")
        lon     = simpledialog.askfloat("Actualizar", "Nueva longitud (decimal):")
        if cid is None or estado is None or ciudad is None or lat is None or lon is None:
            messagebox.showwarning("Aviso", "Datos incompletos.")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE place
                SET country_id=%s, state_province=%s, city=%s, latitude=%s, longitude=%s
                WHERE place_id=%s
                """,
                (cid, estado, ciudad, lat, lon, pid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Lugar {pid} actualizado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_lugar(self):
        """Pide ID y elimina el registro."""
        pid = simpledialog.askinteger("Eliminar", "ID del lugar a eliminar:")
        if pid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar lugar {pid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM place WHERE place_id = %s", (pid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Lugar {pid} eliminado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = LugaresApp()
    app.mainloop()
