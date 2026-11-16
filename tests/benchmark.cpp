// Comparacion empirica: Dial (buckets) vs Dijkstra con heap binario.
// Mismo grafo aleatorio, distintos valores de C. Verifica que ambos den las
// mismas distancias y mide el tiempo y los avances del puntero de Dial.
// Uso: benchmark [n] [m]      (por defecto n = 100000, m = 500000)
//
// Nota: Dijkstra se usa solo como linea base; std::priority_queue NO se usa en Dial.

#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <queue>
#include <random>

#include "dial.h"

static std::vector<long long> dijkstra(const Graph& g, int s) {
    std::vector<long long> d(g.size(), INF);
    using P = std::pair<long long, int>;
    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;
    d[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != d[u]) continue;
        for (int id : g.out(u)) {
            const Edge& e = g.edge(id);
            if (du + e.w < d[e.to]) {
                d[e.to] = du + e.w;
                pq.push({d[e.to], e.to});
            }
        }
    }
    return d;
}

template <class F>
static double ms(F&& f) {
    auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main(int argc, char** argv) {
    const int n = argc > 1 ? std::atoi(argv[1]) : 100000;
    const int m = argc > 2 ? std::atoi(argv[2]) : 500000;
    std::printf("|V| = %d  |E| = %d\n", n, m);
    std::printf("%10s %12s %14s %16s %8s\n", "C", "Dial (ms)", "Dijkstra (ms)", "avances puntero", "iguales");

    for (int C : {1, 10, 100, 1000, 10000, 100000, 1000000}) {
        std::mt19937 rng(7);
        Graph g(n);
        for (int i = 1; i < n; ++i) g.addEdge(rng() % i, i, rng() % (C + 1));  // todos alcanzables
        for (int i = n - 1; i < m; ++i) g.addEdge(rng() % n, rng() % n, rng() % (C + 1));

        DialResult r;
        std::vector<long long> d;
        double tDial = 1e18, tDij = 1e18;
        for (int rep = 0; rep < 3; ++rep) {  // mejor de 3
            tDial = std::min(tDial, ms([&] { r = dial(g, 0); }));
            tDij = std::min(tDij, ms([&] { d = dijkstra(g, 0); }));
        }
        std::printf("%10d %12.1f %14.1f %16lld %8s\n", C, tDial, tDij, r.bucketScans,
                    r.dist == d ? "si" : "NO");
    }
    return 0;
}
