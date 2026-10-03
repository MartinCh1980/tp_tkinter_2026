# TP Tkinter — CRUD Genérico

Sistema de gestión con arquitectura orientada a objetos que implementa una
**clase genérica** de interfaz gráfica, capaz de instanciar el CRUD completo
para distintas entidades (**Vehículos** y **Propietarios**) variando
únicamente los parámetros de inicialización.

## Integrantes

- Alvarez Nicolás
- Aranda Antony
- Chamorro Martín

## Estructura del proyecto

```text
.
├── src/
│   ├── __init__.py          # Define src como paquete de Python
│   ├── crud_gui.py          # Clase genérica de interfaz (CRUDFrame)
│   └── repositorio.py       # Capa de datos: contrato Repositorio e implementaciones
├── main.py                  # Punto de entrada de la aplicación
├── .gitignore               # Archivos y carpetas excluidos del control de versiones
└── README.md                # Documentación del proyecto

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
- **`CRUDFrame`** (en `src.crud_gui.py`): clase genérica de Tkinter que arma el
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

Los casos de prueba ejecutados (validación de campos vacíos, flujo normal y manejo de selección al actualizar/eliminar) se encuentran documentados en el informe plan_de_pruebas.docx, entregado por separado a través de la plataforma de la cátedra.