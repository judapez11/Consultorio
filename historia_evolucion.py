import datetime as dt
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry


class HistoriaEvolucionForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._build()

    def _build(self):
        cuadro = ttk.LabelFrame(self, text="Evolucion del paciente", padding=10)
        cuadro.pack(fill="x")

        self.fecha_entry = DateEntry(
            cuadro, width=14, date_pattern="dd/mm/yyyy", locale="es_ES"
        )
        ttk.Label(cuadro, text="Fecha").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="w", padx=6)

        cuadro2 = ttk.LabelFrame(self, text="Detalle", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self.detalle = tk.Text(cuadro2, width=60, height=6)
        self.detalle.pack(fill="x")

        cuadro3 = ttk.LabelFrame(self, text="Firmas", padding=10)
        cuadro3.pack(fill="x", pady=(8, 0))
        self.firma_pac_var = tk.StringVar()
        self.firma_prof_var = tk.StringVar()
        ttk.Label(cuadro3, text="Firma del paciente").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro3, textvariable=self.firma_pac_var).grid(
            row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro3, text="Firma del profesional").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro3, textvariable=self.firma_prof_var).grid(
            row=1, column=1, sticky="we", padx=6)
        cuadro3.columnconfigure(1, weight=1)

    def limpiar(self):
        self.fecha_entry.set_date(dt.date.today())
        self.detalle.delete("1.0", "end")
        self.firma_pac_var.set("")
        self.firma_prof_var.set("")

    def cargar(self, datos):
        self.limpiar()
        from datetime import datetime
        try:
            self.fecha_entry.set_date(datetime.strptime(datos["fecha"], "%Y-%m-%d").date())
        except (ValueError, KeyError):
            pass
        self.firma_pac_var.set(datos.get("firma_paciente", "") or "")
        self.firma_prof_var.set(datos.get("firma_profesional", "") or "")
        detalle = datos.get("detalle", "") or ""
        if detalle:
            self.detalle.insert("1.0", detalle)

    def validar(self):
        faltan = []
        if not self.detalle.get("1.0", "end").strip():
            faltan.append("Detalle")
        return faltan

    def datos(self):
        return {
            "fecha": self.fecha_entry.get_date().strftime("%Y-%m-%d"),
            "detalle": self.detalle.get("1.0", "end").strip(),
            "firma_paciente": self.firma_pac_var.get().strip(),
            "firma_profesional": self.firma_prof_var.get().strip(),
        }