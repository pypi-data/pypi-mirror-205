#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::passes::fuse_list_ops {

/**
 * @brief Fuses lists into "fused" versions of some ops
 *
 * @param graph The graph to fuse ops for
 * @return If the graph was modified
 */
bool FuseListOps(std::shared_ptr<Graph>& graph);

}  // namespace inference::passes::fuse_list_ops
