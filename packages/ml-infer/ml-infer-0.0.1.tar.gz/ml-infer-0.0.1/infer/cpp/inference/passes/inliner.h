#pragma once

#include <torch/extension.h>

using namespace torch::jit;

namespace inference::passes::inliner {

bool is_call_to_observed_module(Node* n);
GraphFunction* try_to_graph_function(Node* n);

/**
 * @brief Inlines function and method calls
 *
 * @param graph The graph to inline
 * @return If the graph was modified
 */
bool Inliner(Graph& graph);
bool Inliner(std::shared_ptr<Graph>& graph);

}  // namespace inference::passes::inliner
