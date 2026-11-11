// Pruebas: compara Dial contra Bellman-Ford en grafos aleatorios y casos borde,
// y verifica invariantes de la cola de buckets.

#include <cstdlib>
#include <iostream>
#include <random>

#include "dial.h"

static int failures = 0;
#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            std::cerr << "FALLO " << __FILE__ << ":" << __LINE__ << "  " #cond "\n"; \
            ++failures;                                                          \
        }                                                                        \
    } while (0)

static std::vector<long long> bellmanFord(const Graph& g, int s) {
    std::vector<long long> d(g.size(), INF);
    d[s] = 0;
    for (int it = 0; it < g.size(); ++it)
        for (const Edge& e : g.edges())
            if (d[e.from] != INF && d[e.from] + e.w < d[e.to]) d[e.to] = d[e.from] + e.w;
    return d;
}

// Verifica que los nodos se extraen en orden no decreciente y que
// la distancia extraida coincide con el puntero.
struct InvariantChecker : DialObserver {
    long long last = -1;
    void onEvent(const DialEvent& e, const DialState& s) override {
        if (e.type == EventType::Extract) {
            CHECK(s.dist[e.u] == e.cursor);
            CHECK(e.cursor >= last);
            last = e.cursor;
        }
        if (e.type == EventType::Relax) CHECK(e.bucket == static_cast<int>(e.newDist % (s.C + 1)));
    }
};

static void testBucketQueue() {
    BucketQueue q(5, 3);  // 4 buckets
    CHECK(q.empty());
    q.insert(0, 2);
    q.insert(1, 6);  // 6 mod 4 = 2
    q.insert(2, 1);
    CHECK(q.size() == 3);
    CHECK(q.bucketOf(1) == 2);
    q.remove(0);
    CHECK(q.popFront(2) == 1);
    CHECK(q.popFront(1) == 2);
    CHECK(q.empty());
}

static void testSingleNode() {
    Graph g(1);
    DialResult r = dial(g, 0);
    CHECK(r.dist[0] == 0);
    CHECK(r.C == 0);
}

static void testUnreachableAndZeroWeights() {
    Graph g(4);
    g.addEdge(0, 1, 0);
    g.addEdge(1, 2, 2);
    g.addEdge(3, 0, 1);  // 3 no es alcanzable desde 0
    DialResult r = dial(g, 0);
    CHECK(r.dist[1] == 0);
    CHECK(r.dist[2] == 2);
    CHECK(r.dist[3] == INF);
    CHECK(buildPath(r, 3).empty());
    CHECK((buildPath(r, 2) == std::vector<int>{0, 1, 2}));
}

static void testRandom() {
    std::mt19937 rng(2023);
    for (int t = 0; t < 500; ++t) {
        int n = 1 + rng() % 40;
        int C = rng() % 12;
        int m = rng() % (n * 4 + 1);
        Graph g(n);
        for (int i = 0; i < m; ++i) g.addEdge(rng() % n, rng() % n, C ? rng() % (C + 1) : 0);
        int s = rng() % n;
        InvariantChecker chk;
        DialResult r = dial(g, s, &chk);
        CHECK(r.dist == bellmanFord(g, s));
    }
}

int main() {
    testBucketQueue();
    testSingleNode();
    testUnreachableAndZeroWeights();
    testRandom();
    if (failures) {
        std::cerr << failures << " pruebas fallaron\n";
        return EXIT_FAILURE;
    }
    std::cout << "Todas las pruebas pasaron\n";
    return EXIT_SUCCESS;
}
