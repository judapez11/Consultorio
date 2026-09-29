import tkinter as tk
from tkinter import ttk

from pacientes import PacientesTab
from agenda import AgendaTab
from historia import DOCUMENTOS, DocumentoTab


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultorio Dental")
        self.geometry("900x600")
        self.minsize(700, 450)
        self._maximizar()

    def _maximizar(self):
        try:
            self.attributes("-zoomed", True)
        except tk.TclError:
            pass

        self._tabs = ttk.Notebook(self)
        self._tabs.pack(fill="both", expand=True)

        self.agenda_tab = AgendaTab(self._tabs)
        self.pacientes_tab = PacientesTab(self._tabs)
        self._tabs.add(self.agenda_tab, text="Agenda")
        self._tabs.add(self.pacientes_tab, text="Pacientes")

        self.documento_tabs = {}
        for nombre, conf in DOCUMENTOS.items():
            tab = DocumentoTab(self._tabs, nombre, conf)
            self.documento_tabs[nombre] = tab
            self._tabs.add(tab, text=nombre)