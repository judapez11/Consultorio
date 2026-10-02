import calendar as _cal
import datetime as dt
import tkinter as tk
from tkinter import ttk

DIA_SEM = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

ANCHO = 430
ALTO = 330
MARGEN = 8
CAB_H = 26
DIA_H = 24
FILA_H = (ALTO - MARGEN - CAB_H - DIA_H - 10) / 6
COL_W = (ANCHO - 2 * MARGEN) / 7


class Calendario(ttk.Frame):
    """Mini calendario en Canvas (rápido, sin widgets por día)."""

    def __init__(self, master, fecha_inicial=None, on_seleccion=None, **kw):
        super().__init__(master, **kw)
        hoy = fecha_inicial or dt.date.today()
        self._año, self._mes = hoy.year, hoy.month
        self._seleccion = hoy
        self._on_seleccion = on_seleccion
        self._marcas = set()
        self._build()

    def _build(self):
        self.canvas = tk.Canvas(self, width=ANCHO, height=ALTO,
                                highlightthickness=0)
        self.canvas.pack()
        self.canvas.tag_bind("prev", "<Button-1>", lambda e: self._cambiar_mes(-1))
        self.canvas.tag_bind("next", "<Button-1>", lambda e: self._cambiar_mes(1))
        self._redibujar()

    def seleccion_get(self):
        return self._seleccion

    def seleccion_set(self, fecha):
        self._seleccion = fecha
        self._año, self._mes = fecha.year, fecha.month
        self._redibujar()

    def marcar(self, dias):
        self._marcas = set(dias)
        self._redibujar()

    def _cambiar_mes(self, delta):
        total = self._año * 12 + (self._mes - 1) + delta
        self._año, self._mes = divmod(total, 12)
        self._mes += 1
        self._redibujar()

    def _redibujar(self):
        c = self.canvas
        c.delete("all")

        # cabecera mes/año + flechas
        c.create_text(ANCHO / 2, CAB_H / 2 + 4,
                      text=f"{MESES[self._mes - 1]} {self._año}",
                      font=("Segoe UI", 12, "bold"), fill="#333333")
        c.create_text(MARGEN + 14, CAB_H / 2 + 4, text="◀",
                      font=("Segoe UI", 13), fill="#2266aa", tags="prev")
        c.create_text(ANCHO - MARGEN - 14, CAB_H / 2 + 4, text="▶",
                      font=("Segoe UI", 13), fill="#2266aa", tags="next")

        # días de la semana
        y0 = CAB_H + 4
        for i, nombre in enumerate(DIA_SEM):
            c.create_text(MARGEN + COL_W * i + COL_W / 2, y0 + DIA_H / 2,
                          text=nombre, font=("Segoe UI", 9, "bold"),
                          fill="#555555")

        # días del mes
        y1 = y0 + DIA_H
        prim = dt.date(self._año, self._mes, 1)
        inicio = prim.weekday()
        num_dias = _cal.monthrange(self._año, self._mes)[1]
        hoy = dt.date.today()
        for d in range(1, num_dias + 1):
            fila = (inicio + d - 1) // 7
            col = (inicio + d - 1) % 7
            x = MARGEN + col * COL_W
            y = y1 + fila * FILA_H
            fecha = dt.date(self._año, self._mes, d)
            tag = f"dia_{d}"
            color_fondo = "#ffffff"
            if fecha == hoy:
                color_fondo = "#fff3cd"
            if fecha == self._seleccion:
                color_fondo = "#cfe8ff"
            c.create_rectangle(x, y, x + COL_W - 2, y + FILA_H - 2,
                               fill=color_fondo, outline="#cccccc",
                               tags=(tag,))
            c.create_text(x + (COL_W - 2) / 2, y + (FILA_H - 2) / 2 - 2,
                          text=str(d), font=("Segoe UI", 10),
                          fill="#222222", tags=(tag,))
            if fecha in self._marcas:
                c.create_oval(x + (COL_W - 2) / 2 - 3, y + FILA_H - 9,
                              x + (COL_W - 2) / 2 + 3, y + FILA_H - 3,
                              fill="#e74c3c", outline="", tags=(tag,))
            c.tag_bind(tag, "<Button-1>", lambda e, f=fecha: self._elegir(f))
            c.tag_bind(tag, "<Enter>",
                       lambda e, x1=x, y1=y, w1=COL_W, h1=FILA_H:
                       self._resaltar(x1, y1, w1, h1, True))
            c.tag_bind(tag, "<Leave>",
                       lambda e, x1=x, y1=y, w1=COL_W, h1=FILA_H:
                       self._resaltar(x1, y1, w1, h1, False))

    def _resaltar(self, x, y, w, h, activo):
        items = self.canvas.find_overlapping(x, y, x + w - 2, y + h - 2)
        for it in items:
            if self.canvas.type(it) == "rectangle":
                if activo:
                    self.canvas.itemconfig(it, outline="#2266aa", width=2)
                else:
                    self.canvas.itemconfig(it, outline="#cccccc", width=1)
                break

    def _elegir(self, fecha):
        self._seleccion = fecha
        if self._on_seleccion:
            self._on_seleccion(fecha)
        else:
            self._redibujar()