"""Pruebas del componente SelectorNota con pytest-qt.

Ejecuta desde la carpeta del proyecto:  python -m pytest -v
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolButton

from selector_nota import SelectorNota


def test_empieza_sin_nota(qtbot):
    selector = SelectorNota()
    qtbot.addWidget(selector)
    assert selector.nota == 0


def test_clic_en_la_cuarta_estrella(qtbot):
    selector = SelectorNota()
    qtbot.addWidget(selector)
    estrellas = selector.findChildren(QToolButton)
    assert len(estrellas) == 5
    with qtbot.waitSignal(selector.notaCambiada, timeout=1000) as espera:
        qtbot.mouseClick(estrellas[3], Qt.LeftButton)   # la cuarta (se cuenta desde 0)
    assert espera.args == [4]
    assert selector.nota == 4


def test_teclado(qtbot):
    selector = SelectorNota()
    qtbot.addWidget(selector)
    qtbot.keyClick(selector, Qt.Key_3)
    assert selector.nota == 3
    qtbot.keyClick(selector, Qt.Key_Right)
    assert selector.nota == 4
    qtbot.keyClick(selector, Qt.Key_Left)
    qtbot.keyClick(selector, Qt.Key_Left)
    assert selector.nota == 2


def test_limpiar(qtbot):
    selector = SelectorNota()
    qtbot.addWidget(selector)
    selector.nota = 5
    selector.limpiar()
    assert selector.nota == 0