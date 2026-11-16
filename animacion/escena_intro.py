"""Titulo, introduccion conceptual y creditos.
Render individual:  manim -pql animacion/escena_intro.py EscenaIntro
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from comun import (C_ACTUAL, C_ARBOL, C_CAJA, C_COLA, C_FINAL, C_PUNTERO, limpiar,
                   lista_puntos, texto, titulo_seccion)
from config_video import CURSO, INTEGRANTES, PROFESOR, SUBTITULO, TITULO


def portada(scene):
    titulo = texto(TITULO, 72, weight=BOLD).set_color_by_gradient(C_ARBOL, C_FINAL)
    sub = texto(SUBTITULO, 32, color=GREY_B).next_to(titulo, DOWN, buff=0.3)
    curso = texto(CURSO, 22, color=GREY_B).next_to(sub, DOWN, buff=0.6)
    nombres = VGroup(*[texto(n, 26) for n in INTEGRANTES]).arrange(DOWN, buff=0.15)
    nombres.next_to(curso, DOWN, buff=0.45)
    VGroup(titulo, sub, curso, nombres).move_to(ORIGIN)
    scene.play(Write(titulo), run_time=1.5)
    scene.play(FadeIn(sub, shift=UP * 0.2))
    scene.play(FadeIn(curso), LaggedStart(*[FadeIn(n) for n in nombres], lag_ratio=0.3))
    scene.wait(2)
    limpiar(scene)


def problema(scene):
    t = titulo_seccion(scene, "¿Para qué sirve?")
    puntos = lista_puntos([
        "• Calcula los caminos mínimos desde un nodo origen s",
        "   hacia todos los demás nodos (single-source shortest paths).",
        "• Funciona en grafos dirigidos con pesos ENTEROS en el rango [0, C].",
        "• Ejemplos: redes viales con tiempos en minutos, routing de paquetes",
        "   con costos pequeños, mapas de juegos con costos por casilla.",
        "• Propuesto por Robert B. Dial en 1969.",
    ], size=28).next_to(t, DOWN, buff=0.6)
    scene.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in puntos], lag_ratio=0.4),
               run_time=4)
    scene.wait(3)
    limpiar(scene)


def _heap_dibujo():
    niveles = [[0], [-1.0, 1.0], [-1.5, -0.5, 0.5, 1.5]]
    nodos, lineas = VGroup(), VGroup()
    pos = []
    for y, fila in enumerate(niveles):
        pos.append([np.array([x, -y * 0.75, 0]) for x in fila])
    for y in range(1, 3):
        for i, p in enumerate(pos[y]):
            lineas.add(Line(pos[y - 1][i // 2], p, color=GREY))
    for fila in pos:
        for p in fila:
            nodos.add(Circle(radius=0.2, fill_color=C_COLA, fill_opacity=1,
                             stroke_color=WHITE, stroke_width=2).move_to(p))
    return VGroup(lineas, nodos)


def idea(scene):
    t = titulo_seccion(scene, "Idea: Dijkstra, pero sin heap")

    heap = _heap_dibujo()
    dijkstra = VGroup(texto("Dijkstra", 30, weight=BOLD), heap,
                      texto("min-heap: O(log V) por operación", 22, color=GREY_B)
                      ).arrange(DOWN, buff=0.3)
    cajas = VGroup(*[Square(0.55, stroke_color=C_CAJA) for _ in range(5)]).arrange(RIGHT, buff=0.08)
    idx = VGroup(*[texto(str(i), 18, color=GREY_B).next_to(c, UP, buff=0.06)
                   for i, c in enumerate(cajas)])
    flecha = Arrow(DOWN * 0.45, ORIGIN, buff=0, color=C_PUNTERO, stroke_width=5,
                   tip_length=0.18).next_to(cajas[0], DOWN, buff=0.05)
    dial = VGroup(texto("Dial", 30, weight=BOLD), VGroup(idx, cajas, flecha),
                  texto("buckets: O(1) por operación", 22, color=GREY_B)
                  ).arrange(DOWN, buff=0.3)
    VGroup(dijkstra, dial).arrange(RIGHT, buff=2.2).next_to(t, DOWN, buff=0.5)

    scene.play(FadeIn(dijkstra[0]), Create(heap), FadeIn(dijkstra[2]), run_time=1.5)
    scene.play(FadeIn(dial[0]), Create(cajas), FadeIn(idx), GrowArrow(flecha), FadeIn(dial[2]),
               run_time=1.5)
    for i in range(1, 5):
        scene.play(flecha.animate.next_to(cajas[i], DOWN, buff=0.05), run_time=0.3)
    scene.play(flecha.animate.next_to(cajas[0], DOWN, buff=0.05), run_time=0.5)

    pasos = lista_puntos([
        "1. Un nodo con distancia tentativa d se guarda en el bucket d mod (C+1).",
        "2. Un puntero recorre las distancias d = 0, 1, 2, ... en orden creciente.",
        "3. Se extraen los nodos del bucket actual: su distancia ya es definitiva.",
        "4. Al relajar u → v, v se saca de su bucket y pasa a otro en O(1).",
    ], size=24, buff=0.2).to_edge(DOWN, buff=0.5)
    scene.play(LaggedStart(*[FadeIn(p) for p in pasos], lag_ratio=0.5), run_time=3)
    scene.wait(3)
    limpiar(scene)

    t = titulo_seccion(scene, "¿Por qué bastan C + 1 buckets?")
    razon = lista_puntos([
        "Si estamos procesando la distancia d, toda distancia pendiente",
        "es a lo más d + C (venimos de un nodo con distancia ≤ d y una arista ≤ C).",
        "",
        "→ Las distancias pendientes están en [d, d + C]: son C + 1 valores,",
        "   y cada uno cae en un bucket distinto de d mod (C+1).",
        "→ El arreglo se usa de forma CIRCULAR: memoria O(V + C).",
    ], size=26).next_to(t, DOWN, buff=0.6)
    for i in (3, 4, 5):
        razon[i].set_color(C_FINAL)
    scene.play(FadeIn(razon, shift=UP * 0.2), run_time=1.5)
    scene.wait(4)
    limpiar(scene)


def creditos(scene):
    gracias = texto("¡Gracias!", 60, weight=BOLD).set_color_by_gradient(C_ARBOL, C_FINAL)
    nombres = VGroup(*[texto(n, 28) for n in INTEGRANTES]).arrange(DOWN, buff=0.15)
    curso = texto(CURSO + "\n" + PROFESOR, 20, color=GREY_B)
    ref = texto("Referencia: R. B. Dial (1969). Algorithm 360: Shortest-path forest with\n"
                "topological ordering. Communications of the ACM, 12(11), 632-633.\n"
                "Animación: Manim Community Edition  ·  Implementación: C++17",
                18, color=GREY_B)
    VGroup(gracias, nombres, curso, ref).arrange(DOWN, buff=0.45)
    scene.play(Write(gracias))
    scene.play(LaggedStart(*[FadeIn(n) for n in nombres], lag_ratio=0.3), FadeIn(curso))
    scene.play(FadeIn(ref))
    scene.wait(3)
    limpiar(scene, run_time=1)


def intro(scene):
    portada(scene)
    problema(scene)
    idea(scene)


class EscenaIntro(Scene):
    def construct(self):
        intro(self)


class EscenaCreditos(Scene):
    def construct(self):
        creditos(self)
