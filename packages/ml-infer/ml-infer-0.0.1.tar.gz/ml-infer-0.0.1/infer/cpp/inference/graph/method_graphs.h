#pragma once

#include <torch/extension.h>

#include "../config.h"
#include "../exceptions.h"

namespace inference::graph::method_graphs {

/**
 * @brief Gets the method graphs from the module
 *
 * @param mod The module to get graphs for
 * @param config The associated config, for filtering methods
 * @return Mapping from the method name to it's associated graph
 */
std::unordered_map<std::string, std::shared_ptr<torch::jit::Graph>> get_method_graphs(const torch::jit::Module &mod,
                                                                                      const config::Config &config);

}  // namespace inference::graph::method_graphs
