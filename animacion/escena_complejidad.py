"""Analisis de complejidad, con los contadores reales de la ejecucion en C++.
Render individual:  manim -pql animacion/escena_complejidad.py EscenaComplejidad
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from comun import C_ARBOL, C_COLA, C_FINAL, limpiar, lista_puntos, texto, titulo_seccion
from trace_loader import cargar_traza


def complejidad(scene, traza):
    t = titulo_seccion(scene, "Análisis de complejidad")
    puntos = lista_puntos([
        "• Cada nodo se extrae una vez y cada arista se relaja a lo más una vez.",
        "   Insertar / quitar de un bucket (lista doblemente enlazada) es O(1)  ⇒  O(|E|).",
        "• El puntero solo avanza: llega a lo más a la mayor distancia ≤ C·(|V| − 1)",
        "   ⇒  O(C·|V|) revisiones de buckets vacíos.",
    ], size=25, buff=0.22).next_to(t, DOWN, buff=0.45)
    total = texto("Tiempo: O(|E| + C·|V|)        Memoria extra: O(|V| + C)", 32,
                  color=C_FINAL, weight=BOLD).next_to(puntos, DOWN, buff=0.45)
    scene.play(LaggedStart(*[FadeIn(p) for p in puntos], lag_ratio=0.4), run_time=3)
    scene.play(Write(total), run_time=1.5)
    scene.wait(2)

    tabla = VGroup(
        texto("Dijkstra (heap binario)", 24), texto("O((|V| + |E|) log |V|)", 24),
        texto("Dial (buckets)", 24, color=C_ARBOL), texto("O(|E| + C·|V|)", 24, color=C_ARBOL),
    ).arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.25), col_alignments="lr")
    nota = texto("Conviene cuando C es pequeño. Si C es enorme (p. ej. 10⁹), el puntero\n"
                 "recorre demasiados buckets vacíos y Dijkstra es mejor.", 22, color=GREY_B)
    r = traza.result
    real = texto(f"En nuestro ejemplo: |V| = {traza.n}, |E| = {len(traza.edges)}, C = {traza.C}  →  "
                 f"{r['bucket_scans']} avances del puntero, {r['relaxations']} relajaciones",
                 22, color=C_COLA)
    VGroup(tabla, nota, real).arrange(DOWN, buff=0.35).next_to(total, DOWN, buff=0.45)
    scene.play(FadeIn(tabla, shift=UP * 0.2), run_time=1.2)
    scene.play(FadeIn(nota), run_time=1)
    scene.play(FadeIn(real), run_time=1)
    scene.wait(4)
    limpiar(scene)


class EscenaComplejidad(Scene):
    def construct(self):
        complejidad(self, cargar_traza("ejemplo"))
