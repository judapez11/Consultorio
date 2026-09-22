import tkinter as tk
from tkinter import ttk

ESTADOS = ["Sano", "Caries", "Obturado", "Ausente", "Endodoncia", "Protesis", "Otro"]

COLORES = {
    "Sano": "#ffffff",
    "Caries": "#ff5c5c",
    "Obturado": "#4a90d9",
    "Ausente": "#9a9a9a",
    "Endodoncia": "#a06fd1",
    "Protesis": "#5cb85c",
    "Otro": "#f0c040",
}

ZONAS = ["vestibular", "mesial", "oclusal", "distal", "lingual"]

SUPERIOR_DERECHA = ["18", "17", "16", "15", "14", "13", "12", "11"]
SUPERIOR_IZQUIERDA = ["21", "22", "23", "24", "25", "26", "27", "28"]
INFERIOR_IZQUIERDA = ["38", "37", "36", "35", "34", "33", "32", "31"]
INFERIOR_DERECHA = ["41", "42", "43", "44", "45", "46", "47", "48"]

TODO_DIENTES = (
    SUPERIOR_DERECHA + SUPERIOR_IZQUIERDA + INFERIOR_IZQUIERDA + INFERIOR_DERECHA
)

CUADRANTES = [
    ("SUPERIOR DERECHO", SUPERIOR_DERECHA),
    ("SUPERIOR IZQUIERDO", SUPERIOR_IZQUIERDA),
    ("INFERIOR IZQUIERDO", INFERIOR_IZQUIERDA),
    ("INFERIOR DERECHO", INFERIOR_DERECHA),
]

LADO_DERECHO = set(SUPERIOR_DERECHA + INFERIOR_DERECHA)
ARCO_SUPERIOR = set(SUPERIOR_DERECHA + SUPERIOR_IZQUIERDA)

LABEL_ZONA = {
    "vestibular": "Vest",
    "mesial": "Mes",
    "oclusal": "Ocl",
    "distal": "Dis",
    "lingual": "Ling",
}

MARGEN = 20
GAP = 30
SEP_DIENTE = 12
SEP_FILA = 8
NUM_STRIP = 16


