#pragma once

#include <pybind11/pybind11.h>
#include <torch/extension.h>

#include "../config.h"

using namespace pybind11::literals;
using namespace torch::jit;

namespace inference::quantization {

Module insert_observers(Module &mod, const config::Config &config, bool copy);

void add_module(pybind11::module &m);

void add_torch_module(torch::Library &m);

}  // namespace inference::quantization
