#pragma once
// Cola de buckets circular (implementacion propia, sin std::priority_queue).
//
// Hay B = C + 1 buckets. Un nodo con distancia tentativa d vive en el bucket
// d mod B. Como en todo momento las distancias pendientes estan en el rango
// [d_actual, d_actual + C], nunca hay dos distancias distintas en el mismo bucket.
//
// Cada bucket es una lista doblemente enlazada implementada con arreglos
// (head/tail/next/prev), lo que permite en O(1):
//   - insertar un nodo al final de un bucket
//   - eliminar un nodo arbitrario (necesario al "disminuir" su distancia)
//   - extraer el primer nodo de un bucket

#include <vector>

class BucketQueue {
public:
    BucketQueue(int numNodes, int maxWeight);

    int numBuckets() const { return B_; }
    int size() const { return size_; }
    bool empty() const { return size_ == 0; }

    bool contains(int v) const { return bucketOf_[v] != -1; }
    int bucketOf(int v) const { return bucketOf_[v]; }
    bool bucketEmpty(int b) const { return head_[b] == -1; }

    void insert(int v, long long dist);  // O(1)
    void remove(int v);                  // O(1)
    int popFront(int b);                 // O(1), b no debe estar vacio

    // Contenido de cada bucket en orden (solo para trazas / animacion).
    std::vector<std::vector<int>> snapshot() const;

private:
    int B_;
    int size_ = 0;
    std::vector<int> head_, tail_;    // por bucket
    std::vector<int> next_, prev_;    // por nodo
    std::vector<int> bucketOf_;       // por nodo, -1 si no esta en la cola
};
