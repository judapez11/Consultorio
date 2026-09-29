import datetime as dt
import tkinter as tk
from tkinter import ttk

from campo_fecha import CampoFecha
from odontograma import OdontogramaFrame

EXAMEN_CARTA = [
    ("sellantes", "Sellantes"),
    ("fluor", "Fluor"),
    ("profilaxis", "Profilaxis"),
    ("resinas", "Resinas"),
    ("ionomero", "Ionomero"),
    ("endo_tem", "Endodoncia temporal"),
    ("endo_per", "Endodoncia permanente"),
    ("otros", "Otros"),
]

TIPO_DOCUMENTO = ["CC", "TI", "RC"]


class HistoriaCartaForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._build()

    def _build(self):
        cuadro = ttk.LabelFrame(self, text="Datos del certificado", padding=10)
        cuadro.pack(fill="x")

        self.fecha_entry = CampoFecha(cuadro)
        self.fecha_entry.set_date(dt.date.today())
        self.nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.num_doc_var = tk.StringVar()
        self.tipo_doc_var = tk.StringVar(value="CC")
        self.entidad_var = tk.StringVar()

        ttk.Label(cuadro, text="Fecha").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Nombre").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.nombre_var).grid(
            row=1, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Apellidos").grid(row=1, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.apellidos_var).grid(
            row=1, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Edad").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.edad_var).grid(
            row=2, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Tipo de documento").grid(row=2, column=2, sticky="w", pady=3, padx=(12, 0))
        tipo_frame = ttk.Frame(cuadro)
        tipo_frame.grid(row=2, column=3, sticky="w", padx=6)
        for col, tipo in enumerate(TIPO_DOCUMENTO):
            tk.Radiobutton(tipo_frame, text=tipo, variable=self.tipo_doc_var,
                           value=tipo, font=("Segoe UI", 11)).grid(row=0, column=col, padx=2)
        ttk.Label(cuadro, text="Numero de documento").grid(row=3, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.num_doc_var).grid(
            row=3, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Entidad solicitante").grid(row=3, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.entidad_var).grid(
            row=3, column=3, sticky="we", padx=6)

        for c in (1, 3):
            cuadro.columnconfigure(c, weight=1)

        cuadro2 = ttk.LabelFrame(self, text="Motivo de la consulta", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self.motivo = tk.Text(cuadro2, width=60, height=3)
        self.motivo.pack(fill="x")

        self.odontograma = OdontogramaFrame(self)
        self.odontograma.pack(fill="x", pady=(8, 0))

        cuadro3 = ttk.LabelFrame(self, text="Resumen", padding=10)
        cuadro3.pack(fill="x", pady=(8, 0))
        self.caries_var = tk.StringVar(value="NO")
        self.obturados_var = tk.StringVar(value="NO")
        tk.Label(cuadro3, text="Caries", font=("Segoe UI", 11)).pack(side="left")
        for v in ("SI", "NO"):
            tk.Radiobutton(cuadro3, text=v, variable=self.caries_var, value=v,
                           font=("Segoe UI", 11)).pack(side="left", padx=3)
        tk.Label(cuadro3, text="   Obturados", font=("Segoe UI", 11)).pack(side="left")
        for v in ("SI", "NO"):
            tk.Radiobutton(cuadro3, text=v, variable=self.obturados_var, value=v,
                           font=("Segoe UI", 11)).pack(side="left", padx=3)

        cuadro4 = ttk.LabelFrame(self, text="Examen de cavidad oral", padding=10)
        cuadro4.pack(fill="x", pady=(8, 0))
        cuadro4.columnconfigure(0, weight=1)
        self.examen_vars = {}
        for clave, etiqueta in EXAMEN_CARTA:
            self.examen_vars[clave] = tk.StringVar(value="NO")
        self.examen_canvas = tk.Canvas(cuadro4, height=8 * 32 + 6,
                                       highlightthickness=0, cursor="hand2")
        self.examen_canvas.grid(row=0, column=0, sticky="we")
        self.examen_canvas.bind("<Configure>", self._dibujar_examen)

        cuadro5 = ttk.LabelFrame(self, text="Plan de tratamiento", padding=10)
        cuadro5.pack(fill="x", pady=(8, 0))
        self.plan = tk.Text(cuadro5, width=60, height=3)
        self.plan.pack(fill="x")

        cuadro6 = ttk.LabelFrame(self, text="Firma", padding=10)
        cuadro6.pack(fill="x", pady=(8, 0))
        self.firma_var = tk.StringVar()
        ttk.Entry(cuadro6, textvariable=self.firma_var).grid(
            row=0, column=0, sticky="we", padx=6)
        cuadro6.columnconfigure(0, weight=1)

    def _seleccionar_examen(self, clave, valor):
        self.examen_vars[clave].set(valor)
        self._dibujar_examen()

    def _dibujar_examen(self, event=None):
        ancho = event.width if event and event.width > 100 else self.examen_canvas.winfo_width()
        if ancho < 100:
            return
        c = self.examen_canvas
        c.delete("all")
        cx1 = int(ancho * 0.70)
        cx2 = int(ancho * 0.85)
        r = 9
        c.create_text(8, 16, text="Item", font=("Segoe UI", 10, "bold"),
                      fill="#555555", anchor="w")
        c.create_text(cx1, 16, text="SI", font=("Segoe UI", 10, "bold"), fill="#555555")
        c.create_text(cx2, 16, text="NO", font=("Segoe UI", 10, "bold"), fill="#555555")
        c.create_line(4, 26, ancho - 4, 26, fill="#cccccc")
        for idx, (clave, etiqueta) in enumerate(EXAMEN_CARTA):
            y = 30 + idx * 32 + 17
            c.create_text(8, y, text=etiqueta, font=("Segoe UI", 11),
                          fill="#222222", anchor="w")
            for cx, valor in ((cx1, "SI"), (cx2, "NO")):
                tag = f"e_{idx}_{valor}"
                if self.examen_vars[clave].get() == valor:
                    c.create_oval(cx - r, y - r, cx + r, y + r,
                                  fill="#2266aa", outline="#2266aa", tags=(tag,))
                else:
                    c.create_oval(cx - r, y - r, cx + r, y + r,
                                  fill="#ffffff", outline="#888888", width=2,
                                  tags=(tag,))
                c.tag_bind(tag, "<Button-1>",
                           lambda e, cl=clave, v=valor: self._seleccionar_examen(cl, v))

    def prefill_nombre(self, nombre):
        if nombre and not self.nombre_var.get().strip():
            self.nombre_var.set(nombre)

    def limpiar(self):
        self.fecha_entry.set_date(dt.date.today())
        self.nombre_var.set("")
        self.apellidos_var.set("")
        self.edad_var.set("")
        self.num_doc_var.set("")
        self.tipo_doc_var.set("CC")
        self.entidad_var.set("")
        self.caries_var.set("NO")
        self.obturados_var.set("NO")
        for var in self.examen_vars.values():
            var.set("NO")
        for t in (self.motivo, self.plan):
            t.delete("1.0", "end")
        self.firma_var.set("")
        self.odontograma.set_estados({})
        self._dibujar_examen()

    def cargar(self, datos):
        self.limpiar()
        from datetime import datetime
        try:
            self.fecha_entry.set_date(datetime.strptime(datos["fecha"], "%Y-%m-%d").date())
        except (ValueError, KeyError):
            pass
        for var, clave in ((self.nombre_var, "nombre"), (self.apellidos_var, "apellidos"),
                           (self.edad_var, "edad"), (self.num_doc_var, "num_documento"),
                           (self.tipo_doc_var, "tipo_documento"),
                           (self.entidad_var, "entidad_solicitante"),
                           (self.caries_var, "caries"), (self.obturados_var, "obturados"),
                           (self.firma_var, "firma")):
            var.set(datos.get(clave, "") or "")
        for clave, var in self.examen_vars.items():
            valor = (datos.get("examen") or {}).get(clave)
            if valor in ("SI", "NO"):
                var.set(valor)
        for t, clave in ((self.motivo, "motivo_consulta"), (self.plan, "plan_tratamiento")):
            valor = datos.get(clave, "") or ""
            if valor:
                t.insert("1.0", valor)
        self.odontograma.set_estados(datos.get("odontograma") or {})
        self._dibujar_examen()

    def validar(self):
        faltan = []
        if self.fecha_entry.get_date() is None:
            faltan.append("Fecha invalida (dd/mm/yyyy)")
        if not self.entidad_var.get().strip():
            faltan.append("Entidad solicitante")
        if not self.motivo.get("1.0", "end").strip():
            faltan.append("Motivo de la consulta")
        return faltan

    def tiene_contenido(self):
        for var in (self.nombre_var, self.apellidos_var, self.edad_var,
                    self.num_doc_var, self.entidad_var, self.firma_var):
            if var.get().strip():
                return True
        if self.caries_var.get() == "SI" or self.obturados_var.get() == "SI":
            return True
        for var in self.examen_vars.values():
            if var.get() == "SI":
                return True
        for t in (self.motivo, self.plan):
            if t.get("1.0", "end").strip():
                return True
        for zonas in self.odontograma.get_estados().values():
            for estado in zonas.values():
                if estado != "Sano":
                    return True
        return False

    def datos(self):
        def texto(t):
            return t.get("1.0", "end").strip()

        fecha = self.fecha_entry.get_date()
        return {
            "fecha": fecha.strftime("%Y-%m-%d") if fecha else "",
            "nombre": self.nombre_var.get().strip(),
            "apellidos": self.apellidos_var.get().strip(),
            "edad": self.edad_var.get().strip(),
            "num_documento": self.num_doc_var.get().strip(),
            "tipo_documento": self.tipo_doc_var.get(),
            "entidad_solicitante": self.entidad_var.get().strip(),
            "motivo_consulta": texto(self.motivo),
            "caries": self.caries_var.get(),
            "obturados": self.obturados_var.get(),
            "examen": {clave: var.get() for clave, var in self.examen_vars.items()},
            "odontograma": self.odontograma.get_estados(),
            "plan_tratamiento": texto(self.plan),
            "firma": self.firma_var.get().strip(),
        }