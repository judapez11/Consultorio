import datetime as dt
import tkinter as tk
from tkinter import ttk

from campo_fecha import CampoFecha


class HistoriaEvolucionForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._build()

    def _build(self):
        cuadro = ttk.LabelFrame(self, text="Evolucion del paciente", padding=10)
        cuadro.pack(fill="x")

        self.fecha_entry = CampoFecha(cuadro)
        self.fecha_entry.set_date(dt.date.today())
        ttk.Label(cuadro, text="Fecha").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="w", padx=6)

        cuadro2 = ttk.LabelFrame(self, text="Detalle", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self.detalle = tk.Text(cuadro2, width=60, height=16)
        self.detalle.pack(fill="x")

    def limpiar(self):
        self.fecha_entry.set_date(dt.date.today())
        self.detalle.delete("1.0", "end")

    def cargar(self, datos):
        self.limpiar()
        from datetime import datetime
        try:
            self.fecha_entry.set_date(datetime.strptime(datos["fecha"], "%Y-%m-%d").date())
        except (ValueError, KeyError):
            pass
        detalle = datos.get("detalle", "") or ""
        if detalle:
            self.detalle.insert("1.0", detalle)

    def validar(self):
        faltan = []
        if self.fecha_entry.get_date() is None:
            faltan.append("Fecha invalida (dd/mm/yyyy)")
        if not self.detalle.get("1.0", "end").strip():
            faltan.append("Detalle")
        return faltan

    def datos(self):
        fecha = self.fecha_entry.get_date()
        return {
            "fecha": fecha.strftime("%Y-%m-%d") if fecha else "",
            "detalle": self.detalle.get("1.0", "end").strip(),
            "firma_paciente": "",
            "firma_profesional": "",
        }