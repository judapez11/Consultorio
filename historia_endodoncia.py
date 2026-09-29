import datetime as dt
import math
import tkinter as tk
from tkinter import ttk

from campo_fecha import CampoFecha

ANTECEDENTES = [
    ("grupo_sanguineo", "Grupo sanguineo"), ("alergias", "Alergias"),
    ("cardiopatias", "Cardiopatias"), ("embarazo", "Embarazo"),
    ("presion_arterial", "Presion arterial"), ("tto_medico", "Tto. medico actual"),
    ("fuegos_herpes", "Fuegos / herpes labial"), ("hepatitis", "Hepatitis"),
    ("diabetes", "Diabetes"), ("fiebre_reumatica", "Fiebre reumatica"),
    ("hiv", "HIV"), ("inmunosupresion", "Inmunosupresion"),
    ("enf_renal", "Enf. renal"), ("enf_respiratoria", "Enf. respiratoria"),
    ("anestesia_local", "Ha recibido anestesia local"),
    ("trastornos_gastricos", "Trastornos gastricos"),
    ("trastornos_emocionales", "Trastornos emocionales"),
    ("sinusitis", "Sinusitis"), ("cirugias", "Cirugias en general"),
    ("exodoncias", "Exodoncias"), ("enf_orales", "Enf. orales"),
    ("protesis", "Protesis"), ("reaccion_anestesia", "Reaccion adversa a la anestesia"),
]

EXAMEN_CLINICO = [
    ("inflamacion_intraoral", "Inflamacion intraoral"),
    ("inflamacion_extraoral", "Inflamacion extraoral"),
    ("grado_movilidad", "Grado de movilidad"),
    ("test_percusion", "Test de percusion"),
    ("test_palpacion", "Test de palpacion"),
    ("cambio_color", "Cambio de color"),
    ("trauma_oclusal", "Trauma oclusal"),
    ("oclusion_traumatica", "Oclusion traumatica"),
    ("fistula_activa", "Fistula activa"),
    ("bolsa_periodontal", "Bolsa periodontal"),
    ("restauracion", "Restauracion"),
]

EXAMEN_RADIOGRAFICO = [
    ("lesion_furca", "Grado de lesion de furca"), ("lesion_apical", "Lesion apical"),
    ("lesion_lateral", "Lesion lateral"), ("reabsorcion", "Reabsorcion radicular"),
    ("dilaceracion", "Dilaceracion radicular"),
    ("proporcion_corona", "Proporcion corona/raiz"),
    ("perdida_osea_v", "Perdida osea vertical"),
    ("perdida_osea_h", "Perdida osea horizontal"),
    ("retenedor", "Retenedor intra radicular"), ("apice_abierto", "Apice abierto"),
    ("perforacion", "Perforacion"),
]

DOLOR = [
    ("leve_moderado", "Leve/moderado"), ("moderado_severo", "Moderado/severo"),
    ("continuo", "Continuo"), ("intermitente", "Intermitente"),
    ("pulsatil", "Pulsatil"), ("masticacion", "Masticacion/oclusion"),
    ("palpacion", "Palpacion"), ("percusion", "Percusion"),
    ("frio", "Frio"), ("calor", "Calor"), ("dulce", "Dulce"),
]

CONDUCTO_COLUMNAS = ["Long. tentativa", "Long. definitiva", "Referencia",
                     "Lima apical", "Sistema de preparacion"]
CONDUCTO_CLAVES = ["long_tentativa", "long_definitiva", "referencia",
                   "lima_apical", "sistema_preparacion"]
CONDUCTO_FILAS = 4


