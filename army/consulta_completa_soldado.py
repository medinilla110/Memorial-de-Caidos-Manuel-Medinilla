# consulta_completa_soldado.py

import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'
BTN_BG   = '#4e5d2e'

class ConsultaCompletaSoldadoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consulta Completa de Soldado")
        self.geometry("900x900")
        self.configure(bg=BG_COLOR)

        # Canvas + Scrollbar
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.v_scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame interior desplazable
        self.inner = tk.Frame(self.canvas, bg=BG_COLOR)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor='nw')

        # Ajustar el ancho al tamaño del canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.inner_id, width=e.width)
        )

        # Actualizar scroll cuando crece el contenido
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )




        # 1) Pedir ID
        sid = simpledialog.askinteger("Consulta Completa", "ID del soldado:")
        if not sid:
            self.destroy()
            return
        self.sid = sid

        # 2) Construir todos los formularios de asignación
        self._build_basic_frame()
        self._build_medal_frame()
        self._build_rank_frame()
        self._build_unit_frame()
        self._build_superior_frame()
        self._build_battle_frame()

        # 3) Mostrar datos al final
        self._show_data()

    # ——— Básicos y fechas ———————————————————————
    def _build_basic_frame(self):
        frm = tk.LabelFrame(
            self.inner,                     # <<--- aquí
            text="Editar datos básicos",
            bg=BG_COLOR, fg=FG_COLOR,
            font=("Helvetica", 12, "bold")
        )
        frm.pack(fill=tk.X, padx=10, pady=5)

        # Country, Cause, Branch, Transport (igual que antes) + Birth/Death dates
        # (código idéntico al anterior para estos 4 combobox)
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT country_id, name FROM country ORDER BY name"); countries = cur.fetchall()
        cur.execute("SELECT cause_id, description FROM cause_of_death ORDER BY description"); causes = cur.fetchall()
        cur.execute("SELECT branch_id, name FROM branch ORDER BY name"); branches = cur.fetchall()
        cur.execute("SELECT transport_id, type FROM transport ORDER BY type"); transports = cur.fetchall()
        conn.close()

        def place_cb(row, label, values):
            tk.Label(frm, text=label+":", bg=BG_COLOR, fg=FG_COLOR).grid(row=row, column=0, sticky="e", padx=5, pady=3)
            cb = ttk.Combobox(frm, values=[f"{v[0]} - {v[1]}" for v in values], width=30)
            cb.grid(row=row, column=1, sticky="w", padx=5, pady=3)
            return cb

        self.country_cb   = place_cb(0, "País", countries)
        self.cause_cb     = place_cb(1, "Causa muerte", causes)
        self.branch_cb    = place_cb(2, "Rama", branches)
        self.transport_cb = place_cb(3, "Transporte muerte", transports)

        # Fechas de nacimiento / muerte
        tk.Label(frm, text="Fecha nacimiento (YYYY-MM-DD):", bg=BG_COLOR, fg=FG_COLOR).grid(row=4, column=0, sticky="e", padx=5, pady=3)
        self.birth_entry = tk.Entry(frm, width=33)
        self.birth_entry.grid(row=4, column=1, sticky="w", padx=5, pady=3)

        tk.Label(frm, text="Fecha muerte (YYYY-MM-DD):", bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, sticky="e", padx=5, pady=3)
        self.death_entry = tk.Entry(frm, width=33)
        self.death_entry.grid(row=5, column=1, sticky="w", padx=5, pady=3)

        save_btn = tk.Button(frm, text="Guardar básicos", bg=BTN_BG, fg=FG_COLOR,
                             command=self._save_basic)
        save_btn.grid(row=6, column=0, columnspan=2, pady=(8,5))

    def _save_basic(self):
        try:
            cid = int(self.country_cb.get().split(" - ")[0])
            caus = int(self.cause_cb.get().split(" - ")[0])
            bid = int(self.branch_cb.get().split(" - ")[0])
            tid = int(self.transport_cb.get().split(" - ")[0])
            bd  = self.birth_entry.get().strip() or None
            dd  = self.death_entry.get().strip() or None
        except:
            return messagebox.showerror("Error", "Revisa tus selecciones y fechas.")

        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            UPDATE soldier
               SET country_id=%s,
                   cause_id=%s,
                   branch_id=%s,
                   death_transport_id=%s,
                   birth_date=%s,
                   death_date=%s
             WHERE soldier_id=%s
        """, (cid, caus, bid, tid, bd, dd, self.sid))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Datos básicos actualizados.")
        self._show_data()

    # ——— Medallas ——————————————————————————
    def _build_medal_frame(self):
        frm = tk.LabelFrame(self.inner, text="Agregar Medalla", 
                            bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        frm.pack(fill=tk.X, padx=10, pady=5)

        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT medal_id, name FROM medal ORDER BY name"); medals = cur.fetchall()
        conn.close()

        tk.Label(frm, text="Medalla:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.medal_cb = ttk.Combobox(frm, values=[f"{m[0]} - {m[1]}" for m in medals], width=30)
        self.medal_cb.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frm, text="Fecha (YYYY-MM-DD):", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.medal_date = tk.Entry(frm, width=12); self.medal_date.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(frm, text="Cita:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.medal_cit = tk.Entry(frm, width=30); self.medal_cit.grid(row=2, column=1, padx=5)

        btn = tk.Button(frm, text="Agregar medalla", bg=BTN_BG, fg=FG_COLOR, command=self._add_medal)
        btn.grid(row=3, column=0, columnspan=2, pady=(6,4))

    def _add_medal(self):
        try:
            mid = int(self.medal_cb.get().split(" - ")[0])
            date = self.medal_date.get().strip()
            cit  = self.medal_cit.get().strip()
        except:
            return messagebox.showerror("Error", "Revisa medalla y fecha.")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO soldier_medal(soldier_id, medal_id, award_date, citation)
            VALUES(%s,%s,%s,%s)
        """, (self.sid, mid, date or None, cit or None))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Medalla asignada.")
        self._show_data()

    # ——— Ascensos —————————————————————————
    def _build_rank_frame(self):
        frm = tk.LabelFrame(self.inner, text="Agregar Ascenso", 
                            bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        frm.pack(fill=tk.X, padx=10, pady=5)

        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT rank_id, name FROM rangos ORDER BY name"); ranks = cur.fetchall()
        conn.close()

        tk.Label(frm, text="Rango:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.rank_cb = ttk.Combobox(frm, values=[f"{r[0]} - {r[1]}" for r in ranks], width=30)
        self.rank_cb.grid(row=0, column=1, padx=5)

        tk.Label(frm, text="Desde (YYYY-MM-DD):", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5)
        self.rank_from = tk.Entry(frm, width=12); self.rank_from.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(frm, text="Hasta (YYYY-MM-DD):", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5)
        self.rank_to = tk.Entry(frm, width=12); self.rank_to.grid(row=2, column=1, sticky="w", padx=5)

        btn = tk.Button(frm, text="Agregar ascenso", bg=BTN_BG, fg=FG_COLOR, command=self._add_rank)
        btn.grid(row=3, column=0, columnspan=2, pady=(6,4))

    def _add_rank(self):
        try:
            rid = int(self.rank_cb.get().split(" - ")[0])
            f = self.rank_from.get().strip()
            t = self.rank_to.get().strip()
        except:
            return messagebox.showerror("Error", "Revisa rango y fechas.")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO soldier_rank(soldier_id, rank_id, start_date, end_date)
            VALUES(%s,%s,%s,%s)
        """, (self.sid, rid, f or None, t or None))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Ascenso agregado.")
        self._show_data()

    # ——— Unidades ————————————————————————
    def _build_unit_frame(self):
        frm = tk.LabelFrame(self.inner, text="Agregar Unidad", 
                            bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        frm.pack(fill=tk.X, padx=10, pady=5)

        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT unit_id, name FROM `unit` ORDER BY name"); units = cur.fetchall()
        conn.close()

        tk.Label(frm, text="Unidad:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5)
        self.unit_cb = ttk.Combobox(frm, values=[f"{u[0]} - {u[1]}" for u in units], width=30)
        self.unit_cb.grid(row=0, column=1, padx=5)

        tk.Label(frm, text="Desde:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5)
        self.unit_from = tk.Entry(frm, width=12); self.unit_from.grid(row=1, column=1, sticky="w", padx=5)
        tk.Label(frm, text="Hasta:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5)
        self.unit_to = tk.Entry(frm, width=12); self.unit_to.grid(row=2, column=1, sticky="w", padx=5)

        btn = tk.Button(frm, text="Agregar unidad", bg=BTN_BG, fg=FG_COLOR, command=self._add_unit)
        btn.grid(row=3, column=0, columnspan=2, pady=(6,4))

    def _add_unit(self):
        try:
            uid = int(self.unit_cb.get().split(" - ")[0])
            f   = self.unit_from.get().strip()
            t   = self.unit_to.get().strip()
        except:
            return messagebox.showerror("Error", "Revisa unidad y fechas.")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO soldier_unit(soldier_id, unit_id, start_date, end_date)
            VALUES(%s,%s,%s,%s)
        """, (self.sid, uid, f or None, t or None))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Unidad asignada.")
        self._show_data()

    # ——— Superiores ———————————————————————
    def _build_superior_frame(self):
        frm = tk.LabelFrame(self.inner, text="Asignar Superior", 
                            bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        frm.pack(fill=tk.X, padx=10, pady=5)

        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT soldier_id, CONCAT(first_name,' ',last_name) FROM soldier ORDER BY last_name")
        svals = cur.fetchall()
        conn.close()

        tk.Label(frm, text="Superior:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5)
        self.sup_cb = ttk.Combobox(frm, values=[f"{s[0]} - {s[1]}" for s in svals], width=30)
        self.sup_cb.grid(row=0, column=1, padx=5)

        tk.Label(frm, text="Desde:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5)
        self.sup_from = tk.Entry(frm, width=12); self.sup_from.grid(row=1, column=1, sticky="w", padx=5)
        tk.Label(frm, text="Hasta:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5)
        self.sup_to = tk.Entry(frm, width=12); self.sup_to.grid(row=2, column=1, sticky="w", padx=5)

        btn = tk.Button(frm, text="Agregar superior", bg=BTN_BG, fg=FG_COLOR, command=self._add_superior)
        btn.grid(row=3, column=0, columnspan=2, pady=(6,4))

    def _add_superior(self):
        try:
            sup_id = int(self.sup_cb.get().split(" - ")[0])
            f      = self.sup_from.get().strip()
            t      = self.sup_to.get().strip()
        except:
            return messagebox.showerror("Error", "Revisa superior y fechas.")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO soldier_superior(subordinate_id, superior_id, start_date, end_date)
            VALUES(%s,%s,%s,%s)
        """, (self.sid, sup_id, f or None, t or None))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Superior asignado.")
        self._show_data()

    # ——— Batallas —————————————————————————
    def _build_battle_frame(self):
        frm = tk.LabelFrame(self.inner, text="Agregar Batalla", 
                            bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 12, "bold"))
        frm.pack(fill=tk.X, padx=10, pady=5)

        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT battle_id, name FROM batallas ORDER BY name"); bvals = cur.fetchall()
        conn.close()

        tk.Label(frm, text="Batalla:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="e", padx=5)
        self.bat_cb = ttk.Combobox(frm, values=[f"{b[0]} - {b[1]}" for b in bvals], width=30)
        self.bat_cb.grid(row=0, column=1, padx=5)

        tk.Label(frm, text="Rol:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5)
        self.bat_role = tk.Entry(frm, width=20); self.bat_role.grid(row=1, column=1, sticky="w", padx=5)
        self.bat_wound = tk.BooleanVar()
        tk.Checkbutton(frm, text="Herido", variable=self.bat_wound, bg=BG_COLOR, fg=FG_COLOR).grid(
            row=2, column=1, sticky="w", padx=5)

        btn = tk.Button(frm, text="Agregar batalla", bg=BTN_BG, fg=FG_COLOR, command=self._add_battle)
        btn.grid(row=3, column=0, columnspan=2, pady=(6,4))

    def _add_battle(self):
        try:
            bid = int(self.bat_cb.get().split(" - ")[0])
            role = self.bat_role.get().strip()
            w    = int(self.bat_wound.get())
        except:
            return messagebox.showerror("Error", "Revisa batalla y rol.")
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            INSERT INTO soldier_battle(soldier_id, battle_id, role, wounded)
            VALUES(%s,%s,%s,%s)
        """, (self.sid, bid, role or None, w))
        conn.commit(); conn.close()
        messagebox.showinfo("Éxito", "Batalla asignada.")
        self._show_data()

    # ——— Mostrar datos ——————————————————————
    def _show_data(self):
        data = self._fetch_data(self.sid)
        if data is None:
            messagebox.showwarning("No encontrado", f"No existe soldado con ID {self.sid}.")
            return

        # Si ya existe el widget de texto, lo actualizamos
        if hasattr(self, 'st'):
            self.st.config(state=tk.NORMAL)
            self.st.delete("1.0", tk.END)
        else:
            # Creamos el widget solo una vez
            self.st = ScrolledText(self.inner, bg='white', fg='black', font=("Courier", 10))
            self.st.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Insertamos y desactivamos edición
        self.st.insert(tk.END, data)
        self.st.config(state=tk.DISABLED)


    def _fetch_data(self, sid):
        """Recupera todos los datos de un soldado como texto formateado."""
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        # 1) Datos básicos + transporte
        cur.execute("""
            SELECT 
              s.soldier_id,
              s.first_name,
              s.patronymic,
              s.last_name,
              c.name    AS country,
              bp.city   AS birth_city,
              bp.state_province AS birth_state,
              s.birth_date,
              dp.city   AS death_city,
              dp.state_province AS death_state,
              s.death_date,
              cod.description AS cause,
              b.name    AS branch,
              t.`type`  AS transport_type,
              t.nature  AS transport_nature
            FROM soldier s
            LEFT JOIN country        c ON s.country_id           = c.country_id
            LEFT JOIN place          bp ON s.birth_place_id       = bp.place_id
            LEFT JOIN place          dp ON s.death_place_id       = dp.place_id
            LEFT JOIN cause_of_death cod ON s.cause_id            = cod.cause_id
            LEFT JOIN branch         b ON s.branch_id            = b.branch_id
            LEFT JOIN transport      t ON s.death_transport_id   = t.transport_id
            WHERE s.soldier_id = %s
        """, (sid,))
        soldier = cur.fetchone()
        if not soldier:
            conn.close()
            return None

        # 2) Medallas
        cur.execute("""
            SELECT m.name AS medal, sm.award_date, sm.citation
              FROM soldier_medal sm
              JOIN medal m ON sm.medal_id = m.medal_id
             WHERE sm.soldier_id = %s
        """, (sid,))
        medals = cur.fetchall()

        # 3) Ascensos
        cur.execute("""
            SELECT r.name AS rank, sr.start_date, sr.end_date
              FROM soldier_rank sr
              JOIN rangos r ON sr.rank_id = r.rank_id
             WHERE sr.soldier_id = %s
          ORDER BY sr.start_date
        """, (sid,))
        ranks = cur.fetchall()

        # 4) Unidades
        cur.execute("""
            SELECT u.name AS unit, su.start_date, su.end_date
              FROM soldier_unit su
              JOIN `unit` u ON su.unit_id = u.unit_id
             WHERE su.soldier_id = %s
          ORDER BY su.start_date
        """, (sid,))
        units = cur.fetchall()

        # 5) Superiores
        cur.execute("""
            SELECT sup.first_name AS sup_fn, sup.last_name AS sup_ln,
                   ss.start_date, ss.end_date
              FROM soldier_superior ss
              JOIN soldier sup ON ss.superior_id = sup.soldier_id
             WHERE ss.subordinate_id = %s
          ORDER BY ss.start_date
        """, (sid,))
        sups = cur.fetchall()

        # 6) Batallas
        cur.execute("""
            SELECT b.name AS battle, op.name AS operation, c.name AS country,
                   sb.role, sb.wounded
              FROM soldier_battle sb
              JOIN batallas b ON sb.battle_id = b.battle_id
              LEFT JOIN operaciones op ON b.operation_id = op.operation_id
              LEFT JOIN country c ON b.country_id = c.country_id
             WHERE sb.soldier_id = %s
        """, (sid,))
        battles = cur.fetchall()

        # 7) Entierro
        cur.execute("""
            SELECT pl.city   AS burial_city,
                   pl.state_province AS burial_state,
                   br.cemetery, br.plot, br.is_unknown
              FROM burial br
              JOIN place pl ON br.place_id = pl.place_id
             WHERE br.soldier_id = %s
        """, (sid,))
        burial = cur.fetchone()

        conn.close()

        # ——— Construcción de lines ——————————————
        lines = []
        s = soldier
        lines.append(f"ID: {s['soldier_id']}")
        lines.append(f"Nombre: {s['first_name']} {s.get('patronymic','')} {s['last_name']}")
        lines.append(f"País de origen: {s['country']}")
        lines.append(f"Nacido en: {s['birth_city']}, {s['birth_state']} el {s['birth_date']}")
        lines.append(f"Murió en:  {s['death_city']}, {s['death_state']} el {s['death_date']}")
        lines.append(f"Rama: {s['branch']}")
        lines.append(f"Causa de muerte: {s['cause']}")

        t_type = s.get('transport_type') or '-'
        t_nat  = s.get('transport_nature') or '-'
        lines.append(f"Transporte: {t_type} ({t_nat})")

        # Medallas
        lines.append("\nMedallas:")
        if medals:
            for m in medals:
                lines.append(f"  • {m['medal']} — {m['award_date']}: {m['citation']}")
        else:
            lines.append("  (ninguna)")

        # Ascensos
        lines.append("\nAscensos:")
        if ranks:
            for r in ranks:
                lines.append(f"  • {r['rank']} — {r['start_date']} a {r['end_date']}")
        else:
            lines.append("  (ninguno)")

        # Unidades
        lines.append("\nUnidades:")
        if units:
            for u in units:
                lines.append(f"  • {u['unit']} — {u['start_date']} a {u['end_date']}")
        else:
            lines.append("  (ninguna)")

        # Superiores
        lines.append("\nSuperiores:")
        if sups:
            for sup in sups:
                lines.append(f"  • {sup['sup_fn']} {sup['sup_ln']} — {sup['start_date']} a {sup['end_date']}")
        else:
            lines.append("  (ninguno)")

        # Batallas
        lines.append("\nBatallas:")
        if battles:
            for b in battles:
                wounded = "Sí" if b['wounded'] else "No"
                lines.append(f"  • {b['battle']} (Op: {b['operation']}, País: {b['country']}) — rol {b['role']}, herido: {wounded}")
        else:
            lines.append("  (ninguna)")

        # Entierro
        lines.append("\nEntierro:")
        if burial:
            unk = "Sí" if burial['is_unknown'] else "No"
            lines.append(f"  • {burial['burial_city']}, {burial['burial_state']}")
            lines.append(f"    Cementerio: {burial['cemetery']}, Parcela: {burial['plot']}, Desconocido: {unk}")
        else:
            lines.append("  (no registrado)")

        return "\n".join(lines)



if __name__ == "__main__":
    ConsultaCompletaSoldadoApp().mainloop()
