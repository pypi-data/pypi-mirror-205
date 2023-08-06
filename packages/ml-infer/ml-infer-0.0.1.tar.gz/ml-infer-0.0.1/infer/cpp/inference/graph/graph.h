#pragma once

#include <pybind11/pybind11.h>

#include "implicit_tensors.h"

namespace inference::graph {

void add_module(pybind11::module &m);
}
