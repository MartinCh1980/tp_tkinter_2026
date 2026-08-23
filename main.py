"""
Punto de entrada de la aplicación.

Acá se ve el objetivo central del TP: la MISMA clase (CRUDFrame) se usa
para dos entidades distintas, cambiando únicamente los parámetros de
inicialización (título, campos y repositorio). Cero copy-paste de la
lógica de la interfaz.
"""

import tkinter as tk
from tkinter import ttk

from crud_gui import CRUDFrame
from repositorio import RepositorioMemoria, RepositorioSQLite

# Cambiá esta constante para elegir el modo de persistencia sin tocar
# nada más del código. Así queda "preparado para las dos" opciones.
USAR_SQLITE = False


def crear_repositorio(nombre_tabla: str, columnas: list[str]):
    if USAR_SQLITE:
        return RepositorioSQLite(nombre_tabla, columnas)
    return RepositorioMemoria()


def main():
    ventana = tk.Tk()
    ventana.title("TP Tkinter - CRUD Genérico")
    ventana.geometry("650x500")

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True)

    # --- Entidad 1: Vehículos ---
    campos_vehiculos = [
        ("patente", "Patente"),
        ("marca", "Marca"),
        ("modelo", "Modelo"),
        ("anio", "Año"),
    ]
    repo_vehiculos = crear_repositorio("vehiculos", [c for c, _ in campos_vehiculos])
    frame_vehiculos = CRUDFrame(notebook, "Vehículos", campos_vehiculos, repo_vehiculos)
    notebook.add(frame_vehiculos, text="Vehículos")

    # --- Entidad 2: Propietarios ---
    campos_propietarios = [
        ("dni", "DNI"),
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("telefono", "Teléfono"),
    ]
    repo_propietarios = crear_repositorio("propietarios", [c for c, _ in campos_propietarios])
    frame_propietarios = CRUDFrame(notebook, "Propietarios", campos_propietarios, repo_propietarios)
    notebook.add(frame_propietarios, text="Propietarios")

    ventana.mainloop()


if __name__ == "__main__":
    main()
