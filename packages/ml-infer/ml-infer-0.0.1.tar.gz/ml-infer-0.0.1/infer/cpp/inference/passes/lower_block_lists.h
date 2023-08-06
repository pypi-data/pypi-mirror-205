#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::passes::lower_block_lists {

/**
 * @brief Removes removable list mutations from the graph.
 *
 * @param graph The graph to remove mutations for
 * @return If the graph was modified
 */
bool LowerBlockLists(std::shared_ptr<Graph>& graph);

}  // namespace inference::passes::lower_block_lists
