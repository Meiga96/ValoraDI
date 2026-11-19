"""El modelo de ValoraDI: los datos y todos los cálculos.

Este módulo no usa Qt ni SQL: solo Python. Por eso se puede probar con pytest
sin abrir ninguna ventana. La ventana le pide el resumen ya calculado y lo dibuja.
"""
from dataclasses import dataclass

# ── Las categorías ───────────────────────────────────────────────────────
# El nombre interno (el de las columnas de la base de datos) y el que se ve
CATEGORIAS = ("docente", "materiales", "clases")
NOMBRES = {"docente": "Docente", "materiales": "Materiales", "clases": "Clases"}

NOTA_MINIMA = 1
NOTA_MAXIMA = 5


# ── Una valoración: una nota de 1 a 5 para cada categoría ────────────────
@dataclass(frozen=True)
class Valora:
    docente: int
    materiales: int
    clases: int

    def nota(self, categoria):
        """La nota de una categoría: valora.nota("docente")."""
        return getattr(self, categoria)


# ── Los pesos: cuánto cuenta cada categoría en la nota global, en % ──────
@dataclass(frozen=True)
class Pesos:
    docente: int = 40
    materiales: int = 30
    clases: int = 30

    def peso(self, categoria):
        return getattr(self, categoria)

    @property
    def suma(self):
        return self.docente + self.materiales + self.clases

    @property
    def validos(self):
        """Los pesos solo son válidos si suman exactamente 100."""
        return self.suma == 100

    @property
    def aviso(self):
        """El mensaje para quien los está cambiando: cuánto falta o sobra."""
        if self.suma < 100:
            return f"Faltan {100 - self.suma} puntos para llegar a 100 %"
        if self.suma > 100:
            return f"Sobran {self.suma - 100} puntos: la suma pasa de 100 %"
        return ""


# ── El resumen, ya calculado: la ventana solo lo dibuja ──────────────────
@dataclass(frozen=True)
class FilaResumen:
    nombre: str          # "Docente"
    media: float | None  # la media de esa categoría; None si no hay valoraciones
    peso: int            # su peso, en %

    @property
    def texto_media(self):
        return formatear(self.media)


@dataclass(frozen=True)
class Resumen:
    total: int                  # cuántas valoraciones hay
    filas: list                 # una FilaResumen por categoría
    nota_global: float | None   # la media ponderada; None si no hay valoraciones

    @property
    def texto_total(self):
        if self.total == 0:
            return "Aún no hay valoraciones"
        if self.total == 1:
            return "1 valoración"
        return f"{self.total} valoraciones"

    @property
    def texto_global(self):
        return formatear(self.nota_global)


# ── Los cálculos ─────────────────────────────────────────────────────────
def formatear(numero):
    """Un número con un decimal y punto decimal (3.8). Sin número, una raya."""
    return "–" if numero is None else f"{numero:.1f}"


def media(valoras, categoria):
    """La media de una categoría. None si no hay valoraciones."""
    if not valoras:
        return None
    return sum(v.nota(categoria) for v in valoras) / len(valoras)


def nota_global(valoras, pesos):
    """La media ponderada: cada media por su peso, y la suma entre 100.

    Con docente 4.0 (40 %), materiales 3.0 (30 %) y clases 5.0 (30 %):
    (4.0 · 40 + 3.0 · 30 + 5.0 · 30) / 100 = 4.0
    """
    if not valoras:
        return None
    return sum(media(valoras, c) * pesos.peso(c) for c in CATEGORIAS) / 100


def resumir(valoras, pesos):
    """Todo lo que muestra el resumen, en un solo objeto."""
    filas = [FilaResumen(NOMBRES[c], media(valoras, c), pesos.peso(c)) for c in CATEGORIAS]
    return Resumen(total=len(valoras), filas=filas, nota_global=nota_global(valoras, pesos))