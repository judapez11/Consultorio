import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry

from odontograma import OdontogramaFrame

EXAMEN_ORAL = [
    "Labios", "Encias", "Carrillos", "T. oclusion", "Lengua", "Piso boca",
    "S. paranasales", "F. desgastes", "Mucosa oral", "Gl. salivales",
    "M. masticatorios", "Fract. dental", "Maxilares", "Paladar", "A.T.M",
    "Protesis",
]


class HistoriaOdontologicaForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._build()

    def _build(self):
        cuadro = ttk.LabelFrame(self, text="1. Datos de identificacion", padding=10)
        cuadro.pack(fill="x")

        self.fecha_entry = DateEntry(
            cuadro, width=14, date_pattern="dd/mm/yyyy", locale="es_ES"
        )
        self.ocupacion_var = tk.StringVar()
        self.estado_civil_var = tk.StringVar()
        self.fecha_nac_var = tk.StringVar()

        ttk.Label(cuadro, text="Fecha de consulta").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="w", padx=6)
        ttk.Label(cuadro, text="Ocupacion").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.ocupacion_var, width=30).grid(row=1, column=1, padx=6)
        ttk.Label(cuadro, text="Estado civil").grid(row=1, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.estado_civil_var, width=30).grid(row=1, column=3, padx=6)
        ttk.Label(cuadro, text="Fecha de nacimiento").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.fecha_nac_var, width=30).grid(row=2, column=1, padx=6)

        ttk.Label(cuadro, text="Acudiente (si es menor de edad)", font=("Segoe UI", 9, "bold")).grid(
            row=3, column=0, columnspan=4, sticky="w", pady=(10, 2)
        )
        self.acu_a1 = tk.StringVar()
        self.acu_a2 = tk.StringVar()
        self.acu_nom = tk.StringVar()
        self.acu_dir = tk.StringVar()
        self.acu_tel = tk.StringVar()
        self.acu_par = tk.StringVar()

        ttk.Label(cuadro, text="Primer apellido").grid(row=4, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.acu_a1, width=25).grid(row=4, column=1, padx=6)
        ttk.Label(cuadro, text="Segundo apellido").grid(row=4, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.acu_a2, width=25).grid(row=4, column=3, padx=6)
        ttk.Label(cuadro, text="Nombre").grid(row=5, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.acu_nom, width=25).grid(row=5, column=1, padx=6)
        ttk.Label(cuadro, text="Parentesco").grid(row=5, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.acu_par, width=25).grid(row=5, column=3, padx=6)
        ttk.Label(cuadro, text="Direccion").grid(row=6, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.acu_dir, width=25).grid(row=6, column=1, padx=6)
        ttk.Label(cuadro, text="Telefono").grid(row=6, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.acu_tel, width=25).grid(row=6, column=3, padx=6)

        cuadro.columnconfigure(3, weight=1)

        cuadro2 = ttk.LabelFrame(self, text="2. Anamnesis", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self.ant_pers = self._campo_texto(cuadro2, "Antecedentes medicos personales", 0)
        self.ant_fam = self._campo_texto(cuadro2, "Antecedentes medicos familiares", 1)
        self.motivo = self._campo_texto(cuadro2, "Motivo de la consulta", 2)

        cuadro3 = ttk.LabelFrame(self, text="3. Habitos", padding=10)
        cuadro3.pack(fill="x", pady=(8, 0))
        self.cepillado_var = tk.StringVar()
        self.seda_var = tk.StringVar()
        self.enjuague_var = tk.StringVar()
        ttk.Label(cuadro3, text="Cepillado").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro3, textvariable=self.cepillado_var, width=25).grid(row=0, column=1, padx=6)
        ttk.Label(cuadro3, text="Uso de seda dental").grid(row=0, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro3, textvariable=self.seda_var, width=25).grid(row=0, column=3, padx=6)
        ttk.Label(cuadro3, text="Uso de enjuague").grid(row=0, column=4, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro3, textvariable=self.enjuague_var, width=25).grid(row=0, column=5, padx=6)

        self.odontograma = OdontogramaFrame(self)
        self.odontograma.pack(fill="x", pady=(8, 0))

        cuadro4 = ttk.LabelFrame(self, text="5. Examen de cavidad oral", padding=10)
        cuadro4.pack(fill="x", pady=(8, 0))
        ttk.Label(cuadro4, text="Item").grid(row=0, column=0, sticky="w")
        ttk.Label(cuadro4, text="Normal").grid(row=0, column=1)
        ttk.Label(cuadro4, text="Alterado").grid(row=0, column=2)
        self.examen_vars = {}
        for i, item in enumerate(EXAMEN_ORAL, start=1):
            var = tk.StringVar(value="N")
            self.examen_vars[item] = var
            ttk.Label(cuadro4, text=item).grid(row=i, column=0, sticky="w", padx=4, pady=1)
            ttk.Radiobutton(cuadro4, variable=var, value="N").grid(row=i, column=1)
            ttk.Radiobutton(cuadro4, variable=var, value="AN").grid(row=i, column=2)

        cuadro5 = ttk.LabelFrame(self, text="6. Diagnostico", padding=10)
        cuadro5.pack(fill="x", pady=(8, 0))
        self.dx_blando = self._campo_texto(cuadro5, "Tejido blando", 0)
        self.dx_dental = self._campo_texto(cuadro5, "Dental", 1)
        self.dx_perio = self._campo_texto(cuadro5, "Periodontal", 2)
        self.dx_craneo = self._campo_texto(cuadro5, "Craneofacial", 3)
        self.dx_oclusion = self._campo_texto(cuadro5, "Oclusion", 4)

    def _campo_texto(self, padre, etiqueta, fila):
        ttk.Label(padre, text=etiqueta).grid(row=fila, column=0, sticky="nw", pady=3)
        texto = tk.Text(padre, width=60, height=3)
        texto.grid(row=fila, column=1, sticky="we", padx=6, pady=3)
        padre.columnconfigure(1, weight=1)
        return texto

    def limpiar(self):
        for var in (
            self.ocupacion_var, self.estado_civil_var, self.fecha_nac_var,
            self.acu_a1, self.acu_a2, self.acu_nom, self.acu_dir, self.acu_tel,
            self.acu_par, self.cepillado_var, self.seda_var, self.enjuague_var,
        ):
            var.set("")
        for texto in (
            self.ant_pers, self.ant_fam, self.motivo,
            self.dx_blando, self.dx_dental, self.dx_perio,
            self.dx_craneo, self.dx_oclusion,
        ):
            texto.delete("1.0", "end")
        for var in self.examen_vars.values():
            var.set("N")
        self.odontograma.set_estados({})

    def cargar(self, datos):
        self.limpiar()
        from datetime import datetime
        try:
            fecha = datetime.strptime(datos["fecha"], "%Y-%m-%d")
            self.fecha_entry.set_date(fecha.date())
        except (ValueError, KeyError):
            pass
        mapeos = {
            "ocupacion": self.ocupacion_var, "estado_civil": self.estado_civil_var,
            "fecha_nacimiento": self.fecha_nac_var,
            "acudiente_apellido1": self.acu_a1, "acudiente_apellido2": self.acu_a2,
            "acudiente_nombre": self.acu_nom, "acudiente_direccion": self.acu_dir,
            "acudiente_telefono": self.acu_tel, "acudiente_parentesco": self.acu_par,
            "cepillado": self.cepillado_var, "seda": self.seda_var,
            "enjuague": self.enjuague_var,
        }
        for clave, var in mapeos.items():
            var.set(datos.get(clave, "") or "")
        textos = {
            "antecedentes_personales": self.ant_pers,
            "antecedentes_familiares": self.ant_fam,
            "motivo_consulta": self.motivo,
            "diagnostico_tejido_blando": self.dx_blando,
            "diagnostico_dental": self.dx_dental,
            "diagnostico_periodontal": self.dx_perio,
            "diagnostico_craneofacial": self.dx_craneo,
            "diagnostico_oclusion": self.dx_oclusion,
        }
        for clave, texto in textos.items():
            valor = datos.get(clave, "") or ""
            if valor:
                texto.insert("1.0", valor)
        for item, var in self.examen_vars.items():
            valor = (datos.get("examen_oral") or {}).get(item)
            if valor in ("N", "AN"):
                var.set(valor)
        self.odontograma.set_estados(datos.get("odontograma") or {})

    def datos(self):
        def texto(t):
            return t.get("1.0", "end").strip()

        examen = {item: var.get() for item, var in self.examen_vars.items()}
        return {
            "fecha": self.fecha_entry.get_date().strftime("%Y-%m-%d"),
            "ocupacion": self.ocupacion_var.get().strip(),
            "estado_civil": self.estado_civil_var.get().strip(),
            "fecha_nacimiento": self.fecha_nac_var.get().strip(),
            "acudiente_apellido1": self.acu_a1.get().strip(),
            "acudiente_apellido2": self.acu_a2.get().strip(),
            "acudiente_nombre": self.acu_nom.get().strip(),
            "acudiente_direccion": self.acu_dir.get().strip(),
            "acudiente_telefono": self.acu_tel.get().strip(),
            "acudiente_parentesco": self.acu_par.get().strip(),
            "antecedentes_personales": texto(self.ant_pers),
            "antecedentes_familiares": texto(self.ant_fam),
            "motivo_consulta": texto(self.motivo),
            "cepillado": self.cepillado_var.get().strip(),
            "seda": self.seda_var.get().strip(),
            "enjuague": self.enjuague_var.get().strip(),
            "examen_oral": examen,
            "odontograma": self.odontograma.get_estados(),
            "diagnostico_tejido_blando": texto(self.dx_blando),
            "diagnostico_dental": texto(self.dx_dental),
            "diagnostico_periodontal": texto(self.dx_perio),
            "diagnostico_craneofacial": texto(self.dx_craneo),
            "diagnostico_oclusion": texto(self.dx_oclusion),
        }