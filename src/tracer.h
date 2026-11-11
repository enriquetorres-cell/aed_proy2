#pragma once
// Observador que registra cada paso del algoritmo de Dial y lo exporta a JSON.
// Ese JSON es lo que consume la animacion en Python (Manim): asi la animacion
// esta impulsada por la ejecucion real de nuestra implementacion en C++.

#include <string>
#include <vector>

#include "dial.h"

class JsonTracer : public DialObserver {
public:
    void onEvent(const DialEvent& e, const DialState& s) override;

    // Escribe grafo + eventos + resultado final en un archivo JSON.
    void write(const std::string& path, const Graph& g, int source, const DialResult& r) const;

private:
    std::vector<std::string> events_;
};
