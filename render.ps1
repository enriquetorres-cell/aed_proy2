# Compila el C++, corre las pruebas y genera el video final en video/AlgoritmoDeDial.mp4
# Uso (PowerShell, desde la raiz del repo):  .\render.ps1        (alta calidad 1080p60)
#                                            .\render.ps1 -Rapido (480p15, para probar)
param([switch]$Rapido)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (Get-Command g++ -ErrorAction SilentlyContinue) {
    cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
} else {
    cmake -S . -B build
}
if ($LASTEXITCODE -ne 0) { exit 1 }
cmake --build build --config Release
if ($LASTEXITCODE -ne 0) { exit 1 }
ctest --test-dir build -C Release --output-on-failure
if ($LASTEXITCODE -ne 0) { exit 1 }

if ($Rapido) { $calidad = "-ql"; $carpeta = "480p15" } else { $calidad = "-qh"; $carpeta = "1080p60" }
manim $calidad animacion/video_completo.py VideoCompleto
if ($LASTEXITCODE -ne 0) { exit 1 }

New-Item -ItemType Directory -Force video | Out-Null
Copy-Item "media/videos/video_completo/$carpeta/VideoCompleto.mp4" "video/AlgoritmoDeDial.mp4" -Force
Write-Host "Video listo: video/AlgoritmoDeDial.mp4"
