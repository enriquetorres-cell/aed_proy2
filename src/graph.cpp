#include "graph.h"

#include <fstream>
#include <sstream>
#include <stdexcept>

Graph::Graph(int n) : adj_(n) {}

int Graph::addEdge(int u, int v, int w) {
    if (u < 0 || u >= size() || v < 0 || v >= size())
        throw std::invalid_argument("arista con nodo fuera de rango");
    if (w < 0)
        throw std::invalid_argument("el algoritmo de Dial requiere pesos no negativos");
    int id = static_cast<int>(edges_.size());
    edges_.push_back({u, v, w});
    adj_[u].push_back(id);
    if (w > maxW_) maxW_ = w;
    return id;
}

Graph Graph::fromFile(const std::string& path, int& source) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error("no se pudo abrir " + path);

    // Quitamos comentarios y juntamos todo en un solo flujo de tokens.
    std::stringstream tokens;
    std::string line;
    while (std::getline(in, line)) {
        auto hash = line.find('#');
        if (hash != std::string::npos) line = line.substr(0, hash);
        tokens << line << '\n';
    }

    int n, m;
    if (!(tokens >> n >> m >> source)) throw std::runtime_error("cabecera invalida (n m s)");
    if (n <= 0) throw std::runtime_error("n debe ser positivo");
    if (source < 0 || source >= n) throw std::runtime_error("origen fuera de rango");

    Graph g(n);
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        if (!(tokens >> u >> v >> w)) throw std::runtime_error("faltan aristas en el archivo");
        g.addEdge(u, v, w);
    }

    std::string word;
    if (tokens >> word && word == "pos") {
        g.pos.resize(n);
        for (int i = 0; i < n; ++i)
            if (!(tokens >> g.pos[i].x >> g.pos[i].y))
                throw std::runtime_error("faltan posiciones de nodos");
    }
    return g;
}
