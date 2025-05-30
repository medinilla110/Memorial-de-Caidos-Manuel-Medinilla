# paises.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class PaisesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Países")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)

        # --- Barra de botones CRUD ---
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        acciones = [
            ("Agregar",    self.agregar_pais),
            ("Consultar",  self.consultar_pais),
            ("Actualizar", self.actualizar_pais),
            ("Eliminar",   self.eliminar_pais)
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

        # --- Listbox de países ---
        lb_frame = tk.Frame(self, bg=BG_COLOR)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        tk.Label(
            lb_frame,
            text="Lista de Países (ID - Nombre [ISO]):",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "underline")
        ).pack(anchor="w")

        self.listbox = tk.Listbox(lb_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.recargar_lista()

    def recargar_lista(self):
        """Carga todos los países en el listbox."""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT country_id, name, iso_code FROM country")
            for cid, name, iso in cur.fetchall():
                self.listbox.insert(tk.END, f"{cid} - {name} [{iso}]")
        finally:
            conn.close()

    def agregar_pais(self):
        """Pide nombre e ISO y lo inserta en la BD."""
        nombre = simpledialog.askstring("Agregar", "Nombre del país:")
        if not nombre:
            return
        iso = simpledialog.askstring("Agregar", "Código ISO (3 caracteres):")
        if not iso or len(iso) != 3:
            messagebox.showwarning("Aviso", "El código ISO debe tener 3 caracteres.")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO country (name, iso_code) VALUES (%s, %s)",
                (nombre, iso.upper())
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"País '{nombre}' agregado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))
        finally:
            conn.close()

    def consultar_pais(self):
        """Pide ID y muestra todos los campos."""
        cid = simpledialog.askinteger("Consultar", "ID del país:")
        if not cid:
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM country WHERE country_id = %s", (cid,))
            row = cur.fetchone()
            if row:
                info = "\n".join(f"{k}: {v}" for k, v in row.items())
                messagebox.showinfo("Datos del País", info)
            else:
                messagebox.showwarning("No encontrado", f"No existe país con ID {cid}.")
        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))
        finally:
            conn.close()

    def actualizar_pais(self):
        """Pide ID y nuevos datos para actualizar."""
        cid = simpledialog.askinteger("Actualizar", "ID del país:")
        if not cid:
            return
        nuevo_nombre = simpledialog.askstring("Actualizar", "Nuevo nombre:")
        nuevo_iso    = simpledialog.askstring("Actualizar", "Nuevo código ISO (3 caracteres):")
        if not nuevo_nombre or not nuevo_iso or len(nuevo_iso) != 3:
            messagebox.showwarning("Aviso", "Datos inválidos o incompletos.")
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE country SET name = %s, iso_code = %s WHERE country_id = %s",
                (nuevo_nombre, nuevo_iso.upper(), cid)
            )
            conn.commit()
            messagebox.showinfo("Éxito", f"País {cid} actualizado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))
        finally:
            conn.close()

    def eliminar_pais(self):
        """Pide ID y elimina el registro."""
        cid = simpledialog.askinteger("Eliminar", "ID del país a eliminar:")
        if not cid:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar país con ID {cid}?"):
            return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM country WHERE country_id = %s", (cid,))
            conn.commit()
            messagebox.showinfo("Eliminado", f"País {cid} eliminado.")
            self.recargar_lista()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    app = PaisesApp()
    app.mainloop()
