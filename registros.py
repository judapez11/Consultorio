import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox

from campo_fecha import CampoFecha

COLUMNAS_REGISTROS = {
    "temp_ambiente": [
        ("fecha", "Fecha", 110), ("temp_8am", "Temp 8:00 AM", 110),
        ("temp_4pm", "Temp 4:00 PM", 110), ("realizo", "Realizo", 140),
    ],
    "temp_nevera": [
        ("fecha", "Fecha", 110), ("temp_8am", "Temp 8:00 AM", 110),
        ("temp_4pm", "Temp 4:00 PM", 110), ("realizo", "Realizo", 140),
    ],
    "insumos": [
        ("fecha_compra", "Fecha compra", 110), ("producto", "Producto", 150),
        ("marca", "Marca", 120), ("cantidad", "Cantidad", 90),
        ("referencia", "Referencia", 120), ("registro_invima", "Registro INVIMA", 130),
        ("condicion_almacenamiento", "Condicion almacenamiento", 180),
        ("fecha_vencimiento", "Fecha vencimiento", 130),
    ],
    "esterilizacion": [
        ("fecha", "Fecha", 100), ("operador", "Operador", 140),
        ("tipo_empaque", "Tipo empaque", 120), ("tipo_material", "Material", 120),
        ("tiempo", "Tiempo", 80), ("temperatura", "Temp", 80),
        ("cinta_indicadora", "Cinta indicadora", 130), ("control_quimico", "Control quimico", 130),
        ("cinta_resultado", "Cinta resultado", 130), ("control_resultado", "Control resultado", 130),
        ("verificacion", "Verificacion", 130),
    ],
    "glutaraldehido": [
        ("fecha_inicio", "Fecha de inicio", 160),
        ("fecha_cambio", "Fecha de cambio", 160),
    ],
}


class RegistroTab(ttk.Frame):
    """Registro administrativo tipo ledger: tabla de filas + agregar/editar/eliminar."""

    def __init__(self, master, nombre):
        super().__init__(master, padding=10)
        self._nombre = nombre
        self._columnas = COLUMNAS_REGISTROS[nombre]
        self._selected_id = None
        self._build()

    def _build(self):
        self._crud = self._importar_crud()
        self.tree = ttk.Treeview(
            self, columns=("id",) + tuple(c[0] for c in self._columnas),
            show="headings", selectmode="browse",
        )
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, stretch=False)
        for clave, etiqueta, ancho in self._columnas:
            self.tree.heading(clave, text=etiqueta)
            self.tree.column(clave, width=ancho)
        scroll = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scroll.set)
        self.tree.pack(fill="both", expand=True)
        scroll.pack(fill="x")
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar)

        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=(6, 0))
        ttk.Button(botones, text="+ Agregar", command=self._agregar).pack(side="left")
        ttk.Button(botones, text="Editar", command=self._editar).pack(side="left", padx=8)
        ttk.Button(botones, text="Eliminar", command=self._eliminar).pack(side="left")

        self._refrescar()

    def _importar_crud(self):
        from db import REGISTROS_CRUD
        return REGISTROS_CRUD[self._nombre]

    def _seleccionar(self, event):
        sel = self.tree.selection()
        self._selected_id = int(sel[0]) if sel else None

    def _refrescar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for fila in self._crud["listar"]():
            valores = tuple(fila[c[0]] for c in self._columnas)
            self.tree.insert("", "end", iid=str(fila["id"]),
                             values=(fila["id"],) + valores)

    def _dialogo(self, titulo, datos=None):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()
        f = ttk.Frame(ventana, padding=15)
        f.pack(fill="both", expand=True)
        widgets = {}
        for fila, (clave, etiqueta, _ancho) in enumerate(self._columnas):
            ttk.Label(f, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=3)
            if "fecha" in clave:
                campo = CampoFecha(f)
                valor = (datos or {}).get(clave)
                if valor:
                    try:
                        campo.set_date(dt.datetime.strptime(valor, "%Y-%m-%d").date())
                    except ValueError:
                        pass
            else:
                campo = ttk.Entry(f)
                if datos:
                    campo.insert(0, datos.get(clave, ""))
            campo.grid(row=fila, column=1, sticky="we", padx=6, pady=3)
            widgets[clave] = campo
        f.columnconfigure(1, weight=1)
        return ventana, widgets

    def _guardar_dialogo(self, ventana, widgets, rid=None):
        datos = {}
        for clave, widget in widgets.items():
            if isinstance(widget, CampoFecha):
                fecha = widget.get_date()
                datos[clave] = fecha.strftime("%Y-%m-%d") if fecha else ""
            else:
                datos[clave] = widget.get().strip()
        if rid is None:
            self._crud["guardar"](datos)
        else:
            self._crud["actualizar"](rid, datos)
        ventana.destroy()
        self._refrescar()

    def _agregar(self):
        ventana, widgets = self._dialogo("Agregar registro")
        ttk.Button(ventana.winfo_children()[0], text="Guardar",
                   command=lambda: self._guardar_dialogo(ventana, widgets)
                   ).grid(row=len(self._columnas), column=0, columnspan=2, pady=(10, 0))

    def _editar(self):
        if self._selected_id is None:
            messagebox.showinfo("Aviso", "Selecciona un registro de la lista.")
            return
        datos = self._crud["get"](self._selected_id)
        ventana, widgets = self._dialogo("Editar registro", datos)
        rid = self._selected_id
        ttk.Button(ventana.winfo_children()[0], text="Guardar",
                   command=lambda: self._guardar_dialogo(ventana, widgets, rid)
                   ).grid(row=len(self._columnas), column=0, columnspan=2, pady=(10, 0))

    def _eliminar(self):
        if self._selected_id is None:
            messagebox.showinfo("Aviso", "Selecciona un registro de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este registro?"):
            self._crud["borrar"](self._selected_id)
            self._selected_id = None
            self._refrescar()