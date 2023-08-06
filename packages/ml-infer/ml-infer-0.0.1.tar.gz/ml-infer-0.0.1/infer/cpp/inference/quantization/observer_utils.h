#pragma once

#include <torch/extension.h>

#include "disjoint_set.h"

using namespace torch::jit;

namespace inference::quantization::observer_utils {

/**
 * @brief Adds tensors which are the exact same as the current tensor to the same group.
 *
 * @returns If the tensor was handled
 */
bool make_common_groups(disjoint_set::DisjointSet<const Value*>& groups, const Value* tensor);

}  // namespace inference::quantization::observer_utils
