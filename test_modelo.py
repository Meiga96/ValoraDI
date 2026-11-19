"""Pruebas del modelo: los cálculos, sin ventanas ni base de datos.

Ejecuta desde la carpeta del proyecto:  python -m pytest -v
"""
import pytest

from modelo import Pesos, Valora, formatear, media, nota_global, resumir

# Tres valoraciones de ejemplo
VALORAS = [Valora(4, 3, 5), Valora(5, 2, 4), Valora(3, 4, 3)]


def test_media_de_una_categoria():
    assert media(VALORAS, "docente") == 4.0          # (4 + 5 + 3) / 3
    assert media(VALORAS, "materiales") == 3.0       # (3 + 2 + 4) / 3


def test_sin_valoraciones_no_hay_media_ni_nota_global():
    assert media([], "docente") is None
    assert nota_global([], Pesos()) is None


def test_nota_global_ponderada():
    # docente 4.0 · 40 + materiales 3.0 · 30 + clases 4.0 · 30 = 370 → 3.7
    assert nota_global(VALORAS, Pesos(40, 30, 30)) == pytest.approx(3.7)


def test_cambiar_los_pesos_cambia_la_nota_global():
    # Solo cuenta docente: la nota global es la media de docente
    assert nota_global(VALORAS, Pesos(100, 0, 0)) == pytest.approx(4.0)


def test_pesos_validos_y_aviso():
    assert Pesos(40, 30, 30).validos
    assert Pesos(40, 30, 30).aviso == ""
    assert not Pesos(40, 30, 20).validos
    assert Pesos(40, 30, 20).aviso == "Faltan 10 puntos para llegar a 100 %"
    assert Pesos(50, 30, 30).aviso == "Sobran 10 puntos: la suma pasa de 100 %"


def test_resumen_y_textos():
    resumen = resumir(VALORAS, Pesos())
    assert resumen.texto_total == "3 valoraciones"
    assert [f.texto_media for f in resumen.filas] == ["4.0", "3.0", "4.0"]
    assert resumen.texto_global == "3.7"
    assert resumir([Valora(5, 5, 5)], Pesos()).texto_total == "1 valoración"
    assert resumir([], Pesos()).texto_total == "Aún no hay valoraciones"
    assert formatear(None) == "–"