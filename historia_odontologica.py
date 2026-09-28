import datetime as dt
import tkinter as tk
from tkinter import ttk

from campo_fecha import CampoFecha

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

        self.fecha_entry = CampoFecha(cuadro)
        self.fecha_entry.set_date(dt.date.today())
        self.ocupacion_var = tk.StringVar()
        self.estado_civil_var = tk.StringVar()
        self.fecha_nac_var = tk.StringVar()

        ttk.Label(cuadro, text="Fecha de consulta").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Ocupacion").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.ocupacion_var).grid(
            row=1, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Estado civil").grid(row=1, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.estado_civil_var).grid(
            row=1, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Fecha de nacimiento").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.fecha_nac_var).grid(
            row=2, column=1, sticky="we", padx=6)

        self.es_menor_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            cuadro, text="¿Es menor de edad?", variable=self.es_menor_var,
            font=("Segoe UI", 11, "bold"), command=self._toggle_acudiente,
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))

        self.acudiente = ttk.LabelFrame(self, text="Acudiente", padding=10)
        self.acu_a1 = tk.StringVar()
        self.acu_a2 = tk.StringVar()
        self.acu_nom = tk.StringVar()
        self.acu_dir = tk.StringVar()
        self.acu_tel = tk.StringVar()
        self.acu_par = tk.StringVar()

        ttk.Label(self.acudiente, text="Primer apellido").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(self.acudiente, textvariable=self.acu_a1).grid(row=0, column=1, sticky="we", padx=6)
        ttk.Label(self.acudiente, text="Segundo apellido").grid(row=0, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(self.acudiente, textvariable=self.acu_a2).grid(row=0, column=3, sticky="we", padx=6)
        ttk.Label(self.acudiente, text="Nombre").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(self.acudiente, textvariable=self.acu_nom).grid(row=1, column=1, sticky="we", padx=6)
        ttk.Label(self.acudiente, text="Parentesco").grid(row=1, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(self.acudiente, textvariable=self.acu_par).grid(row=1, column=3, sticky="we", padx=6)
        ttk.Label(self.acudiente, text="Direccion").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(self.acudiente, textvariable=self.acu_dir).grid(row=2, column=1, sticky="we", padx=6)
        ttk.Label(self.acudiente, text="Telefono").grid(row=2, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(self.acudiente, textvariable=self.acu_tel).grid(row=2, column=3, sticky="we", padx=6)
        self.acudiente.columnconfigure(1, weight=1)
        self.acudiente.columnconfigure(3, weight=1)

        cuadro.columnconfigure(1, weight=1)
        cuadro.columnconfigure(3, weight=1)

        cuadro2 = ttk.LabelFrame(self, text="2. Anamnesis", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self._anamnesis = cuadro2
        self.ant_pers = self._campo_texto(cuadro2, "Antecedentes medicos personales", 0)
        self.ant_fam = self._campo_texto(cuadro2, "Antecedentes medicos familiares", 1)
        self.motivo = self._campo_texto(cuadro2, "Motivo de la consulta", 2)

        cuadro3 = ttk.LabelFrame(self, text="3. Habitos", padding=10)
        cuadro3.pack(fill="x", pady=(8, 0))
        self.cepillado_var = tk.StringVar()
        self.seda_var = tk.StringVar()
        self.enjuague_var = tk.StringVar()
        ttk.Label(cuadro3, text="Cepillado").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro3, textvariable=self.cepillado_var).grid(
            row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro3, text="Uso de seda dental").grid(row=0, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro3, textvariable=self.seda_var).grid(
            row=0, column=3, sticky="we", padx=6)
        ttk.Label(cuadro3, text="Uso de enjuague").grid(row=0, column=4, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro3, textvariable=self.enjuague_var).grid(
            row=0, column=5, sticky="we", padx=6)
        for c in (1, 3, 5):
            cuadro3.columnconfigure(c, weight=1)

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

    def _toggle_acudiente(self):
        if self.es_menor_var.get():
            self.acudiente.pack(fill="x", pady=(8, 0), before=self._anamnesis)
        else:
            self.acudiente.pack_forget()

    def limpiar(self):
        self.es_menor_var.set(False)
        self._toggle_acudiente()
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
        es_menor = any(var.get().strip() for var in
                       (self.acu_a1, self.acu_a2, self.acu_nom, self.acu_dir,
                        self.acu_tel, self.acu_par))
        self.es_menor_var.set(es_menor)
        self._toggle_acudiente()

    def validar(self):
        faltan = []
        if self.fecha_entry.get_date() is None:
            faltan.append("Fecha de consulta invalida (dd/mm/yyyy)")
        if self.es_menor_var.get():
            campos = [
                ("Primer apellido del acudiente", self.acu_a1),
                ("Nombre del acudiente", self.acu_nom),
                ("Parentesco", self.acu_par),
                ("Direccion del acudiente", self.acu_dir),
                ("Telefono del acudiente", self.acu_tel),
            ]
            for etiqueta, var in campos:
                if not var.get().strip():
                    faltan.append(etiqueta)
        return faltan

    def datos(self):
        def texto(t):
            return t.get("1.0", "end").strip()

        examen = {item: var.get() for item, var in self.examen_vars.items()}
        fecha = self.fecha_entry.get_date()
        return {
            "fecha": fecha.strftime("%Y-%m-%d") if fecha else "",
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