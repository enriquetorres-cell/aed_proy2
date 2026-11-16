# Algoritmo de Dial — Anima tu Algoritmo

**CS2023 - Algoritmos y Estructuras de Datos (UTEC 2026-2)** · Proyecto Final 2
Prof. Víctor Racsó Galván Oyola

Integrantes (Sección 3):
- Choque Coaquira, Rafael Rodrigo
- Maguiña Quispe, Paul Ricardo
- Torres Chafloque, Enrique Eusebio

📹 **Video:** _(pegar aquí el enlace al video)_ · 📄 **Informe:** `informe/Informe_Algoritmo_de_Dial.pdf`

Video educativo, estilo 3Blue1Brown/Manim, que explica el **algoritmo de Dial**:
caminos mínimos desde un origen en grafos dirigidos con pesos enteros en `[0, C]`,
en tiempo `O(|E| + C·|V|)`, usando un arreglo circular de `C + 1` buckets en lugar del heap de Dijkstra.

## ¿Cómo está hecho? (la animación es real, no simulada)

```
data/*.txt ──► build/dial (C++17) ──► trazas/*.json ──► animacion/*.py (Manim) ──► video .mp4
               algoritmo real          cada paso:         dibuja cada evento
               + JsonTracer            extract, relax,    de la traza
                                       buckets, dist...
```

1. **`src/` (C++)**: implementación propia del algoritmo y de la cola de buckets
   (`BucketQueue`: listas doblemente enlazadas sobre arreglos, insertar/eliminar/extraer en O(1)).
   No se usa `std::priority_queue` ni ninguna estructura de terceros.
2. Un observador (`JsonTracer`) registra **cada evento** de la ejecución (inicio, bucket vacío,
   extracción, arista revisada, relajación, fin) junto con el estado completo
   (`dist`, `padre`, contenido de los buckets) y lo guarda en JSON.
3. **`animacion/` (Python + Manim)**: lee esa traza y anima paso a paso. La animación no calcula
   distancias: todo lo que se ve sale de la ejecución del programa en C++.

## Estructura

| Ruta | Contenido |
|---|---|
| `src/graph.*` | Grafo dirigido ponderado + lectura desde archivo |
| `src/bucket_queue.*` | Cola de buckets circular (implementación propia) |
| `src/dial.*` | Algoritmo de Dial con eventos (patrón observador) |
| `src/tracer.*` | Exporta la traza de ejecución a JSON |
| `src/main.cpp` | CLI: `dial <grafo.txt> [traza.json]` |
| `tests/test_dial.cpp` | Pruebas: Dial vs Bellman-Ford en 500 grafos aleatorios + casos borde |
| `tests/benchmark.cpp` | Comparación empírica de tiempos: Dial vs Dijkstra (heap binario) variando C |
| `data/ejemplo.txt` | Instancia ilustrativa del video (6 nodos, C = 4) |
| `data/borde.txt` | Caso borde: arista de peso 0 y nodo inalcanzable |
| `animacion/graph_view.py`, `bucket_view.py` | Dibujo del grafo y de los buckets |
| `animacion/escena_demo.py` | Demostración animada de la ejecución |
| `animacion/escena_intro.py` | Portada, introducción conceptual y créditos |
| `animacion/escena_borde.py` | Caso borde |
| `animacion/escena_complejidad.py` | Análisis de complejidad |
| `animacion/video_completo.py` | Une todo en un solo video |

## Software requerido

- Compilador C++17 (g++ / MinGW, clang o MSVC) y **CMake ≥ 3.16**
- **Python 3.9+** y **Manim Community** (`pip install -r requirements.txt`).
  No se necesita LaTeX (solo se usa `Text`). En Linux, Manim necesita además `libcairo2-dev` y `libpango1.0-dev`.

## Compilar y ejecutar

```bash
# 1) Compilar el código C++ y correr las pruebas
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release     # en Windows con MinGW: agregar -G "MinGW Makefiles"
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure

# 2) Ejecutar el algoritmo (imprime distancias y caminos, y guarda la traza)
./build/dial data/ejemplo.txt trazas/ejemplo.json

# 3) Instalar Manim y renderizar el video
pip install -r requirements.txt
manim -qh animacion/video_completo.py VideoCompleto     # 1080p60
# resultado: media/videos/video_completo/1080p60/VideoCompleto.mp4
```

O todo de una vez: `.\render.ps1` (Windows) o `./render.sh` (Linux/macOS), que deja el video en
`video/AlgoritmoDeDial.mp4`. Para una prueba rápida en baja calidad: `.\render.ps1 -Rapido` / `./render.sh rapido`.

Cada parte del video también se puede renderizar sola:

```bash
manim -pql animacion/escena_intro.py EscenaIntro
manim -pql animacion/escena_demo.py EscenaDemo
manim -pql animacion/escena_borde.py EscenaBorde
manim -pql animacion/escena_complejidad.py EscenaComplejidad
```

## Formato de los grafos (`data/*.txt`)

```
# comentarios con '#'
n m s        # nodos, aristas, origen
u v w        # m líneas: arista dirigida u -> v con peso entero w >= 0
pos          # (opcional) n líneas "x y" con la posición de cada nodo en el dibujo
```

`C` se calcula automáticamente como el peso máximo. Puedes crear tus propios grafos y
animarlos cambiando el nombre en `cargar_traza("...")`.

## Complejidad

- Cada relajación inserta/quita un nodo de un bucket en O(1) → **O(|E|)**.
- El puntero solo avanza y llega a lo más a la distancia máxima ≤ C·(|V|−1) → **O(C·|V|)**.
- Total **O(|E| + C·|V|)** de tiempo y **O(|V| + C)** de memoria extra (buckets circulares).

Comparación empírica (`./build/benchmark`, |V| = 100 000, |E| = 500 000, mismo grafo, mejor de 3):

| C | Dial (ms) | Dijkstra (ms) | Avances del puntero |
|---:|---:|---:|---:|
| 1 | 45.2 | 59.9 | 3 |
| 100 | 46.5 | 58.5 | 398 |
| 10 000 | 48.4 | 63.7 | 38 453 |
| 1 000 000 | 71.5 | 58.9 | 4 004 011 |

Con C pequeño Dial gana; cuando C crece, el puntero recorre millones de buckets vacíos y Dijkstra pasa adelante.
(Los tiempos dependen de la máquina; las distancias de ambos algoritmos coinciden en todos los casos.)

## Referencias

- R. B. Dial (1969). *Algorithm 360: Shortest-path forest with topological ordering*. Communications of the ACM, 12(11), 632–633.
- Manim Community: https://docs.manim.community/ · Estilo inspirado en 3Blue1Brown.
