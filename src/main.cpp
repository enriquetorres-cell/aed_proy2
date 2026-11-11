// Uso: dial <grafo.txt> [traza.json]
// Ejecuta el algoritmo de Dial, imprime distancias y caminos, y opcionalmente
// guarda la traza paso a paso que usa la animacion.

#include <iostream>

#include "dial.h"
#include "tracer.h"

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Uso: " << argv[0] << " <grafo.txt> [traza.json]\n";
        return 1;
    }
    try {
        int source = 0;
        Graph g = Graph::fromFile(argv[1], source);

        JsonTracer tracer;
        DialResult r = dial(g, source, argc >= 3 ? &tracer : nullptr);

        std::cout << "Algoritmo de Dial  |V|=" << g.size() << "  |E|=" << g.edgeCount()
                  << "  C=" << r.C << "  buckets=" << (r.C + 1) << "  origen=" << source << "\n";
        for (int v = 0; v < g.size(); ++v) {
            std::cout << "  dist[" << v << "] = ";
            if (r.dist[v] == INF) {
                std::cout << "INF (inalcanzable)\n";
                continue;
            }
            std::cout << r.dist[v] << "   camino:";
            for (int x : buildPath(r, v)) std::cout << ' ' << x;
            std::cout << '\n';
        }
        std::cout << "Avances del puntero: " << r.bucketScans
                  << "  Relajaciones: " << r.relaxations << "\n";

        if (argc >= 3) {
            tracer.write(argv[2], g, source, r);
            std::cout << "Traza guardada en " << argv[2] << "\n";
        }
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << "\n";
        return 1;
    }
    return 0;
}
