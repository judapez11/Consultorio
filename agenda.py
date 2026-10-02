import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox

from tkcalendar import Calendar

from db import (
    listar_citas,
    guardar_cita,
    actualizar_cita,
    actualizar_estado_cita,
    borrar_cita,
    hora_ocupada,
    listar_pacientes,
)

HORAS = [f"{h:02d}:{m:02d}" for h in range(8, 19) for m in (0, 30)]


class AgendaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._selected_id = None
        self._fecha_actual = None
        self._build()

    def _build(self):
        self.style = ttk.Style(self)
        self.style.configure("Treeview", rowheight=28)

        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        cal_frame = ttk.LabelFrame(contenedor, text="Calendario", padding=10)
        cal_frame.pack(side="left", fill="y", padx=(0, 10))

        self.cal = Calendar(
            cal_frame,
            selectmode="day",
            firstweekday="monday",
            locale="es_ES",
            date_pattern="dd/mm/yyyy",
            font=("Segoe UI", 13),
        )
        self.cal.pack()
        self.cal.tag_config("cita_pendiente", background="#cfe8ff")
        self.cal.tag_config("cita_realizada", background="#c6efce")
        self.cal.tag_config("cita_cancelada", background="#f2c6c6")
        self.cal.bind("<<CalendarSelected>>", lambda e: self._mostrar_dia())

        derecha = ttk.Frame(contenedor)
        derecha.pack(side="left", fill="both", expand=True)

        self.dia_label = ttk.Label(derecha, text="", font=("Segoe UI", 12, "bold"))
        self.dia_label.pack(anchor="w")

        self.tree = ttk.Treeview(
            derecha, columns=("id", "hora", "paciente", "motivo", "estado"),
            show="headings", selectmode="browse",
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("motivo", text="Motivo")
        self.tree.heading("estado", text="Estado")
        self.tree.column("id", width=60, stretch=False)
        self.tree.column("hora", width=80, stretch=False)
        self.tree.column("paciente", width=150)
        self.tree.column("motivo", width=170)
        self.tree.column("estado", width=100, stretch=False)
        scroll = ttk.Scrollbar(derecha, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(fill="both", expand=True, pady=6)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar)

        botones = ttk.Frame(derecha)
        botones.pack(fill="x")
        ttk.Button(botones, text="+ Agregar cita", command=self.agregar).pack(side="left")
        ttk.Button(botones, text="Editar", command=self.editar).pack(side="left", padx=8)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left")
        ttk.Button(botones, text="Marcar realizada",
                   command=lambda: self._marcar_estado("realizada")).pack(side="left", padx=(16, 0))
        ttk.Button(botones, text="Marcar cancelada",
                   command=lambda: self._marcar_estado("cancelada")).pack(side="left", padx=4)
        ttk.Button(botones, text="Pendiente",
                   command=lambda: self._marcar_estado("pendiente")).pack(side="left", padx=4)

        self.refrescar_calendario()
        self.cal.selection_set(dt.date.today())
        self._mostrar_dia()

    def refrescar_calendario(self):
        self.cal.calevent_remove("all")
        for c in listar_citas():
            fecha = dt.datetime.strptime(c["fecha"], "%Y-%m-%d").date()
            tag = f"cita_{c['estado']}" if c["estado"] in (
                "pendiente", "realizada", "cancelada") else "cita_pendiente"
            self.cal.calevent_create(fecha, f"{c['hora']} - {c['paciente_nombre']}", tag)

    def _mostrar_dia(self):
        fecha = self.cal.selection_get()
        if fecha is None:
            return
        self._fecha_actual = fecha.strftime("%Y-%m-%d")
        self.dia_label.config(text="Día: " + fecha.strftime("%A, %d/%m/%Y").capitalize())
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in listar_citas(self._fecha_actual):
            self.tree.insert("", "end", iid=str(c["id"]),
                             values=(c["id"], c["hora"], c["paciente_nombre"],
                                     c["motivo"], c["estado"]))

    def _marcar_estado(self, estado):
        if self._selected_id is None:
            messagebox.showinfo("Aviso", "Selecciona una cita de la lista.")
            return
        actualizar_estado_cita(self._selected_id, estado)
        self.refrescar_calendario()
        self._mostrar_dia()

    def _seleccionar(self, event):
        sel = self.tree.selection()
        self._selected_id = int(sel[0]) if sel else None

    def _elegir_paciente(self, ventana, inicial=None):
        pacientes = listar_pacientes()
        nombres = [p["nombre"] for p in pacientes]
        combo = ttk.Combobox(ventana, values=nombres, state="readonly")
        if inicial:
            for p in pacientes:
                if p["id"] == inicial:
                    combo.set(p["nombre"])
        return combo, pacientes

    def _ventana_cita(self, titulo, datos=None):
        if not listar_pacientes():
            messagebox.showwarning(
                "Sin pacientes", "Registra primero un paciente en la pestaña Pacientes."
            )
            return None

        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.grab_set()
        ventana.transient(self.winfo_toplevel())

        f = ttk.Frame(ventana, padding=15)
        f.pack(fill="both", expand=True)

        ttk.Label(f, text="Paciente").grid(row=0, column=0, sticky="w", pady=4)
        combo_pac, pacientes = self._elegir_paciente(f, (datos or {}).get("paciente_id"))
        combo_pac.grid(row=0, column=1, sticky="we", padx=6, pady=4)

        ttk.Label(f, text="Hora").grid(row=1, column=0, sticky="w", pady=4)
        combo_hora = ttk.Combobox(f, values=HORAS, state="readonly", width=10)
        if datos:
            combo_hora.set(datos["hora"])
        else:
            combo_hora.set("08:00")
        combo_hora.grid(row=1, column=1, sticky="w", padx=6, pady=4)

        ttk.Label(f, text="Motivo").grid(row=2, column=0, sticky="w", pady=4)
        motivo_var = tk.StringVar(value=(datos or {}).get("motivo") or "")
        ttk.Entry(f, textvariable=motivo_var, width=35).grid(
            row=2, column=1, sticky="we", padx=6, pady=4
        )
        f.columnconfigure(1, weight=1)

        return ventana, combo_pac, pacientes, combo_hora, motivo_var

    def agregar(self):
        resultado = self._ventana_cita("Agendar cita")
        if not resultado:
            return
        ventana, combo_pac, pacientes, combo_hora, motivo_var = resultado

        def guardar():
            if not combo_pac.get():
                messagebox.showwarning("Dato requerido", "Selecciona un paciente.")
                return
            hora = combo_hora.get()
            if hora_ocupada(self._fecha_actual, hora):
                messagebox.showwarning(
                    "Hora ocupada", f"Ya hay una cita a las {hora} ese día."
                )
                return
            pid = pacientes[[p["nombre"] for p in pacientes].index(combo_pac.get())]["id"]
            guardar_cita(pid, self._fecha_actual, hora, motivo_var.get().strip())
            ventana.destroy()
            self.refrescar_calendario()
            self._mostrar_dia()

        ttk.Button(f := ventana.winfo_children()[0], text="Guardar",
                   command=guardar).grid(row=3, column=0, columnspan=2, pady=(10, 0))

    def editar(self):
        if self._selected_id is None or not self._fecha_actual:
            messagebox.showinfo("Aviso", "Selecciona una cita de la lista.")
            return
        citas = listar_citas(self._fecha_actual)
        cita = next((c for c in citas if c["id"] == self._selected_id), None)
        if not cita:
            return
        resultado = self._ventana_cita("Editar cita", dict(cita))
        if not resultado:
            return
        ventana, combo_pac, pacientes, combo_hora, motivo_var = resultado

        def guardar():
            hora = combo_hora.get()
            if hora_ocupada(self._fecha_actual, hora, excluir_id=cita["id"]):
                messagebox.showwarning("Hora ocupada", f"Ya hay una cita a las {hora} ese día.")
                return
            pid = pacientes[[p["nombre"] for p in pacientes].index(combo_pac.get())]["id"]
            actualizar_cita(cita["id"], pid, hora, motivo_var.get().strip())
            ventana.destroy()
            self.refrescar_calendario()
            self._mostrar_dia()

        ttk.Button(ventana.winfo_children()[0], text="Guardar",
                   command=guardar).grid(row=3, column=0, columnspan=2, pady=(10, 0))

    def eliminar(self):
        if self._selected_id is None:
            messagebox.showinfo("Aviso", "Selecciona una cita de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar esta cita?"):
            borrar_cita(self._selected_id)
            self._selected_id = None
            self.refrescar_calendario()
            self._mostrar_dia()