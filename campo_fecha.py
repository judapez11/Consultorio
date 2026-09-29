import datetime as dt
import tkinter as tk
from tkinter import ttk


def _formatear_fecha(texto):
    """Convierte solo digitos en dd/mm/yyyy (maximo 8 digitos)."""
    digitos = "".join(c for c in texto if c.isdigit())[:8]
    if len(digitos) <= 2:
        return digitos
    if len(digitos) <= 4:
        return digitos[:2] + "/" + digitos[2:]
    return digitos[:2] + "/" + digitos[2:4] + "/" + digitos[4:]


class CampoFecha(ttk.Frame):
    """Campo de fecha editable con mascara dd/mm/yyyy (sin calendario)."""

    def __init__(self, master, **kw):
        super().__init__(master)
        self._fecha = None
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var,
                               font=("Segoe UI", 12), justify="center")
        self.entry.pack(fill="x", expand=True)
        self.var.trace_add("write", self._aplicar_mascara)

    def _aplicar_mascara(self, *args):
        texto = self.var.get()
        formateado = _formatear_fecha(texto)
        if texto != formateado:
            self.var.set(formateado)
            try:
                self.entry.icursor(len(formateado))
            except tk.TclError:
                pass

    def get_date(self):
        try:
            return dt.datetime.strptime(self.var.get().strip(), "%d/%m/%Y").date()
        except ValueError:
            return None

    def set_date(self, fecha):
        self._fecha = fecha
        self.var.set(fecha.strftime("%d/%m/%Y"))

    def limpiar(self):
        self._fecha = None
        self.var.set("")