class CanvasChecks(ttk.Frame):
    """Lista de casillas dibujadas en canvas (rapido, sin widgets por item)."""

    def __init__(self, master, etiquetas, columnas=3, alto_item=26):
        super().__init__(master)
        self._etiquetas = etiquetas
        self._columnas = columnas
        self._alto_item = alto_item
        self._estados = {clave: False for clave, _ in etiquetas}
        self.canvas = tk.Canvas(self, height=40, highlightthickness=0,
                                cursor="hand2")
        self.canvas.pack(fill="x")
        self.canvas.bind("<Configure>", self._dibujar)

    def _dibujar(self, event=None):
        ancho = event.width if event and event.width > 50 else self.canvas.winfo_width()
        if ancho < 50:
            return
        c = self.canvas
        c.delete("all")
        filas = math.ceil(len(self._etiquetas) / self._columnas)
        c.config(height=filas * self._alto_item + 6)
        for i, (clave, etiqueta) in enumerate(self._etiquetas):
            fila, col = divmod(i, self._columnas)
            x = 6 + col * (ancho / self._columnas)
            y = 4 + fila * self._alto_item
            marca = "☑" if self._estados[clave] else "☐"
            tag = f"chk_{clave}"
            c.create_text(x, y, text=f"{marca} {etiqueta}",
                          font=("DejaVu Sans", 11), fill="#222222",
                          anchor="w", tags=(tag,))
            c.tag_bind(tag, "<Button-1>",
                       lambda e, k=clave: self._toggle(k))

    def _toggle(self, clave):
        self._estados[clave] = not self._estados[clave]
        self._dibujar()

    def get_estados(self):
        return dict(self._estados)

    def set_estados(self, estados):
        for clave in self._estados:
            self._estados[clave] = bool((estados or {}).get(clave))
        self._dibujar()


