#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::passes::loop_unrolling {

/**
 * @brief Unrolls some of the graph loops
 *
 * @param graph The graph to unroll loops
 * @return If the graph was modified
 */
bool UnrollLoops(std::shared_ptr<Graph>& graph);

}  // namespace inference::passes::loop_unrolling
