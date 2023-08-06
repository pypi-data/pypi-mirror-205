#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::passes::lower_block_tuples {

/**
 * @brief Lowers tuples which can be lowered
 *
 * @param graph The graph to lower tuples for
 * @return If the graph was modified
 */
bool LowerBlockTuples(std::shared_ptr<Graph>& graph);

}  // namespace inference::passes::lower_block_tuples
