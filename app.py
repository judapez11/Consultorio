import tkinter as tk
from tkinter import ttk

from pacientes import PacientesTab
from agenda import AgendaTab


def _placeholder(master, texto):
    frame = ttk.Frame(master, padding=40)
    ttk.Label(
        frame,
        text=texto,
        font=("Segoe UI", 16),
        anchor="center",
    ).pack(expand=True, fill="both")
    return frame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consultorio Dental")
        self.geometry("900x600")
        self.minsize(700, 450)

        self._tabs = ttk.Notebook(self)
        self._tabs.pack(fill="both", expand=True)

        self.agenda_tab = AgendaTab(self._tabs)
        self.pacientes_tab = PacientesTab(self._tabs)
        self.historia_tab = _placeholder(self._tabs, "Historia")

        self._tabs.add(self.agenda_tab, text="Agenda")
        self._tabs.add(self.pacientes_tab, text="Pacientes")
        self._tabs.add(self.historia_tab, text="Historia")