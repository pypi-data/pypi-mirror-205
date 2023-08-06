#include "graph.h"

namespace inference::graph {

void add_module(pybind11::module &m) { inference::graph::implicit_tensors::add_module(m); }

}  // namespace inference::graph
