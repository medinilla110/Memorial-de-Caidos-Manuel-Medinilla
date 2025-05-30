# causas_de_muerte.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class CausasDeMuerteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Causas de Muerte")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_causa),
            ("Consultar",  self.consultar_causa),
            ("Actualizar", self.actualizar_causa),
            ("Eliminar",   self.eliminar_causa)
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

        # --- Listbox de causas ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Causas de Muerte (ID - Descripción):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.recargar_lista()

    def recargar_lista(self):
        """Carga todas las causas de muerte en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT cause_id, description FROM cause_of_death ORDER BY cause_id")
            for cid, desc in cur.fetchall():
                self.listbox.insert(tk.END, f"{cid} - {desc}")
        finally:
            conn.close()

    def agregar_causa(self):
        """Pide descripción y la inserta en la BD."""
        desc = simpledialog.askstring("Agregar", "Descripción de la causa de muerte:")
        if not desc:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO cause_of_death (description) VALUES (%s)",
                (desc,)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Causa '{desc}' agregada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_causa(self):
        """Pide ID y muestra la descripción."""
        cid = simpledialog.askinteger("Consultar", "ID de la causa:")
        if cid is None:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM cause_of_death WHERE cause_id = %s", (cid,))
            row = cur.fetchone()
            if row:
                messagebox.showinfo("Datos de la Causa", f"ID: {row['cause_id']}\nDescripción: {row['description']}")
            else:
                messagebox.showwarning("No encontrado", f"No existe causa con ID {cid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_causa(self):
        """Pide ID y nueva descripción para actualizar."""
        cid = simpledialog.askinteger("Actualizar", "ID de la causa:")
        if cid is None:
            return
        nueva_desc = simpledialog.askstring("Actualizar", "Nueva descripción:")
        if not nueva_desc:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE cause_of_death SET description = %s WHERE cause_id = %s",
                (nueva_desc, cid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"Causa {cid} actualizada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_causa(self):
        """Pide ID y elimina la causa."""
        cid = simpledialog.askinteger("Eliminar", "ID de la causa a eliminar:")
        if cid is None:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar causa {cid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM cause_of_death WHERE cause_id = %s", (cid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"Causa {cid} eliminada.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = CausasDeMuerteApp()
    app.mainloop()
