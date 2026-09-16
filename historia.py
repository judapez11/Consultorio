import tkinter as tk
from tkinter import ttk, messagebox

from db import (
    listar_pacientes,
    listar_historias_od,
    get_historia_od,
    guardar_historia_od,
    actualizar_historia_od,
    borrar_historia_od,
)
from historia_odontologica import HistoriaOdontologicaForm

DOCUMENTOS = {
    "Historia Odontologica": {"form": HistoriaOdontologicaForm,
                              "listar": listar_historias_od,
                              "get": get_historia_od,
                              "guardar": guardar_historia_od,
                              "actualizar": actualizar_historia_od,
                              "borrar": borrar_historia_od},
}


class ScrollableFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.interior.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>",
                          lambda ev: self.canvas.yview_scroll(int(-ev.delta / 120), "units")))
        self.interior.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))


class HistoriaTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._paciente_id = None
        self._historia_id = None
        self._form = None
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x")

        ttk.Label(top, text="Paciente:").pack(side="left")
        self.combo_pac = ttk.Combobox(top, state="readonly", width=40)
        self.combo_pac.pack(side="left", padx=6)
        self.combo_pac.bind("<<ComboboxSelected>>", lambda e: self._cargar_paciente())

        ttk.Label(top, text="Documento:").pack(side="left", padx=(16, 0))
        self.combo_doc = ttk.Combobox(
            top, values=list(DOCUMENTOS), state="readonly", width=24
        )
        self.combo_doc.set("Historia Odontologica")
        self.combo_doc.pack(side="left", padx=6)
        self.combo_doc.bind("<<ComboboxSelected>>", lambda e: self._nueva())

        medio = ttk.Frame(self)
        medio.pack(fill="x", pady=8)

        ttk.Label(medio, text="Historias del paciente:").pack(anchor="w")
        self.tree = ttk.Treeview(medio, columns=("id", "fecha"), show="headings",
                                 height=5, selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.column("id", width=60, stretch=False)
        self.tree.column("fecha", width=120)
        self.tree.pack(fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar_historia)

        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=(6, 0))
        ttk.Button(botones, text="Nueva", command=self._nueva).pack(side="left")
        ttk.Button(botones, text="Guardar", command=self._guardar).pack(side="left", padx=8)
        ttk.Button(botones, text="Borrar", command=self._borrar).pack(side="left")

        self.scroll = ScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, pady=(8, 0))

        self._refrescar_pacientes()
        self._nueva()

    def _refrescar_pacientes(self):
        self._pacientes = listar_pacientes()
        nombres = [p["nombre"] for p in self._pacientes]
        self.combo_pac["values"] = nombres
        if nombres:
            self.combo_pac.set(nombres[0])
            self._paciente_id = self._pacientes[0]["id"]
            self._refrescar_historias()

    def _cargar_paciente(self):
        idx = self.combo_pac.current()
        self._paciente_id = self._pacientes[idx]["id"] if idx >= 0 else None
        self._refrescar_historias()
        self._nueva()

    def _config_doc(self):
        nombre = self.combo_doc.get()
        return DOCUMENTOS.get(nombre)

    def _refrescar_historias(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not self._paciente_id:
            return
        conf = self._config_doc()
        for h in conf["listar"](self._paciente_id):
            self.tree.insert("", "end", iid=str(h["id"]),
                             values=(h["id"], h["fecha"]))

    def _nueva(self):
        self._historia_id = None
        self.tree.selection_remove(self.tree.selection())
        for child in self.scroll.interior.winfo_children():
            child.destroy()
        conf = self._config_doc()
        self._form = conf["form"](self.scroll.interior)
        self._form.pack(fill="both", expand=True)

    def _seleccionar_historia(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        hid = int(sel[0])
        conf = self._config_doc()
        datos = conf["get"](hid)
        if not datos:
            return
        self._historia_id = hid
        for child in self.scroll.interior.winfo_children():
            child.destroy()
        self._form = conf["form"](self.scroll.interior)
        self._form.pack(fill="both", expand=True)
        self._form.cargar(datos)

    def _guardar(self):
        if not self._paciente_id:
            messagebox.showwarning("Aviso", "Selecciona un paciente.")
            return
        if not self._form:
            return
        conf = self._config_doc()
        datos = self._form.datos()
        if self._historia_id is None:
            conf["guardar"](self._paciente_id, datos)
            messagebox.showinfo("Guardado", "Historia guardada.")
        else:
            conf["actualizar"](self._historia_id, datos)
            messagebox.showinfo("Guardado", "Historia actualizada.")
        self._refrescar_historias()

    def _borrar(self):
        if self._historia_id is None:
            messagebox.showinfo("Aviso", "Selecciona una historia de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Borrar esta historia?"):
            conf = self._config_doc()
            conf["borrar"](self._historia_id)
            self._nueva()
            self._refrescar_historias()