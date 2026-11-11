#pragma once
// Algoritmo de Dial: caminos minimos desde un origen en grafos con pesos
// enteros en [0, C]. Complejidad O(|E| + C*|V|) tiempo, O(|V| + C) memoria extra.

#include <limits>
#include <vector>

#include "bucket_queue.h"
#include "graph.h"

constexpr long long INF = std::numeric_limits<long long>::max();

enum class EventType {
    Init,          // se inserta el origen con distancia 0
    ScanEmpty,     // el bucket actual esta vacio: se avanza el puntero
    Extract,       // se extrae u del bucket actual: dist[u] es definitiva
    ConsiderEdge,  // se revisa la arista u -> v
    Relax,         // dist[v] mejora: v se mueve de bucket
    NoRelax,       // la arista no mejora dist[v]
    Done           // la cola quedo vacia
};

struct DialEvent {
    EventType type;
    int u = -1;
    int v = -1;
    int edge = -1;
    long long cursor = 0;   // distancia que se esta procesando (puntero)
    int bucket = -1;        // bucket involucrado (destino en Relax)
    int fromBucket = -1;    // en Relax: bucket anterior de v (-1 si era INF)
    long long oldDist = INF;
    long long newDist = INF;
};

// Vista de solo lectura del estado interno, entregada al observador.
struct DialState {
    const Graph& g;
    int source;
    int C;
    const std::vector<long long>& dist;
    const std::vector<int>& parent;
    const std::vector<bool>& done;
    const BucketQueue& bq;
};

// Patron observador: permite generar la traza para la animacion sin
// mezclar codigo de visualizacion dentro del algoritmo.
class DialObserver {
public:
    virtual ~DialObserver() = default;
    virtual void onEvent(const DialEvent& e, const DialState& s) = 0;
};

struct DialResult {
    std::vector<long long> dist;  // INF si el nodo es inalcanzable
    std::vector<int> parent;      // -1 para el origen o inalcanzables
    int C = 0;
    long long bucketScans = 0;    // veces que el puntero avanzo
    long long relaxations = 0;
};

DialResult dial(const Graph& g, int source, DialObserver* observer = nullptr);

// Reconstruye el camino origen -> v (vacio si v es inalcanzable).
std::vector<int> buildPath(const DialResult& r, int v);
