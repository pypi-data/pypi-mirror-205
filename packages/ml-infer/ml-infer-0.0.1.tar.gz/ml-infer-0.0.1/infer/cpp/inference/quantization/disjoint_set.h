#pragma once

#include <pybind11/pybind11.h>

#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../exceptions.h"

namespace inference::quantization::disjoint_set {

template <typename T>
class DisjointSet {
   private:
    std::vector<size_t> parent;

    // Mappings to and from the item to it's index in the `parent` array.
    std::unordered_map<T, size_t> indices;
    std::unordered_map<size_t, T> rev_indices;

   public:
    DisjointSet() {}

    size_t size() const { return parent.size(); }

    DisjointSet<T> add(T item) {
        size_t index = size();  // Last index
        parent.push_back(index);
        indices[item] = index;
        rev_indices[index] = item;
        return *this;
    }

    bool has(T item) { return indices.find(item) != indices.end(); }

    size_t find_index(size_t index) {
        size_t parent_index = index;
        while (parent[parent_index] != parent_index) parent_index = parent[parent_index];

        // Ensures that visited indices are one hop from the parent, for efficiency.
        size_t index_tmp = index;
        while (parent[index_tmp] != index_tmp) {
            parent[index_tmp] = parent_index;
            index_tmp = parent[index_tmp];
        }

        return parent_index;
    }

    size_t find_item(T item) {
        MCHECK(has(item), "Item not found in the disjoint set");
        return find_index(indices[item]);
    }

    void join(T a, T b) {
        size_t a_idx = find_item(a), b_idx = find_item(b);
        parent[a_idx] = b_idx;
    }

    void maybe_join(T a, T b) {
        if (has(a) && has(b)) join(a, b);
    }

    const size_t num_sets() {
        std::unordered_set<size_t> parents;
        for (size_t i = 0; i < size(); i++) parents.emplace(find_index(i));
        return parents.size();
    }

    std::vector<std::unordered_set<T>> sets() {
        std::unordered_map<size_t, std::unordered_set<size_t>> parent_to_set;

        // Creates mapping from the parent index to the set of children.
        for (size_t i = 0; i < size(); i++) {
            size_t p = find_index(i);
            if (parent_to_set.find(p) == parent_to_set.end()) {
                std::unordered_set<size_t> pset = {i};
                parent_to_set.emplace(p, pset);
            } else {
                parent_to_set[p].emplace(i);
            }
        }

        // Converts dictionary to a set of sets.
        std::vector<std::unordered_set<T>> output_set;
        output_set.reserve(parent_to_set.size());
        for (auto& [key, value] : parent_to_set) {
            std::unordered_set<T> output_set_item;
            for (size_t i : value) output_set_item.emplace(rev_indices.at(i));
            output_set.push_back(output_set_item);
        }

        return output_set;
    }

    std::unordered_map<T, size_t> set_ids() {
        const std::vector<std::unordered_set<T>> set_vec = sets();
        std::unordered_map<T, size_t> set_map;
        for (size_t i = 0; i < set_vec.size(); i++)
            for (auto& elem : set_vec[i]) set_map.emplace(elem, i);
        return set_map;
    }
};

void add_module(pybind11::module& m);

}  // namespace inference::quantization::disjoint_set
