#pragma once

#include <pybind11/pybind11.h>
#include <torch/extension.h>

#include "../config.h"

using namespace pybind11::literals;
using namespace torch::jit;

namespace inference::graph::implicit_tensors {

/**
 * @brief Returns a set of all implicit tensors in the module
 *
 * @param mod The module to consider
 * @param config Additional configuration options
 * @return The set of implicit tensors
 */
std::unordered_map<std::string, std::unordered_set<Value *>> get_implicit_tensors(Module &mod,
                                                                                  const config::Config &config);

void add_module(pybind11::module &m);

}  // namespace inference::graph::implicit_tensors
