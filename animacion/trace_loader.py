"""Carga la traza JSON generada por el programa en C++ (build/dial).

La animacion NO calcula nada por su cuenta: cada paso que se muestra sale de
la ejecucion real del algoritmo implementado en src/dial.cpp.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
TRAZAS = RAIZ / "trazas"

_CANDIDATOS = [
    RAIZ / "build" / "dial.exe",
    RAIZ / "build" / "dial",
    RAIZ / "build" / "Release" / "dial.exe",
    RAIZ / "build" / "Debug" / "dial.exe",
]


@dataclass
class Traza:
    n: int
    source: int
    C: int
    B: int
    nodes: list
    edges: list
    events: list
    result: dict

    def arista(self, eid: int) -> dict:
        return self.edges[eid]


def _binario() -> Path | None:
    return next((c for c in _CANDIDATOS if c.exists()), None)


def cargar_traza(nombre: str) -> Traza:
    """Ejecuta build/dial sobre data/<nombre>.txt y lee trazas/<nombre>.json."""
    entrada = DATA / f"{nombre}.txt"
    salida = TRAZAS / f"{nombre}.json"
    exe = _binario()
    if exe is not None:
        TRAZAS.mkdir(exist_ok=True)
        subprocess.run([str(exe), str(entrada), str(salida)], check=True,
                       capture_output=True, text=True)
    elif not salida.exists():
        raise FileNotFoundError(
            "No se encontro build/dial. Compila primero el codigo C++:\n"
            "  cmake -S . -B build && cmake --build build --config Release")
    with open(salida, encoding="utf-8") as f:
        d = json.load(f)
    return Traza(d["n"], d["source"], d["C"], d["B"], d["nodes"], d["edges"],
                 d["events"], d["result"])
