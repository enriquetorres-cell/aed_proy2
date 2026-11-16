"""Video final completo (una sola escena -> un solo .mp4).
Render final:  manim -qh animacion/video_completo.py VideoCompleto
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from comun import limpiar
from escena_borde import caso_borde
from escena_complejidad import complejidad
from escena_demo import demo_dial
from escena_intro import creditos, intro
from trace_loader import cargar_traza


class VideoCompleto(Scene):
    def construct(self):
        ejemplo = cargar_traza("ejemplo")
        intro(self)                 
        demo_dial(self, ejemplo)    
        limpiar(self)
        caso_borde(self)            
        limpiar(self)
        complejidad(self, ejemplo)  
        creditos(self)
