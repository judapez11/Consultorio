import tkinter as tk
from tkinter import ttk

ESTADOS = ["Sano", "Caries", "Obturado", "Ausente", "Endodoncia", "Protesis", "Otro"]

SUPERIOR_DERECHA = ["18", "17", "16", "15", "14", "13", "12", "11"]
SUPERIOR_IZQUIERDA = ["21", "22", "23", "24", "25", "26", "27", "28"]
INFERIOR_IZQUIERDA = ["38", "37", "36", "35", "34", "33", "32", "31"]
INFERIOR_DERECHA = ["41", "42", "43", "44", "45", "46", "47", "48"]


class OdontogramaFrame(ttk.LabelFrame):
    def __init__(self, master, **kw):
        kw.setdefault("text", "Odontograma")
        super().__init__(master, padding=10, **kw)
        self._combos = {}
        self._build()

    def _build(self):
        ttk.Label(self, text="LADO DERECHO", font=("Segoe UI", 8, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w"
        )
        ttk.Label(self, text="LADO IZQUIERDO", font=("Segoe UI", 8, "bold")).grid(
            row=0, column=4, columnspan=4, sticky="e"
        )

        filas = [
            ("ARCO SUPERIOR", SUPERIOR_DERECHA, SUPERIOR_IZQUIERDA),
            ("ARCO INFERIOR", INFERIOR_IZQUIERDA, INFERIOR_DERECHA),
        ]
        for f, (titulo, izquierda, derecha) in enumerate(filas, start=1):
            ttk.Label(self, text=titulo, font=("Segoe UI", 9, "bold")).grid(
                row=f, column=0, columnspan=8, sticky="w", pady=(6, 2)
            )
            for c, diente in enumerate(izquierda + derecha):
                combo = ttk.Combobox(
                    self, values=ESTADOS, state="readonly", width=9
                )
                combo.set("Sano")
                combo.grid(row=f + 1, column=c, padx=2, pady=2)
                ttk.Label(self, text=diente, width=9).grid(
                    row=f + 2, column=c, padx=2
                )
                self._combos[diente] = combo

    def get_estados(self):
        return {d: c.get() for d, c in self._combos.items()}

    def set_estados(self, estados):
        for diente, combo in self._combos.items():
            estado = (estados or {}).get(diente)
            if estado in ESTADOS:
                combo.set(estado)
            else:
                combo.set("Sano")