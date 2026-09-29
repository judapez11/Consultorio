import tkinter as tk
from tkinter import ttk, messagebox

from db import (
    listar_pacientes,
    listar_historias_od,
    get_historia_od,
    guardar_historia_od,
    actualizar_historia_od,
    borrar_historia_od,
    listar_historias_urgencia,
    get_historia_urgencia,
    guardar_historia_urgencia,
    actualizar_historia_urgencia,
    borrar_historia_urgencia,
    listar_evolucion,
    get_evolucion,
    guardar_evolucion,
    actualizar_evolucion,
    borrar_evolucion,
)
from historia_odontologica import HistoriaOdontologicaForm
from historia_urgencia import HistoriaUrgenciaForm
from historia_evolucion import HistoriaEvolucionForm

DOCUMENTOS = {
    "Historia Odontologica": {"form": HistoriaOdontologicaForm,
                              "listar": listar_historias_od,
                              "get": get_historia_od,
                              "guardar": guardar_historia_od,
                              "actualizar": actualizar_historia_od,
                              "borrar": borrar_historia_od,
                              "columna": "Motivo de consulta"},
    "Historia de Urgencia": {"form": HistoriaUrgenciaForm,
                             "listar": listar_historias_urgencia,
                             "get": get_historia_urgencia,
                             "guardar": guardar_historia_urgencia,
                             "actualizar": actualizar_historia_urgencia,
                             "borrar": borrar_historia_urgencia,
                             "columna": "Motivo de consulta"},
    "Hoja de Evolucion": {"form": HistoriaEvolucionForm,
                          "listar": listar_evolucion,
                          "get": get_evolucion,
                          "guardar": guardar_evolucion,
                          "actualizar": actualizar_evolucion,
                          "borrar": borrar_evolucion,
                          "columna": "Detalle"},
}


class ScrollableFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll = tk.Scrollbar(self, orient="vertical",
                                   command=self.canvas.yview, width=22,
                                   relief="groove")
        self.scroll.pack(side="right", fill="y")

        self.interior = ttk.Frame(self.canvas)
        self.interior.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self._ventana = self.canvas.create_window(
            (0, 0), window=self.interior, anchor="nw", tags="ventana"
        )
        self.canvas.bind("<Configure>", self._ajustar_ancho)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.canvas.bind_all("<MouseWheel>", self._rueda)
        self.canvas.bind_all("<Button-4>", self._rueda_linux)
        self.canvas.bind_all("<Button-5>", self._rueda_linux)

    def _ajustar_ancho(self, event):
        self.canvas.itemconfigure(self._ventana, width=event.width)

    def _rueda(self, event):
        if isinstance(event.widget, (tk.Text, tk.Listbox)):
            return
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _rueda_linux(self, event):
        if isinstance(event.widget, (tk.Text, tk.Listbox)):
            return
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")


