"""
Vista + Controlador de la interfaz.

CRUDFrame es LA clase genérica: se instancia una vez por entidad
(Vehículos, Propietarios, lo que sea) variando únicamente los
parámetros del constructor. No conoce SQLite ni nada de bases de datos:
solo conoce el contrato de Repositorio (obtener_todos/agregar/actualizar/eliminar).
"""

import tkinter as tk
from tkinter import ttk, messagebox


class CRUDFrame(tk.Frame):
    def __init__(self, master, titulo_entidad, campos, repositorio):
        """
        master: el widget contenedor (ventana o Notebook)
        titulo_entidad: string para mostrar, ej "Vehículos"
        campos: lista de tuplas (clave_interna, etiqueta_visible)
                ej [("patente", "Patente"), ("marca", "Marca"), ("modelo", "Modelo")]
        repositorio: instancia de Repositorio (memoria o SQLite)
        """
        super().__init__(master)
        self.titulo_entidad = titulo_entidad
        self.campos = campos
        self.repositorio = repositorio

        # --- Gestión del estado ---
        # Acá vive la clave de todo el punto "Gestión del Estado" del enunciado:
        # un diccionario que mapea clave_interna -> widget Entry.
        # Gracias a esto, leer o limpiar el formulario es un solo bucle,
        # sin importar cuántos campos tenga la entidad.
        self.entradas: dict[str, tk.Entry] = {}

        self.id_seleccionado = None  # id del registro elegido en la tabla (o None)

        self._construir_formulario()
        self._construir_botones()
        self._construir_tabla()
        self._refrescar_tabla()

    # ------------------------------------------------------------------
    # Construcción dinámica del formulario
    # ------------------------------------------------------------------
    def _construir_formulario(self):
        frame_form = tk.LabelFrame(self, text=f"Datos de {self.titulo_entidad}")
        frame_form.pack(padx=10, pady=10, fill="x")

        # Acá está la "Generación Dinámica" que pide el TP: un solo bucle
        # que recorre self.campos y crea Label + Entry para cada uno.
        # Si mañana la entidad tiene 3 campos o 10, este código no cambia.
        for fila, (clave, etiqueta) in enumerate(self.campos):
            lbl = tk.Label(frame_form, text=f"{etiqueta}:")
            lbl.grid(row=fila, column=0, sticky="e", padx=5, pady=4)

            entrada = tk.Entry(frame_form, width=30)
            entrada.grid(row=fila, column=1, sticky="we", padx=5, pady=4)

            # guardamos la referencia en el diccionario de estado
            self.entradas[clave] = entrada

        frame_form.columnconfigure(1, weight=1)

    def _construir_botones(self):
        frame_botones = tk.Frame(self)
        frame_botones.pack(padx=10, pady=(0, 10), fill="x")

        tk.Button(frame_botones, text="Crear", command=self._crear).pack(side="left", padx=3)
        tk.Button(frame_botones, text="Actualizar", command=self._actualizar).pack(side="left", padx=3)
        tk.Button(frame_botones, text="Eliminar", command=self._eliminar).pack(side="left", padx=3)
        tk.Button(frame_botones, text="Limpiar", command=self._limpiar_formulario).pack(side="left", padx=3)

    def _construir_tabla(self):
        columnas_ids = [clave for clave, _ in self.campos]
        self.tabla = ttk.Treeview(self, columns=columnas_ids, show="headings", height=8)

        for clave, etiqueta in self.campos:
            self.tabla.heading(clave, text=etiqueta)
            self.tabla.column(clave, width=120, anchor="center")

        self.tabla.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

    # ------------------------------------------------------------------
    # Lectura / limpieza del formulario (usa el diccionario de estado)
    # ------------------------------------------------------------------
    def _leer_formulario(self) -> dict:
        return {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}

    def _limpiar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.tabla.selection_remove(self.tabla.selection())
        self.id_seleccionado = None

    def _cargar_formulario(self, datos: dict):
        for clave, entrada in self.entradas.items():
            entrada.delete(0, tk.END)
            entrada.insert(0, datos.get(clave, ""))

    # ------------------------------------------------------------------
    # Validación
    # ------------------------------------------------------------------
    def _validar_campos_completos(self, datos: dict) -> bool:
        faltantes = [
            etiqueta for clave, etiqueta in self.campos if not datos.get(clave)
        ]
        if faltantes:
            messagebox.showwarning(
                "Campos incompletos",
                "Completá los siguientes campos:\n- " + "\n- ".join(faltantes),
            )
            return False
        return True

    # ------------------------------------------------------------------
    # Operaciones CRUD (delegan todo en self.repositorio)
    # ------------------------------------------------------------------
    def _crear(self):
        datos = self._leer_formulario()
        if not self._validar_campos_completos(datos):
            return
        self.repositorio.agregar(datos)
        self._limpiar_formulario()
        self._refrescar_tabla()
        messagebox.showinfo("Éxito", f"{self.titulo_entidad[:-1] if self.titulo_entidad.endswith('s') else self.titulo_entidad} creado correctamente.")

    def _actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Primero seleccioná un registro de la tabla.")
            return
        datos = self._leer_formulario()
        if not self._validar_campos_completos(datos):
            return
        self.repositorio.actualizar(self.id_seleccionado, datos)
        self._limpiar_formulario()
        self._refrescar_tabla()
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")

    def _eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin selección", "Primero seleccioná un registro de la tabla.")
            return
        confirmar = messagebox.askyesno("Confirmar", "¿Seguro que querés eliminar este registro?")
        if not confirmar:
            return
        self.repositorio.eliminar(self.id_seleccionado)
        self._limpiar_formulario()
        self._refrescar_tabla()

    # ------------------------------------------------------------------
    # Tabla
    # ------------------------------------------------------------------
    def _refrescar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for registro in self.repositorio.obtener_todos():
            valores = [registro.get(clave, "") for clave, _ in self.campos]
            # usamos el id real del registro como "iid" del item en el Treeview,
            # así después lo recuperamos directo al seleccionar una fila.
            self.tabla.insert("", tk.END, iid=str(registro["id"]), values=valores)

    def _al_seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_registro = int(seleccion[0])
        registros = {r["id"]: r for r in self.repositorio.obtener_todos()}
        registro = registros.get(id_registro)
        if registro:
            self.id_seleccionado = id_registro
            self._cargar_formulario(registro)
