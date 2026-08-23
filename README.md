# TP Tkinter — CRUD Genérico

Sistema de gestión con arquitectura orientada a objetos que implementa una
**clase genérica** de interfaz gráfica, capaz de instanciar el CRUD completo
para distintas entidades (**Vehículos** y **Propietarios**) variando
únicamente los parámetros de inicialización.

## Integrantes

- Nombre Apellido

## Estructura del proyecto

```
.
├── main.py              # Punto de entrada: instancia la clase genérica para cada entidad
├── crud_gui.py           # Clase genérica de interfaz (CRUDFrame)
├── repositorio.py         # Capa de datos: interfaz Repositorio + implementaciones (memoria / SQLite)
├── plan_de_pruebas.docx   # Reporte con los casos de prueba ejecutados
├── .gitignore
└── README.md
```

## Arquitectura

El proyecto sigue el patrón **Repositorio**, separando por completo la
interfaz gráfica de la lógica de persistencia:

- **`Repositorio`** (clase abstracta): define el contrato
  (`obtener_todos`, `agregar`, `actualizar`, `eliminar`) que debe cumplir
  cualquier fuente de datos.
- **`RepositorioMemoria`**: implementación en memoria (listas/diccionarios),
  útil para probar sin depender de una base de datos.
- **`RepositorioSQLite`**: implementación con base de datos real, genérica
  para cualquier tabla/columnas.
- **`CRUDFrame`** (en `crud_gui.py`): clase genérica de Tkinter que arma el
  formulario, la tabla y los botones **dinámicamente** a partir de una lista
  de campos, y delega toda operación de datos en el repositorio recibido por
  parámetro. No conoce SQLite ni ningún detalle de persistencia.

Gracias a esta separación, la misma clase `CRUDFrame` se reutiliza para
Vehículos y Propietarios sin duplicar código de interfaz — solo cambian los
parámetros del constructor (título, campos, repositorio).

## Requisitos

- Python 3.10 o superior (usa Tkinter, incluido en la instalación estándar)

## Cómo ejecutar

```bash
python main.py
```

Por defecto corre en modo de persistencia **en memoria**. Para usar SQLite,
cambiar la constante `USAR_SQLITE = True` en `main.py`.

## Plan de pruebas

El reporte `plan_de_pruebas.docx` documenta los casos de prueba ejecutados,
incluyendo validación de campos vacíos, flujo normal (happy path) y manejo
de errores de selección al actualizar/eliminar sin un registro elegido.
