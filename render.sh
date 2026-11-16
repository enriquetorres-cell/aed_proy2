#!/usr/bin/env bash
# Compila el C++, corre las pruebas y genera el video final en video/AlgoritmoDeDial.mp4
# Uso:  ./render.sh          (alta calidad 1080p60)
#       ./render.sh rapido   (480p15, para probar)
set -euo pipefail
cd "$(dirname "$0")"

cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure

if [ "${1:-}" = "rapido" ]; then calidad=-ql; carpeta=480p15; else calidad=-qh; carpeta=1080p60; fi
manim "$calidad" animacion/video_completo.py VideoCompleto

mkdir -p video
cp "media/videos/video_completo/$carpeta/VideoCompleto.mp4" video/AlgoritmoDeDial.mp4
echo "Video listo: video/AlgoritmoDeDial.mp4"
