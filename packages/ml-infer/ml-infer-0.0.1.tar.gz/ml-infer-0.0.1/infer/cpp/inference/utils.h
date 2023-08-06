#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::utils {

/**
 * @brief Renders the node or value as a string
 *
 * @param node The node or value to render
 * @return The rendered node or value
 */
std::string to_string(const Node *node);
std::string to_string(const Value *value, bool with_node = false);

}  // namespace inference::utils
