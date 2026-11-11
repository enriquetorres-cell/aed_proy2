"""Demostracion animada de la ejecucion del algoritmo de Dial.

Cada animacion corresponde a un evento de la traza producida por build/dial.
Render individual:  manim -pql animacion/escena_demo.py EscenaDemo
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from bucket_view import BucketView
from comun import (C_ACTUAL, C_ARBOL, C_ARISTA, C_COLA, C_FINAL, C_INALCANZABLE,
                   C_RESALTE, fmt_dist, leyenda, texto)
from graph_view import GraphView
from trace_loader import cargar_traza


class Panel:
    """Recuadro a la derecha con el numero de paso y la explicacion."""

    def __init__(self, total):
        self.total = total
        self.marco = RoundedRectangle(width=5.0, height=3.7, corner_radius=0.15,
                                      stroke_color=GREY_D).move_to([4.45, 0.85, 0])
        self.paso = texto(f"Paso 0 / {total}", 22, color=GREY_B).move_to(
            self.marco.get_top() + DOWN * 0.3)
        self.cuerpo = VGroup()
        self.leyenda = leyenda().scale(0.95).move_to(self.marco.get_bottom() + UP * 0.45)
        self.grupo = VGroup(self.marco, self.paso, self.leyenda)

    def cambiar(self, k, mensaje):
        nuevo = texto(mensaje, 22, line_spacing=0.8)
        if nuevo.width > self.marco.width - 0.4:
            nuevo.scale_to_fit_width(self.marco.width - 0.4)
        nuevo.move_to(self.marco.get_center() + UP * 0.15)
        nuevo_paso = texto(f"Paso {k} / {self.total}", 22, color=GREY_B).move_to(self.paso)
        anims = [FadeIn(nuevo, shift=UP * 0.1), Transform(self.paso, nuevo_paso)]
        if len(self.cuerpo):
            anims.append(FadeOut(self.cuerpo, shift=UP * 0.1))
        self.cuerpo = nuevo
        return anims


def demo_dial(scene, traza, titulo="Demostración: ejecución del algoritmo", rt=1.0):
    """Anima todos los eventos de la traza sobre `scene`. rt escala la duracion."""
    cab = texto(titulo, 34, weight=BOLD).to_edge(UP, buff=0.3)
    info = texto(f"|V| = {traza.n}    |E| = {len(traza.edges)}    C = {traza.C}  →  "
                 f"{traza.B} buckets    origen = {traza.source}", 22, color=GREY_B
                 ).next_to(cab, DOWN, buff=0.12)
    grafo = GraphView(traza)
    buckets = BucketView(traza.B)
    panel = Panel(len(traza.events))

    scene.play(Write(cab), FadeIn(info), run_time=0.8 * rt)
    scene.play(Create(grafo), run_time=1.5 * rt)
    scene.play(FadeIn(buckets), FadeIn(panel.grupo), run_time=0.8 * rt)

    actual = None
    arista_arbol = {}  # v -> id de la arista que le dio su distancia actual

    for k, ev in enumerate(traza.events, 1):
        t = ev["type"]
        extra = []
        if t in ("extract", "scan_empty", "done") and actual is not None:
            extra.append(grafo.anim_color(actual, C_FINAL))
            actual = None

        if t == "init":
            s = ev["u"]
            msg = (f"Inicio: dist[{s}] = 0,\nel resto de distancias = ∞.\n"
                   f"Se inserta {s} en el bucket 0.")
            scene.play(*panel.cambiar(k, msg), grafo.anim_color(s, C_COLA), grafo.anim_dist(s, 0),
                       *buckets.actualizar(ev["buckets"]), *buckets.mover_puntero(0),
                       run_time=1.3 * rt)

        elif t == "scan_empty":
            b, d = ev["bucket"], ev["cursor"]
            msg = (f"Bucket {b} vacío: no quedan nodos\ncon distancia {d}.\n"
                   f"Avanzamos el puntero a d = {d + 1}.")
            scene.play(*panel.cambiar(k, msg), Indicate(buckets.cajas[b], color=C_INALCANZABLE),
                       *extra, run_time=0.8 * rt)
            scene.play(*buckets.mover_puntero(d + 1), run_time=0.6 * rt)

        elif t == "extract":
            u, b, d = ev["u"], ev["bucket"], ev["cursor"]
            msg = (f"Extraemos {u} del bucket {b}  (d = {d}).\n"
                   f"dist[{u}] = {d} ya es definitiva.\nRevisamos sus aristas salientes.")
            scene.play(*panel.cambiar(k, msg), grafo.anim_color(u, C_ACTUAL),
                       *buckets.actualizar(ev["buckets"]), *extra, run_time=1.0 * rt)
            actual = u

        elif t == "consider_edge":
            scene.play(grafo.anim_arista(ev["edge"], C_RESALTE, 6), run_time=0.4 * rt)

        elif t == "relax":
            u, v, eid = ev["u"], ev["v"], ev["edge"]
            w, du, nd = traza.arista(eid)["w"], ev["dist"][u], ev["new"]
            b, fb = ev["bucket"], ev["from_bucket"]
            mov = (f"{v} se mueve del bucket {fb} al {b}" if fb >= 0
                   else f"{v} entra al bucket {b}")
            msg = (f"Arista {u} → {v}  (peso {w}):\n{du} + {w} = {nd} < {fmt_dist(ev['old'])}\n"
                   f"dist[{v}] = {nd},  padre[{v}] = {u}\n{mov}\n({nd} mod {traza.B} = {b})")
            if v in arista_arbol:
                extra.append(grafo.anim_arista(arista_arbol[v], C_ARISTA, 3))
            arista_arbol[v] = eid
            ficha = grafo.ficha(v)
            scene.add(ficha)
            scene.play(*panel.cambiar(k, msg), grafo.anim_dist(v, nd), grafo.anim_color(v, C_COLA),
                       grafo.anim_arista(eid, C_ARBOL, 5),
                       ficha.animate.scale(0.6).move_to(buckets.centro_caja(b)),
                       *extra, run_time=1.2 * rt)
            scene.play(FadeOut(ficha), *buckets.actualizar(ev["buckets"]), run_time=0.5 * rt)

        elif t == "no_relax":
            u, v, eid = ev["u"], ev["v"], ev["edge"]
            w, du = traza.arista(eid)["w"], ev["dist"][u]
            msg = (f"Arista {u} → {v}  (peso {w}):\n{du} + {w} = {ev['new']} ≥ "
                   f"{fmt_dist(ev['old'])}\nNo mejora: se ignora.")
            scene.play(*panel.cambiar(k, msg), grafo.anim_arista(eid, C_INALCANZABLE, 5),
                       run_time=0.8 * rt)
            scene.play(grafo.anim_arista(eid, C_ARISTA, 3), run_time=0.3 * rt)

        elif t == "done":
            inalc = [i for i, d in enumerate(ev["dist"]) if d is None]
            msg = "La cola de buckets quedó vacía.\nFin: todas las distancias\nson mínimas."
            if inalc:
                msg += f"\nInalcanzables: {', '.join(map(str, inalc))}  (dist = ∞)"
                extra += [grafo.anim_borde(i, C_INALCANZABLE, 6) for i in inalc]
            scene.play(*panel.cambiar(k, msg), *extra, run_time=1.2 * rt)

        scene.wait(0.15 * rt)

    # Resumen final: en azul queda el arbol de caminos minimos.
    dist = traza.result["dist"]
    resumen = texto("dist = [" + ", ".join(fmt_dist(d) for d in dist) + "]", 26,
                    color=C_FINAL).next_to(grafo, DOWN, buff=0.05).align_to(grafo, LEFT)
    nota = texto("en azul: árbol de caminos mínimos", 20, color=C_ARBOL).next_to(
        resumen, RIGHT, buff=0.4)
    scene.play(FadeIn(resumen), FadeIn(nota), run_time=0.8 * rt)
    scene.wait(2 * rt)


class EscenaDemo(Scene):
    def construct(self):
        demo_dial(self, cargar_traza("ejemplo"))
