import tkinter as tk
from tkinter import ttk, messagebox

from db import (
    listar_pacientes,
    guardar_paciente,
    actualizar_paciente,
    borrar_paciente,
)


class PacientesTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self._selected_id = None
        self._build()

    def _build(self):
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=50)
        top = ttk.LabelFrame(self, text="Buscar paciente", padding=10)
        top.pack(fill="x")

        self.busqueda_var = tk.StringVar()
        entrada = ttk.Entry(top, textvariable=self.busqueda_var)
        entrada.pack(side="left", fill="x", expand=True, padx=(0, 8))
        entrada.bind("<Return>", lambda e: self.refrescar_lista())
        ttk.Button(top, text="Buscar", command=self.refrescar_lista).pack(side="left")
        ttk.Button(top, text="Limpiar", command=self.limpiar_busqueda).pack(
            side="left", padx=(8, 0)
        )

        medio = ttk.Frame(self)
        medio.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(medio, columns=("id", "nombre", "telefono"),
                                 show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.column("id", width=50, stretch=False)
        self.tree.column("nombre", width=200)
        self.tree.column("telefono", width=120)
        scroll = ttk.Scrollbar(medio, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="left", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar)

        form = ttk.LabelFrame(self, text="Datos del paciente", padding=10)
        form.pack(fill="x")

        self.nombre_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.email_var = tk.StringVar()

        f = ttk.Frame(form)
        f.pack(fill="x")
        ttk.Label(f, text="Nombre").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(f, textvariable=self.nombre_var, width=40).grid(row=0, column=1, padx=5)
        ttk.Label(f, text="Teléfono").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(f, textvariable=self.telefono_var, width=40).grid(row=1, column=1, padx=5)
        ttk.Label(f, text="Dirección").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(f, textvariable=self.direccion_var, width=40).grid(row=2, column=1, padx=5)
        ttk.Label(f, text="Email").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(f, textvariable=self.email_var, width=40).grid(row=3, column=1, padx=5)
        f.columnconfigure(1, weight=1)

        botones = ttk.Frame(form)
        botones.pack(fill="x", pady=(10, 0))
        ttk.Button(botones, text="Guardar", command=self.guardar).pack(side="left")
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(
            side="left", padx=8
        )
        ttk.Button(botones, text="Borrar", command=self.borrar).pack(side="left")
        ttk.Button(botones, text="Nuevo", command=self.nuevo).pack(side="left", padx=8)

        self.refrescar_lista()

    def limpiar_busqueda(self):
        self.busqueda_var.set("")
        self.refrescar_lista()

    def refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in listar_pacientes(self.busqueda_var.get().strip()):
            self.tree.insert("", "end", iid=str(p["id"]),
                             values=(p["id"], p["nombre"], p["telefono"]))

    def _seleccionar(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        pid = int(sel[0])
        for p in listar_pacientes():
            if p["id"] == pid:
                self._selected_id = pid
                self.nombre_var.set(p["nombre"])
                self.telefono_var.set(p["telefono"])
                self.direccion_var.set(p["direccion"])
                self.email_var.set(p["email"])
                break

    def _datos_form(self):
        return {
            "nombre": self.nombre_var.get().strip(),
            "telefono": self.telefono_var.get().strip(),
            "direccion": self.direccion_var.get().strip(),
            "email": self.email_var.get().strip(),
        }

    def guardar(self):
        datos = self._datos_form()
        if not datos["nombre"]:
            messagebox.showwarning("Dato requerido", "El nombre es obligatorio.")
            return
        guardar_paciente(datos)
        self.nuevo()
        self.refrescar_lista()

    def actualizar(self):
        if self._selected_id is None:
            messagebox.showinfo("Aviso", "Selecciona un paciente de la lista.")
            return
        datos = self._datos_form()
        if not datos["nombre"]:
            messagebox.showwarning("Dato requerido", "El nombre es obligatorio.")
            return
        actualizar_paciente(self._selected_id, datos)
        self.refrescar_lista()

    def borrar(self):
        if self._selected_id is None:
            messagebox.showinfo("Aviso", "Selecciona un paciente de la lista.")
            return
        if messagebox.askyesno("Confirmar", "¿Borrar este paciente?"):
            borrar_paciente(self._selected_id)
            self.nuevo()
            self.refrescar_lista()

    def nuevo(self):
        self._selected_id = None
        self.nombre_var.set("")
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.email_var.set("")
        self.tree.selection_remove(self.tree.selection())