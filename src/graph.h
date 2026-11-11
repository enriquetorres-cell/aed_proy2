#pragma once
// Grafo dirigido y ponderado con pesos enteros no negativos.
// Representacion: lista de adyacencia que guarda los ids de las aristas salientes.

#include <string>
#include <vector>

struct Edge {
    int from;
    int to;
    int w;
};

struct Point {
    double x;
    double y;
};

class Graph {
public:
    explicit Graph(int n = 0);

    // Agrega la arista dirigida u -> v con peso w (w >= 0). Devuelve su id.
    int addEdge(int u, int v, int w);

    int size() const { return static_cast<int>(adj_.size()); }
    int edgeCount() const { return static_cast<int>(edges_.size()); }

    // C = peso maximo de las aristas (0 si no hay aristas).
    int maxWeight() const { return maxW_; }

    const std::vector<int>& out(int u) const { return adj_[u]; }
    const Edge& edge(int id) const { return edges_[id]; }
    const std::vector<Edge>& edges() const { return edges_; }

    // Posiciones opcionales de los nodos (solo para la animacion).
    std::vector<Point> pos;

    // Lee un grafo desde archivo. Formato (lineas con '#' son comentarios):
    //   n m s          -> nodos, aristas, nodo origen
    //   u v w          -> m lineas, arista dirigida u->v con peso w
    //   pos            -> (opcional) palabra clave seguida de n lineas "x y"
    static Graph fromFile(const std::string& path, int& source);

private:
    std::vector<std::vector<int>> adj_;
    std::vector<Edge> edges_;
    int maxW_ = 0;
};
