import datetime as dt
import tkinter as tk
from tkinter import ttk

from campo_fecha import CampoFecha

ANTECEDENTES = [
    ("ant_quirurgicos", "Quirurgicos"),
    ("ant_patologicos", "Patologicos"),
    ("ant_toxicoalergicos", "Toxicoalergicos"),
    ("ant_transfusionales", "Transfusionales"),
    ("ant_traumaticos", "Traumaticos"),
    ("ant_otros", "Otros"),
]


class HistoriaUrgenciaForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._build()

    def _build(self):
        cuadro = ttk.LabelFrame(self, text="Datos del paciente", padding=10)
        cuadro.pack(fill="x")

        self.fecha_entry = CampoFecha(cuadro)
        self.fecha_entry.set_date(dt.date.today())
        self.nombre_var = tk.StringVar()
        self.identificacion_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.acudiente_var = tk.StringVar()

        ttk.Label(cuadro, text="Fecha").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Nombre y apellidos").grid(row=0, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.nombre_var).grid(
            row=0, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Identificacion").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.identificacion_var).grid(
            row=1, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Edad").grid(row=1, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.edad_var).grid(
            row=1, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Direccion").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.direccion_var).grid(
            row=2, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Telefono").grid(row=2, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.telefono_var).grid(
            row=2, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Nombre del acudiente (si es menor de edad)").grid(
            row=3, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.acudiente_var).grid(
            row=3, column=1, sticky="we", padx=6)

        for c in (1, 3):
            cuadro.columnconfigure(c, weight=1)

        cuadro2 = ttk.LabelFrame(self, text="Motivo de la consulta", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self.motivo = self._campo_texto(cuadro2)

        cuadro3 = ttk.LabelFrame(self, text="Antecedentes personales", padding=10)
        cuadro3.pack(fill="x", pady=(8, 0))
        self.ant_vars = {}
        for i, (clave, etiqueta) in enumerate(ANTECEDENTES):
            var = tk.BooleanVar(value=False)
            self.ant_vars[clave] = var
            tk.Checkbutton(
                cuadro3, text=etiqueta, variable=var,
                font=("Segoe UI", 11),
            ).grid(row=i // 3, column=i % 3, sticky="w", padx=6, pady=3)
        for c in range(3):
            cuadro3.columnconfigure(c, weight=1)

        cuadro4 = ttk.LabelFrame(self, text="Antecedentes familiares", padding=10)
        cuadro4.pack(fill="x", pady=(8, 0))
        self.ant_fam = self._campo_texto(cuadro4)

        cuadro5 = ttk.LabelFrame(self, text="Examen fisico", padding=10)
        cuadro5.pack(fill="x", pady=(8, 0))
        self.examen_fisico = self._campo_texto(cuadro5)

        cuadro6 = ttk.LabelFrame(self, text="Examen radiologico", padding=10)
        cuadro6.pack(fill="x", pady=(8, 0))
        self.examen_radio = self._campo_texto(cuadro6)

        cuadro7 = ttk.LabelFrame(self, text="Impresion diagnostica", padding=10)
        cuadro7.pack(fill="x", pady=(8, 0))
        self.impresion = self._campo_texto(cuadro7)

        cuadro8 = ttk.LabelFrame(self, text="Plan de tratamiento", padding=10)
        cuadro8.pack(fill="x", pady=(8, 0))
        self.plan = self._campo_texto(cuadro8)

        cuadro9 = ttk.LabelFrame(self, text="Firmas", padding=10)
        cuadro9.pack(fill="x", pady=(8, 0))
        self.firma_pac_var = tk.StringVar()
        self.cc_pac_var = tk.StringVar()
        self.firma_odo_var = tk.StringVar()
        self.cc_odo_var = tk.StringVar()
        ttk.Label(cuadro9, text="Firma del paciente").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro9, textvariable=self.firma_pac_var).grid(
            row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro9, text="CC").grid(row=0, column=2, sticky="w", padx=(12, 0))
        ttk.Entry(cuadro9, textvariable=self.cc_pac_var).grid(
            row=0, column=3, sticky="we", padx=6)
        ttk.Label(cuadro9, text="Firma del odontologo").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro9, textvariable=self.firma_odo_var).grid(
            row=1, column=1, sticky="we", padx=6)
        ttk.Label(cuadro9, text="CC").grid(row=1, column=2, sticky="w", padx=(12, 0))
        ttk.Entry(cuadro9, textvariable=self.cc_odo_var).grid(
            row=1, column=3, sticky="we", padx=6)
        for c in (1, 3):
            cuadro9.columnconfigure(c, weight=1)

    def _campo_texto(self, padre):
        texto = tk.Text(padre, width=60, height=3)
        texto.pack(fill="x")
        return texto

    def prefill_nombre(self, nombre):
        if nombre and not self.nombre_var.get().strip():
            self.nombre_var.set(nombre)

    def limpiar(self):
        from datetime import date
        self.nombre_var.set("")
        self.identificacion_var.set("")
        self.edad_var.set("")
        self.direccion_var.set("")
        self.telefono_var.set("")
        self.acudiente_var.set("")
        for var in self.ant_vars.values():
            var.set(False)
        for texto in (
            self.motivo, self.ant_fam, self.examen_fisico, self.examen_radio,
            self.impresion, self.plan,
        ):
            texto.delete("1.0", "end")
        self.firma_pac_var.set("")
        self.cc_pac_var.set("")
        self.firma_odo_var.set("")
        self.cc_odo_var.set("")
        self.fecha_entry.set_date(date.today())

    def cargar(self, datos):
        self.limpiar()
        from datetime import datetime
        try:
            self.fecha_entry.set_date(datetime.strptime(datos["fecha"], "%Y-%m-%d").date())
        except (ValueError, KeyError):
            pass
        mapeos = {
            "nombre": self.nombre_var, "identificacion": self.identificacion_var,
            "edad": self.edad_var, "direccion": self.direccion_var,
            "telefono": self.telefono_var, "acudiente": self.acudiente_var,
            "firma_paciente": self.firma_pac_var, "cc_paciente": self.cc_pac_var,
            "firma_odontologo": self.firma_odo_var, "cc_odontologo": self.cc_odo_var,
        }
        for clave, var in mapeos.items():
            var.set(datos.get(clave, "") or "")
        for clave, var in self.ant_vars.items():
            var.set(bool(datos.get(clave, 0)))
        textos = {
            "motivo_consulta": self.motivo,
            "antecedentes_familiares": self.ant_fam,
            "examen_fisico": self.examen_fisico,
            "examen_radiologico": self.examen_radio,
            "impresion_diagnostica": self.impresion,
            "plan_tratamiento": self.plan,
        }
        for clave, texto in textos.items():
            valor = datos.get(clave, "") or ""
            if valor:
                texto.insert("1.0", valor)

    def tiene_contenido(self):
        for var in (self.nombre_var, self.identificacion_var, self.edad_var,
                    self.direccion_var, self.telefono_var, self.acudiente_var,
                    self.firma_pac_var, self.cc_pac_var,
                    self.firma_odo_var, self.cc_odo_var):
            if var.get().strip():
                return True
        if any(v.get() for v in self.ant_vars.values()):
            return True
        for t in (self.motivo, self.ant_fam, self.examen_fisico, self.examen_radio,
                  self.impresion, self.plan):
            if t.get("1.0", "end").strip():
                return True
        return False

    def validar(self):
        faltan = []
        if self.fecha_entry.get_date() is None:
            faltan.append("Fecha invalida (dd/mm/yyyy)")
        if not self.motivo.get("1.0", "end").strip():
            faltan.append("Motivo de la consulta")
        return faltan

    def datos(self):
        def texto(t):
            return t.get("1.0", "end").strip()

        fecha = self.fecha_entry.get_date()
        return {
            "fecha": fecha.strftime("%Y-%m-%d") if fecha else "",
            "nombre": self.nombre_var.get().strip(),
            "identificacion": self.identificacion_var.get().strip(),
            "edad": self.edad_var.get().strip(),
            "direccion": self.direccion_var.get().strip(),
            "telefono": self.telefono_var.get().strip(),
            "acudiente": self.acudiente_var.get().strip(),
            "motivo_consulta": texto(self.motivo),
            "ant_quirurgicos": int(self.ant_vars["ant_quirurgicos"].get()),
            "ant_patologicos": int(self.ant_vars["ant_patologicos"].get()),
            "ant_toxicoalergicos": int(self.ant_vars["ant_toxicoalergicos"].get()),
            "ant_transfusionales": int(self.ant_vars["ant_transfusionales"].get()),
            "ant_traumaticos": int(self.ant_vars["ant_traumaticos"].get()),
            "ant_otros": int(self.ant_vars["ant_otros"].get()),
            "antecedentes_familiares": texto(self.ant_fam),
            "examen_fisico": texto(self.examen_fisico),
            "examen_radiologico": texto(self.examen_radio),
            "impresion_diagnostica": texto(self.impresion),
            "plan_tratamiento": texto(self.plan),
            "firma_paciente": self.firma_pac_var.get().strip(),
            "cc_paciente": self.cc_pac_var.get().strip(),
            "firma_odontologo": self.firma_odo_var.get().strip(),
            "cc_odontologo": self.cc_odo_var.get().strip(),
        }