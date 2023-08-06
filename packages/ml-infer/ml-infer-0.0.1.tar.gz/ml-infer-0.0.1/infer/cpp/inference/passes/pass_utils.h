#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::passes::pass_utils {

/**
 * @brief Runs all consistency checks.
 */
void run_all_checks(const Block* block, bool recurse = true);
void run_all_checks(const std::shared_ptr<Graph>& graph, bool recurse = true);

/**
 * @brief Gets the depth of the block relative to the owning block.
 */
size_t block_depth(Block* block);

/**
 * @brief Gets the lowest common block between two blocks.
 */
Block* common_block(Block* lhs, Block* rhs);

/**
 * @brief Gets intermediate blocks (including child, excluding parent).
 */
std::deque<Block*> blocks_between(Block* child, Block* parent);

}  // namespace inference::passes::pass_utils
