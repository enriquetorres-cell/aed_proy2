"""Caso borde: arista de peso 0 y nodo inalcanzable (traza de data/borde.txt).
Render individual:  manim -pql animacion/escena_borde.py EscenaBorde
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from comun import C_FINAL, C_INALCANZABLE, limpiar, lista_puntos, titulo_seccion
from escena_demo import demo_dial
from trace_loader import cargar_traza


def caso_borde(scene):
    t = titulo_seccion(scene, "Caso borde")
    puntos = lista_puntos([
        "• Arista de peso 0: d[u] + 0 = d, el vecino entra al MISMO bucket",
        "   que estamos procesando y se extrae en esta misma pasada.",
        "• Nodo inalcanzable: nunca entra a ningún bucket, su distancia queda ∞.",
        "• El algoritmo termina cuando TODOS los buckets están vacíos,",
        "   no cuando el puntero da una vuelta.",
    ], size=27).next_to(t, DOWN, buff=0.6)
    puntos[0].set_color(C_FINAL)
    puntos[2].set_color(C_INALCANZABLE)
    scene.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in puntos], lag_ratio=0.4),
               run_time=3)
    scene.wait(3)
    limpiar(scene)
    demo_dial(scene, cargar_traza("borde"), titulo="Caso borde: peso 0 y nodo inalcanzable",
              rt=0.9)


class EscenaBorde(Scene):
    def construct(self):
        caso_borde(self)
