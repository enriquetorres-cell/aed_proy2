"""Colores, textos y utilidades compartidas por todas las escenas."""
from manim import *

# Paleta de estados de un nodo
C_PENDIENTE = "#9aa0a6"   # dist = infinito, aun no descubierto
C_COLA = "#ffd166"        # esta en algun bucket (distancia tentativa)
C_ACTUAL = "#f4845f"      # se esta procesando (recien extraido)
C_FINAL = "#06d6a0"       # distancia definitiva
C_INALCANZABLE = "#ef476f"

# Aristas y buckets
C_ARISTA = "#6c757d"
C_RESALTE = "#ffd166"
C_ARBOL = "#4cc9f0"       # arista del arbol de caminos minimos
C_CAJA = "#adb5bd"
C_PUNTERO = "#4cc9f0"
C_DIST = "#ffd166"


def texto(s, size=28, color=WHITE, **kw):
    return Text(s, font_size=size, color=color, **kw)


def fmt_dist(d):
    return "∞" if d is None else str(d)


def limpiar(scene, run_time=0.6):
    """Hace FadeOut de todo lo que hay en pantalla."""
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)


def titulo_seccion(scene, s, size=40):
    t = texto(s, size, weight=BOLD).to_edge(UP, buff=0.4)
    scene.play(Write(t), run_time=0.8)
    return t


def lista_puntos(lineas, size=28, buff=0.3):
    """VGroup de lineas alineadas a la izquierda.
    Una linea que empieza con espacios se dibuja con sangria; "" deja un espacio en blanco."""
    filas, sangria = [], []
    for l in lineas:
        if l.strip():
            filas.append(texto(l.strip(), size))
        else:  # Text("") no tiene altura: usamos un espaciador invisible
            filas.append(Rectangle(width=0.1, height=size / 100, stroke_opacity=0, fill_opacity=0))
        sangria.append(l.startswith(" "))
    g = VGroup(*filas).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    for fila, s in zip(filas, sangria):
        if s:
            fila.shift(RIGHT * 0.45)
    if g.width > 12.8:
        g.scale_to_fit_width(12.8)
    return g


def leyenda():
    """Leyenda de colores de los nodos."""
    items = [("sin descubrir (∞)", C_PENDIENTE), ("en un bucket", C_COLA),
             ("procesando", C_ACTUAL), ("definitivo", C_FINAL)]
    filas = VGroup()
    for nombre, color in items:
        punto = Circle(radius=0.1, fill_color=color, fill_opacity=1, stroke_width=1, stroke_color=WHITE)
        filas.add(VGroup(punto, texto(nombre, 18)).arrange(RIGHT, buff=0.12))
    return filas.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.12), col_alignments="ll")
