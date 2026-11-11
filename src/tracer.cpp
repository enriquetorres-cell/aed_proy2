#include "tracer.h"

#include <fstream>
#include <sstream>
#include <stdexcept>

namespace {

const char* typeName(EventType t) {
    switch (t) {
        case EventType::Init: return "init";
        case EventType::ScanEmpty: return "scan_empty";
        case EventType::Extract: return "extract";
        case EventType::ConsiderEdge: return "consider_edge";
        case EventType::Relax: return "relax";
        case EventType::NoRelax: return "no_relax";
        case EventType::Done: return "done";
    }
    return "?";
}

std::string num(long long x) { return x == INF ? "null" : std::to_string(x); }

std::string distArray(const std::vector<long long>& d) {
    std::string s = "[";
    for (size_t i = 0; i < d.size(); ++i) s += (i ? "," : "") + num(d[i]);
    return s + "]";
}

std::string intArray(const std::vector<int>& a) {
    std::string s = "[";
    for (size_t i = 0; i < a.size(); ++i) s += (i ? "," : "") + std::to_string(a[i]);
    return s + "]";
}

std::string boolArray(const std::vector<bool>& a) {
    std::string s = "[";
    for (size_t i = 0; i < a.size(); ++i) s += std::string(i ? "," : "") + (a[i] ? "true" : "false");
    return s + "]";
}

}  // namespace

void JsonTracer::onEvent(const DialEvent& e, const DialState& s) {
    std::ostringstream o;
    o << "{\"type\":\"" << typeName(e.type) << "\""
      << ",\"u\":" << e.u << ",\"v\":" << e.v << ",\"edge\":" << e.edge
      << ",\"cursor\":" << e.cursor << ",\"bucket\":" << e.bucket
      << ",\"from_bucket\":" << e.fromBucket
      << ",\"old\":" << num(e.oldDist) << ",\"new\":" << num(e.newDist)
      << ",\"dist\":" << distArray(s.dist)
      << ",\"parent\":" << intArray(s.parent)
      << ",\"done\":" << boolArray(s.done)
      << ",\"buckets\":[";
    auto snap = s.bq.snapshot();
    for (size_t b = 0; b < snap.size(); ++b) o << (b ? "," : "") << intArray(snap[b]);
    o << "]}";
    events_.push_back(o.str());
}

void JsonTracer::write(const std::string& path, const Graph& g, int source,
                       const DialResult& r) const {
    std::ofstream out(path);
    if (!out) throw std::runtime_error("no se pudo escribir " + path);

    out << "{\n  \"n\": " << g.size() << ",\n  \"source\": " << source
        << ",\n  \"C\": " << r.C << ",\n  \"B\": " << (r.C + 1) << ",\n  \"nodes\": [";
    for (int i = 0; i < g.size(); ++i) {
        out << (i ? "," : "") << "\n    {\"id\":" << i;
        if (!g.pos.empty()) out << ",\"x\":" << g.pos[i].x << ",\"y\":" << g.pos[i].y;
        out << "}";
    }
    out << "\n  ],\n  \"edges\": [";
    for (int i = 0; i < g.edgeCount(); ++i) {
        const Edge& e = g.edge(i);
        out << (i ? "," : "") << "\n    {\"id\":" << i << ",\"u\":" << e.from
            << ",\"v\":" << e.to << ",\"w\":" << e.w << "}";
    }
    out << "\n  ],\n  \"events\": [";
    for (size_t i = 0; i < events_.size(); ++i) out << (i ? "," : "") << "\n    " << events_[i];
    out << "\n  ],\n  \"result\": {\"dist\":" << distArray(r.dist)
        << ",\"parent\":" << intArray(r.parent) << ",\"bucket_scans\":" << r.bucketScans
        << ",\"relaxations\":" << r.relaxations << "}\n}\n";
}
