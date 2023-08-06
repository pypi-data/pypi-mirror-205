#include "disjoint_set.h"

#include <pybind11/stl.h>

using namespace pybind11::literals;

namespace inference::quantization::disjoint_set {

template <typename T>
void add_module_for(pybind11::module& m, const char* type_name) {
    pybind11::class_<DisjointSet<T>>(m, type_name)
        .def(pybind11::init<>())
        .def("__len__", &DisjointSet<T>::size)
        .def("__iadd__", &DisjointSet<T>::add)
        .def("__contains__", &DisjointSet<T>::has)
        .def("join", &DisjointSet<T>::join, "a"_a, "b"_a, "Joins the sets for two items")
        .def("maybe_join", &DisjointSet<T>::maybe_join, "a"_a, "b"_a, "Joins if both elements have sets")
        .def("num_sets", &DisjointSet<T>::num_sets, "Returns the number of disjoint sets")
        .def("sets", &DisjointSet<T>::sets, "Returns a set of sets, where each element is used once")
        .def("set_ids", &DisjointSet<T>::set_ids, "Returns a mapping from the element to it's set ID");
}

void add_module(pybind11::module& m) {
    add_module_for<std::string>(m, "DisjointStringSet");
    add_module_for<int>(m, "DisjointIntSet");
}

}  // namespace inference::quantization::disjoint_set
