#include "dial.h"

#include <algorithm>
#include <stdexcept>

DialResult dial(const Graph& g, int source, DialObserver* observer) {
    const int n = g.size();
    if (source < 0 || source >= n) throw std::invalid_argument("origen fuera de rango");

    const int C = g.maxWeight();
    BucketQueue bq(n, C);
    const int B = bq.numBuckets();

    std::vector<long long> dist(n, INF);
    std::vector<int> parent(n, -1);
    std::vector<bool> done(n, false);
    DialState state{g, source, C, dist, parent, done, bq};

    DialResult res;
    res.C = C;
    auto emit = [&](const DialEvent& e) {
        if (observer) observer->onEvent(e, state);
    };

    dist[source] = 0;
    bq.insert(source, 0);
    {
        DialEvent e{EventType::Init};
        e.u = source;
        e.bucket = 0;
        e.newDist = 0;
        emit(e);
    }

    long long cur = 0;  // distancia que estamos procesando
    while (!bq.empty()) {
        const int b = static_cast<int>(cur % B);

        if (bq.bucketEmpty(b)) {
            DialEvent e{EventType::ScanEmpty};
            e.cursor = cur;
            e.bucket = b;
            emit(e);
            ++cur;
            ++res.bucketScans;
            continue;
        }

        const int u = bq.popFront(b);
        done[u] = true;  // dist[u] == cur es definitiva
        {
            DialEvent e{EventType::Extract};
            e.u = u;
            e.cursor = cur;
            e.bucket = b;
            e.newDist = dist[u];
            emit(e);
        }

        for (int id : g.out(u)) {
            const Edge& ed = g.edge(id);
            const int v = ed.to;
            const long long nd = dist[u] + ed.w;

            DialEvent consider{EventType::ConsiderEdge};
            consider.u = u;
            consider.v = v;
            consider.edge = id;
            consider.cursor = cur;
            consider.oldDist = dist[v];
            consider.newDist = nd;
            emit(consider);

            if (!done[v] && nd < dist[v]) {
                DialEvent e = consider;
                e.type = EventType::Relax;
                e.fromBucket = bq.contains(v) ? bq.bucketOf(v) : -1;
                if (bq.contains(v)) bq.remove(v);  // "decrease-key" en O(1)
                dist[v] = nd;
                parent[v] = u;
                bq.insert(v, nd);
                e.bucket = bq.bucketOf(v);
                ++res.relaxations;
                emit(e);
            } else {
                DialEvent e = consider;
                e.type = EventType::NoRelax;
                emit(e);
            }
        }
    }

    {
        DialEvent e{EventType::Done};
        e.cursor = cur;
        emit(e);
    }

    res.dist = dist;
    res.parent = parent;
    return res;
}

std::vector<int> buildPath(const DialResult& r, int v) {
    std::vector<int> path;
    if (r.dist[v] == INF) return path;
    for (int x = v; x != -1; x = r.parent[x]) path.push_back(x);
    std::reverse(path.begin(), path.end());
    return path;
}
