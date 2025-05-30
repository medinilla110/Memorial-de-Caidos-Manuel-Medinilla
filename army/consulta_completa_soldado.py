# consulta_completa_soldado.py

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.scrolledtext import ScrolledText
from db_connection import get_connection

# Colores “militares”
BG_COLOR = '#556b2f'
FG_COLOR = 'white'

class ConsultaCompletaSoldadoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consulta Completa de Soldado")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)
        self._run_query()

    def _run_query(self):
        sid = simpledialog.askinteger("Consulta Completa", "ID del soldado:")
        if not sid:
            self.destroy()
            return

        data = self._fetch_data(sid)
        if data is None:
            messagebox.showwarning("No encontrado", f"No existe soldado con ID {sid}.")
            self.destroy()
            return

        st = ScrolledText(self, bg='white', fg='black', font=("Courier", 10))
        st.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        st.insert(tk.END, data)
        st.config(state=tk.DISABLED)

    def _fetch_data(self, sid):
        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "No hay conexión a la BD")
            self.destroy()
            return

        try:
            cur = conn.cursor(dictionary=True)

            # 1. Datos básicos del soldado + Transporte (type y nature)
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
                return None

            # 2. Medallas
            cur.execute("""
                SELECT m.name AS medal, sm.award_date, sm.citation
                  FROM soldier_medal sm
                  JOIN medal m ON sm.medal_id = m.medal_id
                  WHERE sm.soldier_id = %s
            """, (sid,))
            medals = cur.fetchall()

            # 3. Ascensos
            cur.execute("""
                SELECT r.name AS rank, sr.start_date, sr.end_date
                  FROM soldier_rank sr
                  JOIN `rangos` r ON sr.rank_id = r.rank_id
                  WHERE sr.soldier_id = %s
                  ORDER BY sr.start_date
            """, (sid,))
            ranks = cur.fetchall()

            # 4. Unidades
            cur.execute("""
                SELECT u.name AS unit, su.start_date, su.end_date
                  FROM soldier_unit su
                  JOIN `unit` u ON su.unit_id = u.unit_id
                  WHERE su.soldier_id = %s
                  ORDER BY su.start_date
            """, (sid,))
            units = cur.fetchall()

            # 5. Superiores
            cur.execute("""
                SELECT sup.first_name AS sup_fn, sup.last_name AS sup_ln,
                       ss.start_date, ss.end_date
                  FROM soldier_superior ss
                  JOIN soldier sup ON ss.superior_id = sup.soldier_id
                  WHERE ss.subordinate_id = %s
                  ORDER BY ss.start_date
            """, (sid,))
            sups = cur.fetchall()

            # 6. Batallas
            cur.execute("""
                SELECT b.name AS battle, op.name AS operation, c.name AS country,
                       sb.role, sb.wounded
                  FROM soldier_battle sb
                  JOIN `batallas` b ON sb.battle_id = b.battle_id
                  LEFT JOIN operaciones op ON b.operation_id = op.operation_id
                  LEFT JOIN country c ON b.country_id = c.country_id
                  WHERE sb.soldier_id = %s
            """, (sid,))
            battles = cur.fetchall()

            # 7. Entierro
            cur.execute("""
                SELECT pl.city   AS burial_city,
                       pl.state_province AS burial_state,
                       br.cemetery, br.plot, br.is_unknown
                  FROM burial br
                  JOIN place pl ON br.place_id = pl.place_id
                  WHERE br.soldier_id = %s
            """, (sid,))
            burial = cur.fetchone()

        finally:
            conn.close()

        # Formateo de resultados
        lines = []
        s = soldier
        lines.append(f"ID: {s['soldier_id']}")
        lines.append(f"Nombre completo: {s['first_name']} {s.get('patronymic','')} {s['last_name']}")
        lines.append(f"País de origen: {s['country']}")
        lines.append(f"Nacido en: {s['birth_city']}, {s['birth_state']} el {s['birth_date']}")
        lines.append(f"Murió en:  {s['death_city']}, {s['death_state']} el {s['death_date']}")
        lines.append(f"Rama: {s['branch']}")
        lines.append(f"Causa de muerte: {s['cause']}")

        # Transporte
        t_type = s.get('transport_type')
        t_nat  = s.get('transport_nature')
        if t_type or t_nat:
            lines.append(f"Transporte: {t_type or '-'} ({t_nat or '-'})")

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
    app = ConsultaCompletaSoldadoApp()
    app.mainloop()
