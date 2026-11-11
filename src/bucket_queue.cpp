#include "bucket_queue.h"

#include <stdexcept>

BucketQueue::BucketQueue(int numNodes, int maxWeight)
    : B_(maxWeight + 1),
      head_(B_, -1),
      tail_(B_, -1),
      next_(numNodes, -1),
      prev_(numNodes, -1),
      bucketOf_(numNodes, -1) {}

void BucketQueue::insert(int v, long long dist) {
    if (contains(v)) throw std::logic_error("el nodo ya esta en la cola");
    int b = static_cast<int>(dist % B_);
    bucketOf_[v] = b;
    next_[v] = -1;
    prev_[v] = tail_[b];
    if (tail_[b] != -1) next_[tail_[b]] = v;
    else head_[b] = v;
    tail_[b] = v;
    ++size_;
}

void BucketQueue::remove(int v) {
    int b = bucketOf_[v];
    if (b == -1) throw std::logic_error("el nodo no esta en la cola");
    if (prev_[v] != -1) next_[prev_[v]] = next_[v];
    else head_[b] = next_[v];
    if (next_[v] != -1) prev_[next_[v]] = prev_[v];
    else tail_[b] = prev_[v];
    next_[v] = prev_[v] = bucketOf_[v] = -1;
    --size_;
}

int BucketQueue::popFront(int b) {
    int v = head_[b];
    if (v == -1) throw std::logic_error("bucket vacio");
    remove(v);
    return v;
}

std::vector<std::vector<int>> BucketQueue::snapshot() const {
    std::vector<std::vector<int>> out(B_);
    for (int b = 0; b < B_; ++b)
        for (int v = head_[b]; v != -1; v = next_[v]) out[b].push_back(v);
    return out;
}