class HistoriaEndodonciaForm(ttk.Frame):
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
        self.referido_var = tk.StringVar()
        self.eps_var = tk.StringVar()

        ttk.Label(cuadro, text="Fecha").grid(row=0, column=0, sticky="w", pady=3)
        self.fecha_entry.grid(row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Nombre y apellido").grid(row=0, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.nombre_var).grid(
            row=0, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Identificacion").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.identificacion_var).grid(
            row=1, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Edad (anos)").grid(row=1, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.edad_var).grid(
            row=1, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Direccion").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.direccion_var).grid(
            row=2, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="Telefono").grid(row=2, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.telefono_var).grid(
            row=2, column=3, sticky="we", padx=6)
        ttk.Label(cuadro, text="Referido por").grid(row=3, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro, textvariable=self.referido_var).grid(
            row=3, column=1, sticky="we", padx=6)
        ttk.Label(cuadro, text="E.P.S.").grid(row=3, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro, textvariable=self.eps_var).grid(
            row=3, column=3, sticky="we", padx=6)
        for c in (1, 3):
            cuadro.columnconfigure(c, weight=1)

        cuadro2 = ttk.LabelFrame(self, text="Motivo de la consulta", padding=10)
        cuadro2.pack(fill="x", pady=(8, 0))
        self.motivo = tk.Text(cuadro2, width=60, height=3)
        self.motivo.pack(fill="x")

        cuadro3 = ttk.LabelFrame(self, text="Antecedentes", padding=10)
        cuadro3.pack(fill="x", pady=(8, 0))
        self.antecedentes = CanvasChecks(cuadro3, ANTECEDENTES, columnas=3)
        self.antecedentes.pack(fill="x")

        cuadro4 = ttk.LabelFrame(self, text="Signos vitales", padding=10)
        cuadro4.pack(fill="x", pady=(8, 0))
        self.pa_var = tk.StringVar()
        self.fr_var = tk.StringVar()
        self.fc_var = tk.StringVar()
        ttk.Label(cuadro4, text="P.A (mm Hg)").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro4, textvariable=self.pa_var).grid(row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro4, text="F.R (x min)").grid(row=0, column=2, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro4, textvariable=self.fr_var).grid(row=0, column=3, sticky="we", padx=6)
        ttk.Label(cuadro4, text="F.C (pul/min)").grid(row=0, column=4, sticky="w", pady=3, padx=(12, 0))
        ttk.Entry(cuadro4, textvariable=self.fc_var).grid(row=0, column=5, sticky="we", padx=6)
        for c in (1, 3, 5):
            cuadro4.columnconfigure(c, weight=1)

        cuadro5 = ttk.LabelFrame(self, text="Observaciones", padding=10)
        cuadro5.pack(fill="x", pady=(8, 0))
        self.observaciones = tk.Text(cuadro5, width=60, height=3)
        self.observaciones.pack(fill="x")

        cuadro6 = ttk.LabelFrame(self, text="Antecedentes medico-familiares", padding=10)
        cuadro6.pack(fill="x", pady=(8, 0))
        self.ant_fam = tk.Text(cuadro6, width=60, height=3)
        self.ant_fam.pack(fill="x")

        cuadro7 = ttk.LabelFrame(self, text="Diente por tratar", padding=10)
        cuadro7.pack(fill="x", pady=(8, 0))
        self.diente_var = tk.StringVar()
        ttk.Entry(cuadro7, textvariable=self.diente_var).pack(fill="x")

        cuadro8 = ttk.LabelFrame(self, text="Examen clinico", padding=10)
        cuadro8.pack(fill="x", pady=(8, 0))
        self.examen_clinico = CanvasChecks(cuadro8, EXAMEN_CLINICO, columnas=3)
        self.examen_clinico.pack(fill="x")

        cuadro9 = ttk.LabelFrame(self, text="Examen radiografico", padding=10)
        cuadro9.pack(fill="x", pady=(8, 0))
        self.examen_radio = CanvasChecks(cuadro9, EXAMEN_RADIOGRAFICO, columnas=3)
        self.examen_radio.pack(fill="x")

        cuadro10 = ttk.LabelFrame(self, text="Dolor", padding=10)
        cuadro10.pack(fill="x", pady=(8, 0))
        self.dolor = CanvasChecks(cuadro10, DOLOR, columnas=3)
        self.dolor.pack(fill="x")

        cuadro11 = ttk.LabelFrame(self, text="Diagnostico / Pronostico / Plan de tratamiento",
                                  padding=10)
        cuadro11.pack(fill="x", pady=(8, 0))
        self.diagnostico = tk.Text(cuadro11, width=60, height=2)
        self.diagnostico.pack(fill="x", pady=(0, 4))
        self.pronostico = tk.Text(cuadro11, width=60, height=2)
        self.pronostico.pack(fill="x", pady=(0, 4))
        self.plan = tk.Text(cuadro11, width=60, height=2)
        self.plan.pack(fill="x")

        cuadro12 = ttk.LabelFrame(self, text="Conductos", padding=10)
        cuadro12.pack(fill="x", pady=(8, 0))
        for c, etiqueta in enumerate(CONDUCTO_COLUMNAS):
            ttk.Label(cuadro12, text=etiqueta, font=("Segoe UI", 9, "bold")).grid(
                row=0, column=c, padx=4, pady=2)
            cuadro12.columnconfigure(c, weight=1)
        self.conducto_vars = []
        for fila in range(CONDUCTO_FILAS):
            vars_fila = {}
            for c, clave in enumerate(CONDUCTO_CLAVES):
                var = tk.StringVar()
                ttk.Entry(cuadro12, textvariable=var).grid(
                    row=fila + 1, column=c, sticky="we", padx=4, pady=2)
                vars_fila[clave] = var
            self.conducto_vars.append(vars_fila)

        cuadro13 = ttk.LabelFrame(self, text="Observaciones finales", padding=10)
        cuadro13.pack(fill="x", pady=(8, 0))
        self.obs_finales = tk.Text(cuadro13, width=60, height=3)
        self.obs_finales.pack(fill="x")

        cuadro14 = ttk.LabelFrame(self, text="Firmas", padding=10)
        cuadro14.pack(fill="x", pady=(8, 0))
        self.firma_pac_var = tk.StringVar()
        self.firma_endo_var = tk.StringVar()
        ttk.Label(cuadro14, text="Firma del paciente").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro14, textvariable=self.firma_pac_var).grid(
            row=0, column=1, sticky="we", padx=6)
        ttk.Label(cuadro14, text="Firma del endodoncista").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(cuadro14, textvariable=self.firma_endo_var).grid(
            row=1, column=1, sticky="we", padx=6)
        cuadro14.columnconfigure(1, weight=1)

    def prefill_nombre(self, nombre):
        if nombre and not self.nombre_var.get().strip():
            self.nombre_var.set(nombre)

    def limpiar(self):
        self.fecha_entry.set_date(dt.date.today())
        for var in (self.nombre_var, self.identificacion_var, self.edad_var,
                    self.direccion_var, self.telefono_var, self.referido_var,
                    self.eps_var, self.pa_var, self.fr_var, self.fc_var,
                    self.diente_var, self.firma_pac_var, self.firma_endo_var):
            var.set("")
        for t in (self.motivo, self.observaciones, self.ant_fam,
                  self.diagnostico, self.pronostico, self.plan,
                  self.obs_finales):
            t.delete("1.0", "end")
        for checks in (self.antecedentes, self.examen_clinico,
                       self.examen_radio, self.dolor):
            checks.set_estados({})
        for vars_fila in self.conducto_vars:
            for var in vars_fila.values():
                var.set("")

    def cargar(self, datos):
        self.limpiar()
        from datetime import datetime
        try:
            self.fecha_entry.set_date(datetime.strptime(datos["fecha"], "%Y-%m-%d").date())
        except (ValueError, KeyError):
            pass
        for var, clave in ((self.nombre_var, "nombre"),
                           (self.identificacion_var, "identificacion"),
                           (self.edad_var, "edad"), (self.direccion_var, "direccion"),
                           (self.telefono_var, "telefono"),
                           (self.referido_var, "referido_por"),
                           (self.eps_var, "eps"), (self.pa_var, "pa"),
                           (self.fr_var, "fr"), (self.fc_var, "fc"),
                           (self.diente_var, "diente_tratar"),
                           (self.firma_pac_var, "firma_paciente"),
                           (self.firma_endo_var, "firma_endodoncista")):
            var.set(datos.get(clave, "") or "")
        for t, clave in ((self.motivo, "motivo_consulta"),
                         (self.observaciones, "observaciones"),
                         (self.ant_fam, "antecedentes_familiares"),
                         (self.diagnostico, "diagnostico"),
                         (self.pronostico, "pronostico"),
                         (self.plan, "plan_tratamiento"),
                         (self.obs_finales, "observaciones_finales")):
            valor = datos.get(clave, "") or ""
            if valor:
                t.insert("1.0", valor)
        self.antecedentes.set_estados(datos.get("antecedentes") or {})
        self.examen_clinico.set_estados(datos.get("examen_clinico") or {})
        self.examen_radio.set_estados(datos.get("examen_radiografico") or {})
        self.dolor.set_estados(datos.get("dolor") or {})
        conductos = datos.get("conductos") or []
        for fila, vars_fila in enumerate(self.conducto_vars):
            fila_datos = conductos[fila] if fila < len(conductos) else {}
            for clave, var in vars_fila.items():
                var.set(fila_datos.get(clave, "") or "")

    def validar(self):
        faltan = []
        if self.fecha_entry.get_date() is None:
            faltan.append("Fecha invalida (dd/mm/yyyy)")
        if not self.motivo.get("1.0", "end").strip():
            faltan.append("Motivo de la consulta")
        if not self.diente_var.get().strip():
            faltan.append("Diente por tratar")
        return faltan

    def tiene_contenido(self):
        for var in (self.nombre_var, self.identificacion_var, self.edad_var,
                    self.direccion_var, self.telefono_var, self.referido_var,
                    self.eps_var, self.pa_var, self.fr_var, self.fc_var,
                    self.diente_var, self.firma_pac_var, self.firma_endo_var):
            if var.get().strip():
                return True
        for t in (self.motivo, self.observaciones, self.ant_fam,
                  self.diagnostico, self.pronostico, self.plan,
                  self.obs_finales):
            if t.get("1.0", "end").strip():
                return True
        for checks in (self.antecedentes, self.examen_clinico,
                       self.examen_radio, self.dolor):
            if any(checks.get_estados().values()):
                return True
        for vars_fila in self.conducto_vars:
            for var in vars_fila.values():
                if var.get().strip():
                    return True
        return False

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
            "referido_por": self.referido_var.get().strip(),
            "eps": self.eps_var.get().strip(),
            "motivo_consulta": texto(self.motivo),
            "antecedentes": self.antecedentes.get_estados(),
            "pa": self.pa_var.get().strip(),
            "fr": self.fr_var.get().strip(),
            "fc": self.fc_var.get().strip(),
            "observaciones": texto(self.observaciones),
            "antecedentes_familiares": texto(self.ant_fam),
            "diente_tratar": self.diente_var.get().strip(),
            "examen_clinico": self.examen_clinico.get_estados(),
            "examen_radiografico": self.examen_radio.get_estados(),
            "dolor": self.dolor.get_estados(),
            "diagnostico": texto(self.diagnostico),
            "pronostico": texto(self.pronostico),
            "plan_tratamiento": texto(self.plan),
            "conductos": [{clave: var.get().strip()
                           for clave, var in vars_fila.items()}
                          for vars_fila in self.conducto_vars],
            "observaciones_finales": texto(self.obs_finales),
            "firma_paciente": self.firma_pac_var.get().strip(),
            "firma_endodoncista": self.firma_endo_var.get().strip(),
        }