"""El almacén de ValoraDI: guarda y lee las valoraciones y los pesos con SQLite.

Aquí está todo el SQL. Este módulo no usa Qt: si algo falla, lanza sqlite3.Error
y es la ventana quien muestra el mensaje.
"""
import sqlite3
from pathlib import Path

from modelo import Pesos, Valora

# La base de datos se guarda junto a este archivo, se ejecute desde donde se ejecute
RUTA_BD = Path(__file__).with_name("valora.db")


def conectar():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row   # acceso por nombre: fila["docente"]
    return conexion


# ── Crear las tablas (solo la primera vez) ───────────────────────────────
def crear_bd():
    conexion = conectar()
    try:
        # Una fila por valoración. CHECK: la base de datos no acepta notas fuera de 1 a 5
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS valora (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                docente    INTEGER NOT NULL CHECK (docente BETWEEN 1 AND 5),
                materiales INTEGER NOT NULL CHECK (materiales BETWEEN 1 AND 5),
                clases     INTEGER NOT NULL CHECK (clases BETWEEN 1 AND 5)
            )
        """)
        # Una sola fila (id = 1) con los pesos de la nota global
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS pesos (
                id         INTEGER PRIMARY KEY CHECK (id = 1),
                docente    INTEGER NOT NULL,
                materiales INTEGER NOT NULL,
                clases     INTEGER NOT NULL
            )
        """)
        conexion.commit()
    finally:
        conexion.close()


# ── Las valoraciones ─────────────────────────────────────────────────────
def guardar_valora(valora):
    conexion = conectar()
    try:
        # Los ? se sustituyen por los valores, en orden: nunca se pegan al texto del SQL
        conexion.execute(
            "INSERT INTO valora (docente, materiales, clases) VALUES (?, ?, ?)",
            (valora.docente, valora.materiales, valora.clases),
        )
        conexion.commit()
    finally:
        conexion.close()


def leer_valoras():
    conexion = conectar()
    try:
        filas = conexion.execute("SELECT docente, materiales, clases FROM valora ORDER BY id").fetchall()
        return [Valora(f["docente"], f["materiales"], f["clases"]) for f in filas]
    finally:
        conexion.close()


# ── Los pesos ────────────────────────────────────────────────────────────
def leer_pesos():
    """Los pesos guardados o, si aún no se han cambiado nunca, los de por defecto."""
    conexion = conectar()
    try:
        fila = conexion.execute("SELECT docente, materiales, clases FROM pesos WHERE id = 1").fetchone()
        return Pesos() if fila is None else Pesos(fila["docente"], fila["materiales"], fila["clases"])
    finally:
        conexion.close()


def guardar_pesos(pesos):
    conexion = conectar()
    try:
        # INSERT OR REPLACE: si ya hay una fila con id = 1, la sustituye
        conexion.execute(
            "INSERT OR REPLACE INTO pesos (id, docente, materiales, clases) VALUES (1, ?, ?, ?)",
            (pesos.docente, pesos.materiales, pesos.clases),
        )
        conexion.commit()
    finally:
        conexion.close()