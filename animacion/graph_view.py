"""Dibujo del grafo dirigido y ponderado (nodos, aristas, pesos y distancias)."""
import numpy as np
from manim import *

from comun import (C_ARISTA, C_DIST, C_PENDIENTE, fmt_dist, texto)


class GraphView(VGroup):
    def __init__(self, traza, caja=(-6.6, -1.0, 1.5, 2.7), radio=0.33):
        super().__init__()
        self.traza = traza
        self.radio = radio
        x0, y0, x1, y1 = caja
        self.centro = np.array([(x0 + x1) / 2, (y0 + y1) / 2, 0.0])

        self.pos = self._posiciones(traza, x0, y0, x1, y1)
        self.flechas, self.pesos = {}, {}
        self.circulos, self.ids, self.dists = {}, {}, {}

        pares = {(e["u"], e["v"]) for e in traza.edges}
        for e in traza.edges:
            self._crear_arista(e, (e["v"], e["u"]) in pares)
        for nd in traza.nodes:
            self._crear_nodo(nd["id"])

        self.add(*self.flechas.values(), *self.pesos.values())
        for i in self.circulos:
            self.add(self.circulos[i], self.ids[i], self.dists[i])

    # ---------- construccion ----------
    def _posiciones(self, traza, x0, y0, x1, y1):
        n = traza.n
        if all("x" in nd for nd in traza.nodes):
            pts = np.array([[nd["x"], nd["y"]] for nd in traza.nodes], dtype=float)
        else:  # sin posiciones: nodos en circulo
            ang = [2 * np.pi * i / n for i in range(n)]
            pts = np.array([[np.cos(a), np.sin(a)] for a in ang])
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        span = np.maximum(hi - lo, 1e-9)
        margen = self.radio + 0.45
        escala = min((x1 - x0 - 2 * margen) / span[0], (y1 - y0 - 2 * margen) / span[1], 2.5)
        medio = (lo + hi) / 2
        return [np.array([*(p - medio) * escala, 0.0]) + self.centro for p in pts]

    def _crear_arista(self, e, hay_reversa):
        p, q = self.pos[e["u"]], self.pos[e["v"]]
        if e["u"] == e["v"]:  # auto-lazo
            flecha = CurvedArrow(p + UL * self.radio * 0.8, p + UR * self.radio * 0.8,
                                 angle=-4, color=C_ARISTA, stroke_width=3, tip_length=0.15)
            etiqueta_pos = p + UP * (self.radio + 0.55)
        else:
            d = (q - p) / np.linalg.norm(q - p)
            perp = np.array([-d[1], d[0], 0.0])
            off = perp * 0.13 if hay_reversa else 0
            flecha = Arrow(p + off, q + off, buff=self.radio + 0.02, color=C_ARISTA,
                           stroke_width=3, tip_length=0.2,
                           max_tip_length_to_length_ratio=0.25,
                           max_stroke_width_to_length_ratio=12)
            etiqueta_pos = (p + q) / 2 + off + perp * 0.27
        peso = texto(str(e["w"]), 24).move_to(etiqueta_pos)
        self.flechas[e["id"]] = flecha
        self.pesos[e["id"]] = peso

    def _crear_nodo(self, i):
        c = Circle(radius=self.radio, fill_color=C_PENDIENTE, fill_opacity=1,
                   stroke_color=WHITE, stroke_width=3).move_to(self.pos[i])
        self.circulos[i] = c
        self.ids[i] = texto(str(i), 28, color=BLACK, weight=BOLD).move_to(c)
        self.dists[i] = self._texto_dist(i, None)

    def _texto_dist(self, i, d):
        direccion = self.pos[i] - self.centro
        norma = np.linalg.norm(direccion)
        direccion = UP if norma < 1e-6 else direccion / norma
        return texto(fmt_dist(d), 26, color=C_DIST, weight=BOLD).move_to(
            self.pos[i] + direccion * (self.radio + 0.32))

    # ---------- animaciones ----------
    def anim_color(self, i, color):
        return self.circulos[i].animate.set_fill(color)

    def anim_borde(self, i, color, ancho=3):
        return self.circulos[i].animate.set_stroke(color, width=ancho)

    def anim_dist(self, i, d):
        return Transform(self.dists[i], self._texto_dist(i, d))

    def anim_arista(self, eid, color, ancho=3):
        return self.flechas[eid].animate.set_color(color).set_stroke(width=ancho)

    def ficha(self, i):
        """Copia del nodo (circulo + id), util para animarlo viajando a un bucket."""
        return VGroup(self.circulos[i].copy(), self.ids[i].copy())