class OdontogramaFrame(ttk.LabelFrame):
    def __init__(self, master, **kw):
        kw.setdefault("text", "Odontograma")
        super().__init__(master, padding=10, **kw)
        self._estados = {}
        for d in TODO_DIENTES:
            self._estados[d] = {z: "Sano" for z in ZONAS}
        self._paleta = "Sano"
        self._celdas = {}
        self._build()

    def _build(self):
        self.info_var = tk.StringVar(value="Haz clic en un sector del diente")
        ttk.Label(self, textvariable=self.info_var, font=("Segoe UI", 10)).pack(
            anchor="w", pady=(0, 6)
        )
        self.canvas = tk.Canvas(self, height=440, highlightthickness=1,
                                highlightbackground="#c0c0c0")
        self.canvas.pack(fill="x")
        self.canvas.bind("<Configure>", self._on_resize)
        self._dibujar_paleta()

    def _zona_por_posicion(self, diente):
        if diente in LADO_DERECHO:
            izq, der = "mesial", "distal"
        else:
            izq, der = "distal", "mesial"
        if diente in ARCO_SUPERIOR:
            top, bottom = "vestibular", "lingual"
        else:
            top, bottom = "lingual", "vestibular"
        return {"top": top, "izq": izq, "centro": "oclusal", "der": der, "bottom": bottom}

    def _on_resize(self, event):
        if event.width < 300:
            return
        self._dibujar(event.width)

    def _dibujar(self, ancho):
        self.canvas.delete("all")
        qw = (ancho - 2 * MARGEN - GAP) / 2
        paso_x = (qw - 2 * SEP_DIENTE) / 4
        zone_h = max(24, min(48, paso_x * 0.24))
        paso_y = NUM_STRIP + 3 * zone_h + SEP_FILA
        qh = 2 * paso_y + 8
        self.canvas.config(height=int(2 * qh + 2 * MARGEN))
        self._celdas = {}
        self._zone_h = zone_h
        for i, (titulo, dientes) in enumerate(CUADRANTES):
            fila, col = divmod(i, 2)
            ox = MARGEN + col * (qw + GAP)
            oy = MARGEN + fila * (qh + GAP)
            self.canvas.create_text(
                ox + qw / 2, oy - 10, text=titulo,
                font=("Segoe UI", 10, "bold"), fill="#333333",
            )
            for c, diente in enumerate(dientes):
                cx = ox + SEP_DIENTE + (c % 4) * paso_x
                cy = oy + 2 + (c // 4) * paso_y
                self._celdas[diente] = (cx, cy, paso_x - SEP_DIENTE)
                self._dibujar_diente(diente)

    def _dibujar_diente(self, diente):
        x, y, w = self._celdas[diente]
        zh = self._zone_h
        self.canvas.create_text(
            x + w / 2, y + NUM_STRIP / 2, text=diente,
            font=("Segoe UI", 9, "bold"), fill="#222222",
            tags=(f"num_{diente}",),
        )
        self.canvas.tag_bind(f"num_{diente}", "<Button-3>",
                             lambda e, d=diente: self._toggle_ausente(d))
        zonas = self._zona_por_posicion(diente)
        zy = y + NUM_STRIP
        z1 = zy + zh
        z2 = zy + 2 * zh
        z3 = zy + 3 * zh
        tercios = [w / 3, 2 * w / 3, w]
        rects = [
            (zonas["top"], x, zy, x + w, z1),
            (zonas["izq"], x, z1, x + tercios[0], z2),
            ("oclusal", x + tercios[0], z1, x + tercios[1], z2),
            (zonas["der"], x + tercios[1], z1, x + tercios[2], z2),
            (zonas["bottom"], x, z2, x + w, z3),
        ]
        fuente = ("Segoe UI", max(7, int(zh * 0.32)))
        for zona, x1, y1, x2, y2 in rects:
            tag = f"z_{diente}_{zona}"
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill=COLORES[self._estados[diente][zona]],
                outline="#888888", width=1, tags=(tag,),
            )
            self.canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2, text=LABEL_ZONA[zona],
                font=fuente, fill="#333333", tags=(tag,),
            )
            self.canvas.tag_bind(tag, "<Button-1>",
                                 lambda e, z=zona, d=diente: self._clic(d, z))
            self.canvas.tag_bind(tag, "<Button-3>",
                                 lambda e, d=diente: self._toggle_ausente(d))
            self.canvas.tag_bind(tag, "<Enter>",
                                 lambda e, z=zona, d=diente: self._hover(d, z))
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self._saliendo())

    def _pintar(self, diente):
        if not self._celdas:
            return
        ausente = self._ausente(diente)
        color = COLORES["Ausente"] if ausente else None
        for zona in ZONAS:
            for item in self.canvas.find_withtag(f"z_{diente}_{zona}"):
                if self.canvas.type(item) == "rectangle":
                    self.canvas.itemconfig(
                        item,
                        fill=color if color else COLORES[self._estados[diente][zona]],
                    )
        marca = f"x_{diente}"
        self.canvas.delete(marca)
        if ausente:
            x, y, w = self._celdas[diente]
            self.canvas.create_text(
                x + w / 2, y + NUM_STRIP + 1.5 * self._zone_h, text="✕",
                font=("Segoe UI", 22, "bold"), fill="#333333", tags=(marca,),
            )

    def _ausente(self, diente):
        return all(self._estados[diente][z] == "Ausente" for z in ZONAS)

    def _toggle_ausente(self, diente):
        if self._ausente(diente):
            for z in ZONAS:
                self._estados[diente][z] = "Sano"
        else:
            for z in ZONAS:
                self._estados[diente][z] = "Ausente"
        self._pintar(diente)
        estado = "Ausente" if self._ausente(diente) else "presente"
        self.info_var.set(f"Diente {diente}: {estado}")

    def _clic(self, diente, zona):
        if self._ausente(diente):
            return
        if self._estados[diente][zona] == self._paleta:
            self._estados[diente][zona] = "Sano"
        else:
            self._estados[diente][zona] = self._paleta
        self._pintar(diente)
        self.info_var.set(
            f"Diente {diente} · {LABEL_ZONA[zona]}: {self._estados[diente][zona]}"
        )

    def _hover(self, diente, zona):
        self.info_var.set(
            f"Diente {diente} · {LABEL_ZONA[zona]}: {self._estados[diente][zona]}"
        )

    def _saliendo(self):
        self.info_var.set(
            "Haz clic en un sector del diente · clic derecho = diente ausente"
        )

    def _dibujar_paleta(self):
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(8, 2))
        ttk.Label(barra, text="Estado:").pack(side="left", padx=(0, 6))
        self._botones_paleta = {}
        for estado in ESTADOS:
            boton = tk.Button(
                barra, text=estado, bg=COLORES[estado], relief="raised",
                command=lambda e=estado: self._elegir_estado(e),
            )
            boton.pack(side="left", padx=2)
            self._botones_paleta[estado] = boton
        self._elegir_estado("Sano")

        leyenda = ttk.Frame(self)
        leyenda.pack(fill="x")
        ttk.Label(
            leyenda,
            text="Clic en sector: pinta el estado elegido · clic otra vez: Sano · clic derecho: diente ausente",
            font=("Segoe UI", 8),
        ).pack(anchor="w")

    def _elegir_estado(self, estado):
        self._paleta = estado
        for nombre, boton in self._botones_paleta.items():
            boton.config(relief="sunken" if nombre == estado else "raised")

    def get_estados(self):
        return {d: dict(z) for d, z in self._estados.items()}

    def set_estados(self, estados):
        for diente in TODO_DIENTES:
            dato = (estados or {}).get(diente)
            if isinstance(dato, dict):
                for z in ZONAS:
                    estado = dato.get(z)
                    self._estados[diente][z] = estado if estado in ESTADOS else "Sano"
            elif isinstance(dato, str):
                estado = dato if dato in ESTADOS else "Sano"
                for z in ZONAS:
                    self._estados[diente][z] = estado
            else:
                for z in ZONAS:
                    self._estados[diente][z] = "Sano"
        for diente in TODO_DIENTES:
            if self._celdas:
                self._pintar(diente)