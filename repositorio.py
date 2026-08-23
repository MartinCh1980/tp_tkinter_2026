"""
Capa de datos (Modelo).

La idea central acá es el patrón "Repositorio": definimos un contrato
(la clase abstracta Repositorio) que dice QUÉ operaciones tiene que poder
hacer cualquier fuente de datos, sin importar CÓMO las hace.

La GUI (crud_gui.py) va a hablar únicamente contra este contrato.
Nunca va a saber si atrás hay una lista de Python o una base SQLite.
Eso es justamente lo que pide el punto "Separación Lógica" del TP.
"""

from abc import ABC, abstractmethod
import sqlite3


class Repositorio(ABC):
    """Contrato que debe cumplir cualquier fuente de datos (memoria, SQLite, etc)."""

    @abstractmethod
    def obtener_todos(self) -> list[dict]:
        """Devuelve una lista de diccionarios, cada uno con 'id' + los campos."""
        raise NotImplementedError

    @abstractmethod
    def agregar(self, datos: dict) -> int:
        """Inserta un registro nuevo. Devuelve el id asignado."""
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, id_registro: int, datos: dict) -> None:
        """Modifica el registro con ese id."""
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, id_registro: int) -> None:
        """Borra el registro con ese id."""
        raise NotImplementedError


class RepositorioMemoria(Repositorio):
    """
    Implementación 'liviana': todo vive en un diccionario de Python
    mientras el programa está corriendo. Al cerrar la app, se pierde.
    Útil para probar la GUI sin depender de una base de datos.
    """

    def __init__(self):
        self._datos: dict[int, dict] = {}
        self._siguiente_id = 1

    def obtener_todos(self) -> list[dict]:
        return [{"id": id_reg, **valores} for id_reg, valores in self._datos.items()]

    def agregar(self, datos: dict) -> int:
        id_nuevo = self._siguiente_id
        self._datos[id_nuevo] = dict(datos)
        self._siguiente_id += 1
        return id_nuevo

    def actualizar(self, id_registro: int, datos: dict) -> None:
        if id_registro not in self._datos:
            raise KeyError(f"No existe el registro con id {id_registro}")
        self._datos[id_registro] = dict(datos)

    def eliminar(self, id_registro: int) -> None:
        if id_registro not in self._datos:
            raise KeyError(f"No existe el registro con id {id_registro}")
        del self._datos[id_registro]


class RepositorioSQLite(Repositorio):
    """
    Implementación real con base de datos SQLite.
    Es genérica: recibe el nombre de la tabla y las columnas por parámetro,
    así que sirve tanto para 'vehiculos' como para 'propietarios' sin
    escribir SQL distinto a mano para cada entidad.
    """

    def __init__(self, nombre_tabla: str, columnas: list[str], db_path: str = "tp_crud.db"):
        self.nombre_tabla = nombre_tabla
        self.columnas = columnas  # ej: ["patente", "marca", "modelo"]
        self._conexion = sqlite3.connect(db_path)
        self._crear_tabla_si_no_existe()

    def _crear_tabla_si_no_existe(self) -> None:
        columnas_sql = ", ".join(f"{col} TEXT" for col in self.columnas)
        self._conexion.execute(
            f"CREATE TABLE IF NOT EXISTS {self.nombre_tabla} "
            f"(id INTEGER PRIMARY KEY AUTOINCREMENT, {columnas_sql})"
        )
        self._conexion.commit()

    def obtener_todos(self) -> list[dict]:
        cursor = self._conexion.execute(
            f"SELECT id, {', '.join(self.columnas)} FROM {self.nombre_tabla}"
        )
        registros = []
        for fila in cursor.fetchall():
            registro = {"id": fila[0]}
            for indice, columna in enumerate(self.columnas):
                registro[columna] = fila[indice + 1]
            registros.append(registro)
        return registros

    def agregar(self, datos: dict) -> int:
        placeholders = ", ".join("?" for _ in self.columnas)
        valores = [datos[col] for col in self.columnas]
        cursor = self._conexion.execute(
            f"INSERT INTO {self.nombre_tabla} ({', '.join(self.columnas)}) "
            f"VALUES ({placeholders})",
            valores,
        )
        self._conexion.commit()
        return cursor.lastrowid

    def actualizar(self, id_registro: int, datos: dict) -> None:
        set_clause = ", ".join(f"{col} = ?" for col in self.columnas)
        valores = [datos[col] for col in self.columnas] + [id_registro]
        self._conexion.execute(
            f"UPDATE {self.nombre_tabla} SET {set_clause} WHERE id = ?", valores
        )
        self._conexion.commit()

    def eliminar(self, id_registro: int) -> None:
        self._conexion.execute(
            f"DELETE FROM {self.nombre_tabla} WHERE id = ?", (id_registro,)
        )
        self._conexion.commit()