class DocumentoTab(ttk.Frame):
    """Pestana para un tipo de documento: selector de paciente + lista + form."""

    def __init__(self, master, nombre_doc, conf):
        super().__init__(master, padding=10)
        self._nombre_doc = nombre_doc
        self._conf = conf
        self._paciente_id = None
        self._historia_id = None
        self._form = None
        self._pacientes = []
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x")

        ttk.Label(top, text="Paciente:", font=("Segoe UI", 11, "bold")).pack(side="left")

        lista_frame = ttk.Frame(top)
        lista_frame.pack(side="left", fill="x", expand=True, padx=6)
        self._pac_list = tk.Listbox(
            lista_frame, height=6, exportselection=False,
            activestyle="dotbox", font=("Segoe UI", 11),
        )
        scroll = ttk.Scrollbar(lista_frame, orient="vertical",
                               command=self._pac_list.yview)
        self._pac_list.configure(yscrollcommand=scroll.set)
        self._pac_list.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")
        self._pac_list.bind("<<ListboxSelect>>", self._list_seleccion)
        self._pac_list.bind("<MouseWheel>", self._rueda_lista)
        self._pac_list.bind("<Button-4>", self._rueda_lista_linux)
        self._pac_list.bind("<Button-5>", self._rueda_lista_linux)

        medio = ttk.Frame(self)
        medio.pack(fill="x", pady=8)

        ttk.Label(medio, text="Historias del paciente:").pack(anchor="w")
        self.tree = ttk.Treeview(medio, columns=("id", "fecha", "motivo"),
                                 show="headings", height=5, selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("motivo", text=self._conf.get("columna", "Motivo de consulta"))
        self.tree.column("id", width=60, stretch=False)
        self.tree.column("fecha", width=120, stretch=False)
        self.tree.column("motivo", width=320)
        self.tree.pack(fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar_historia)

        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=(6, 0))
        ttk.Button(botones, text="Nueva", command=self._nueva).pack(side="left")
        ttk.Button(botones, text="Guardar", command=self._guardar).pack(side="left", padx=8)
        ttk.Button(botones, text="Cancelar", command=self._cancelar).pack(side="left")
        ttk.Button(botones, text="Borrar", command=self._borrar).pack(side="left", padx=8)

        self.scroll = ScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, pady=(8, 0))

        self._refrescar_pacientes()
        self._nueva()

    def _cargar_lista(self):
        self._pacientes = listar_pacientes()
        self._pac_list.delete(0, "end")
        for p in self._pacientes:
            self._pac_list.insert("end", p["nombre"])

    def _index_actual(self):
        for i, p in enumerate(self._pacientes):
            if p["id"] == self._paciente_id:
                return i
        return -1

    def _fijar_lista(self):
        self._pac_list.selection_clear(0, "end")
        idx = self._index_actual()
        if idx >= 0:
            self._pac_list.selection_set(idx)
            self._pac_list.see(idx)

    def _rueda_lista(self, event):
        self._pac_list.yview_scroll(int(-event.delta / 120), "units")
        return "break"

    def _rueda_lista_linux(self, event):
        if event.num == 4:
            self._pac_list.yview_scroll(-1, "units")
        elif event.num == 5:
            self._pac_list.yview_scroll(1, "units")
        return "break"

    def _list_seleccion(self, event):
        sel = self._pac_list.curselection()
        if not sel:
            return
        self._intentar_cambiar(sel[0])

    def _intentar_cambiar(self, idx):
        if idx == self._index_actual():
            return
        if self._form is not None and self._form.tiene_contenido():
            if not messagebox.askyesno(
                    "Cambiar paciente",
                    "El formulario tiene datos sin guardar.\n"
                    "¿Descartarlos y cambiar de paciente?"):
                self._fijar_lista()
                return
        self._cambiar_a(idx)

    def _cambiar_a(self, idx):
        p = self._pacientes[idx]
        self._paciente_id = p["id"]
        self._fijar_lista()
        self._refrescar_historias()
        self._nueva()

    def _refrescar_pacientes(self):
        self._cargar_lista()
        if self._pacientes:
            self._paciente_id = self._pacientes[0]["id"]
        else:
            self._paciente_id = None
        self._fijar_lista()
        self._refrescar_historias()

    def _config_doc(self):
        return self._conf

    def _refrescar_historias(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not self._paciente_id:
            return
        for h in self._conf["listar"](self._paciente_id):
            self.tree.insert("", "end", iid=str(h["id"]),
                             values=(h["id"], h["fecha"], h["motivo_consulta"]))

    def _nombre_paciente(self):
        for p in self._pacientes:
            if p["id"] == self._paciente_id:
                return p["nombre"]
        return ""

    def _prefill_form(self):
        prefill = getattr(self._form, "prefill_nombre", None)
        if prefill:
            prefill(self._nombre_paciente())

    def _nueva(self):
        self._historia_id = None
        self.tree.selection_remove(self.tree.selection())
        self._refrescar_historias()
        for child in self.scroll.interior.winfo_children():
            child.destroy()
        self._form = self._conf["form"](self.scroll.interior)
        self._form.pack(fill="both", expand=True)
        self._prefill_form()

    def _cancelar(self):
        self._nueva()

    def _seleccionar_historia(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        hid = int(sel[0])
        datos = self._conf["get"](hid)
        if not datos:
            return
        self._historia_id = hid
        for child in self.scroll.interior.winfo_children():
            child.destroy()
        self._form = self._conf["form"](self.scroll.interior)
        self._form.pack(fill="both", expand=True)
        self._form.cargar(datos)

    def _guardar(self):
        if not self._paciente_id:
            messagebox.showwarning("Aviso", "Selecciona un paciente.")
            return
        if not self._form:
            return
        validar = getattr(self._form, "validar", None)
        if validar:
            faltan = validar()
            if faltan:
                messagebox.showwarning(
                    "Campos incompletos", "Completa antes de guardar: " + ", ".join(faltan)
                )
                return
        datos = self._form.datos()
        if self._historia_id is None:
            self._conf["guardar"](self._paciente_id, datos)
            messagebox.showinfo("Guardado", "Historia guardada.")
        else:
            self._conf["actualizar"](self._historia_id, datos)
            messagebox.showinfo("Guardado", "Historia actualizada.")
        self._refrescar_historias()

    def _borrar(self):
        if self._historia_id is None:
            messagebox.showinfo("Aviso", "Selecciona una historia de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Borrar esta historia?"):
            self._conf["borrar"](self._historia_id)
            self._nueva()
            self._refrescar_historias()