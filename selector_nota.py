"""Componente reutilizable SelectorNota: cinco estrellas para elegir una nota de 1 a 5."""
from PySide6.QtCore import Property, Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton


class SelectorNota(QFrame):
    """Cinco estrellas para elegir una nota de 1 a 5, con el ratón o con el teclado.

    Propiedad:
        nota (int): la nota elegida, de 1 a 5. 0 si aún no se ha elegido ninguna.
    Señal:
        notaCambiada(int): se emite cada vez que cambia la nota.
    Método:
        limpiar(): vuelve a «sin nota» (0).
    Teclado (con el foco en el componente):
        teclas 1 a 5 → esa nota; flecha derecha → una más; flecha izquierda → una menos.

    Ejemplo:
        selector = SelectorNota()
        selector.notaCambiada.connect(lambda n: print("Nota:", n))
    """

    # La señal propia se declara en la CLASE, no dentro de __init__
    notaCambiada = Signal(int)

    LLENA = "★"
    VACIA = "☆"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._nota = 0

        # ── El foco: el componente entero recibe el teclado ──────────────
        # StrongFocus: se llega con Tab y con un clic
        self.setFocusPolicy(Qt.StrongFocus)

        # ── Composición: cinco botones-estrella y la nota en número ──────
        disposicion = QHBoxLayout(self)
        disposicion.setContentsMargins(4, 2, 4, 2)
        disposicion.setSpacing(0)
        self._estrellas = []
        for valor in range(1, 6):
            estrella = QToolButton()
            estrella.setAutoRaise(True)                # sin borde de botón
            estrella.setFocusPolicy(Qt.NoFocus)        # el foco lo tiene el componente, no cada estrella
            estrella.setToolTip(f"{valor} de 5")
            estrella.setStyleSheet("font-size: 20px;")
            # valor=valor: cada estrella recuerda su propio número
            estrella.clicked.connect(lambda _=False, valor=valor: self._set_nota(valor))
            disposicion.addWidget(estrella)
            self._estrellas.append(estrella)
        self._numero = QLabel()
        self._numero.setMinimumWidth(24)
        disposicion.addSpacing(8)
        disposicion.addWidget(self._numero)
        disposicion.addStretch()

        self._dibujar()

    # ── La propiedad «nota» ──────────────────────────────────────────────
    def _get_nota(self):
        return self._nota

    def _set_nota(self, valor):
        valor = max(0, min(5, valor))      # siempre entre 0 y 5
        if valor == self._nota:
            return                          # sin cambios: no se avisa
        self._nota = valor
        self._dibujar()
        self.notaCambiada.emit(valor)

    nota = Property(int, _get_nota, _set_nota, notify=notaCambiada)

    def limpiar(self):
        self._set_nota(0)

    # ── Dibujar: estrellas llenas hasta la nota y el número ──────────────
    def _dibujar(self):
        for valor, estrella in enumerate(self._estrellas, start=1):
            estrella.setText(self.LLENA if valor <= self._nota else self.VACIA)
        self._numero.setText(str(self._nota) if self._nota else "–")
        # Lo que lee el lector de pantalla, además del nombre accesible
        self.setAccessibleDescription(f"{self._nota} de 5" if self._nota else "Sin nota")

    # ── El teclado ───────────────────────────────────────────────────────
    def keyPressEvent(self, evento):
        tecla = evento.key()
        if Qt.Key_1 <= tecla <= Qt.Key_5:
            self._set_nota(tecla - Qt.Key_0)
        elif tecla == Qt.Key_Right:
            self._set_nota(max(1, self._nota + 1))
        elif tecla == Qt.Key_Left:
            self._set_nota(max(1, self._nota - 1))
        else:
            super().keyPressEvent(evento)   # el resto (Tab…), como siempre

    # Un marco alrededor cuando tiene el foco, para que se vea dónde está el teclado
    def focusInEvent(self, evento):
        self.setFrameShape(QFrame.StyledPanel)
        super().focusInEvent(evento)

    def focusOutEvent(self, evento):
        self.setFrameShape(QFrame.NoFrame)
        super().focusOutEvent(evento)