# transportes.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class TransportesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Transportes")
        self.geometry("700x450")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_transporte),
            ("Consultar",  self.consultar_transporte),
            ("Actualizar", self.actualizar_transporte),
            ("Eliminar",   self.eliminar_transporte)
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

        # --- Listbox de transportes ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Transportes (ID - Tipo - Naturaleza - Ubicación):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los transportes en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT transport_id, type, nature, location
                  FROM `transport`
                  ORDER BY transport_id
            """)
            for tid, tipo, naturaleza, ubic in cur.fetchall():
                self.listbox.insert(
                    tk.END,
                    f"{tid} - {tipo} - {naturaleza} - {ubic or '-'}"
                )
        finally:
            conn.close()

    def agregar_transporte(self):
        """Pide datos y lo inserta en la BD."""
        tipo = simpledialog.askstring("Agregar", "Tipo de transporte (e.g. Avión, Submarino):")
        if not tipo:
            return
        naturaleza = simpledialog.askstring("Agregar", "Naturaleza (e.g. Combate, Transporte):")
        if naturaleza is None:
            return
        ubic = simpledialog.askstring("Agregar", "Ubicación al momento de la muerte:")
        # ubic puede ser None

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO `transport` (type, nature, location) VALUES (%s, %s, %s)",
                (tipo, naturaleza, ubic)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Transporte '{tipo}' agregado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_transporte(self):
        """Pide ID y muestra todos los campos."""
        tid = simpledialog.askinteger("Consultar", "ID del transporte:")
        if tid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM `transport` WHERE transport_id = %s", (tid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos del Transporte", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe transporte con ID {tid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_transporte(self):
        """Pide ID y nuevos datos para actualizar."""
        tid = simpledialog.askinteger("Actualizar", "ID del transporte:")
        if tid is None:
            return
        nuevo_tipo = simpledialog.askstring("Actualizar", "Nuevo tipo de transporte:")
        if not nuevo_tipo:
            return
        nueva_naturaleza = simpledialog.askstring("Actualizar", "Nueva naturaleza:")
        if nueva_naturaleza is None:
            return
        nueva_ubic = simpledialog.askstring("Actualizar", "Nueva ubicación:")

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE `transport` SET type=%s, nature=%s, location=%s WHERE transport_id=%s",
                (nuevo_tipo, nueva_naturaleza, nueva_ubic, tid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Transporte {tid} actualizado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_transporte(self):
        """Pide ID y elimina el registro."""
        tid = simpledialog.askinteger("Eliminar", "ID del transporte a eliminar:")
        if tid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar transporte {tid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM `transport` WHERE transport_id = %s", (tid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Transporte {tid} eliminado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = TransportesApp()
    app.mainloop()
