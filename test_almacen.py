"""Pruebas del almacén: guardar y leer con SQLite, en una base de datos de prueba.

Ejecuta desde la carpeta del proyecto:  python -m pytest -v
"""
import sqlite3

import pytest

import almacen
from modelo import Pesos, Valora


@pytest.fixture(autouse=True)
def bd_de_prueba(tmp_path, monkeypatch):
    # Cada prueba usa una base de datos nueva en una carpeta temporal: valora.db no se toca
    monkeypatch.setattr(almacen, "RUTA_BD", tmp_path / "prueba.db")
    almacen.crear_bd()


def test_guardar_y_leer_valoraciones():
    almacen.guardar_valora(Valora(4, 3, 5))
    almacen.guardar_valora(Valora(5, 2, 4))
    assert almacen.leer_valoras() == [Valora(4, 3, 5), Valora(5, 2, 4)]


def test_la_base_de_datos_no_acepta_notas_fuera_de_1_a_5():
    with pytest.raises(sqlite3.IntegrityError):
        almacen.guardar_valora(Valora(6, 3, 5))


def test_pesos_por_defecto_y_guardados():
    assert almacen.leer_pesos() == Pesos(40, 30, 30)
    almacen.guardar_pesos(Pesos(50, 25, 25))
    almacen.guardar_pesos(Pesos(60, 20, 20))        # sustituye, no añade otra fila
    assert almacen.leer_pesos() == Pesos(60, 20, 20)