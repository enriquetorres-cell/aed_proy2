"""Dibujo del arreglo circular de buckets y del puntero de distancia actual."""
from manim import *

from comun import C_CAJA, C_COLA, C_PUNTERO, texto


class BucketView(VGroup):
    def __init__(self, B, centro=DOWN * 2.35, ancho=1.05, alto=1.2):
        super().__init__()
        self.B = B
        self.alto = alto
        self.ancho = min(ancho, 12.0 / B - 0.15)

        self.cajas = VGroup(*[
            Rectangle(width=self.ancho, height=alto, stroke_color=C_CAJA, stroke_width=3)
            for _ in range(B)
        ]).arrange(RIGHT, buff=0.15).move_to(centro)
        self.indices = VGroup(*[
            texto(str(b), 20, color=GREY_B).next_to(self.cajas[b], UP, buff=0.08)
            for b in range(B)
        ])
        self.titulo = texto(f"Buckets  (índice = d mod {B})", 22).next_to(
            self.cajas, LEFT, buff=0.35)
        if self.titulo.get_left()[0] < -6.9:
            self.titulo.next_to(self.indices, UP, buff=0.1).align_to(self.cajas, LEFT)

        self.puntero = Arrow(DOWN * 0.5, ORIGIN, buff=0, color=C_PUNTERO, stroke_width=6,
                             tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        self.puntero.next_to(self.cajas[0], DOWN, buff=0.06)
        self.texto_d = self._texto_puntero(0)

        self.add(self.cajas, self.indices, self.titulo, self.puntero, self.texto_d)
        self.contenido = [VGroup() for _ in range(B)]
        self.estado = [[] for _ in range(B)]

    def _texto_puntero(self, d):
        return texto(f"d = {d}  (bucket {d % self.B})", 22, color=C_PUNTERO).next_to(
            self.puntero, RIGHT, buff=0.12)

    def _fichas(self, b, nodos):
        g = VGroup()
        for v in nodos:
            c = Circle(radius=0.2, fill_color=C_COLA, fill_opacity=1,
                       stroke_color=WHITE, stroke_width=2)
            g.add(VGroup(c, texto(str(v), 20, color=BLACK, weight=BOLD).move_to(c)))
        if len(g):
            cols = 1 if len(nodos) <= 2 else 2
            g.arrange_in_grid(cols=cols, buff=0.08)
            if g.height > self.alto - 0.12:
                g.scale_to_fit_height(self.alto - 0.12)
            if g.width > self.ancho - 0.12:
                g.scale_to_fit_width(self.ancho - 0.12)
            g.move_to(self.cajas[b])
        return g

    def actualizar(self, buckets):
        """Animaciones para que el dibujo refleje el snapshot de la traza."""
        anims = []
        for b in range(self.B):
            if buckets[b] != self.estado[b]:
                viejo, nuevo = self.contenido[b], self._fichas(b, buckets[b])
                if len(viejo):
                    anims.append(FadeOut(viejo))
                if len(nuevo):
                    anims.append(FadeIn(nuevo))
                self.contenido[b] = nuevo
                self.estado[b] = list(buckets[b])
        return anims

    def centro_caja(self, b):
        return self.cajas[b].get_center()

    def mover_puntero(self, d):
        b = d % self.B
        destino = self.puntero.copy().next_to(self.cajas[b], DOWN, buff=0.06)
        nuevo_texto = texto(f"d = {d}  (bucket {b})", 22, color=C_PUNTERO).next_to(
            destino, RIGHT, buff=0.12)
        anims = [self.puntero.animate.move_to(destino), Transform(self.texto_d, nuevo_texto)]
        for i, caja in enumerate(self.cajas):
            color = C_PUNTERO if i == b else C_CAJA
            anims.append(caja.animate.set_stroke(color, width=5 if i == b else 3))
        return anims
