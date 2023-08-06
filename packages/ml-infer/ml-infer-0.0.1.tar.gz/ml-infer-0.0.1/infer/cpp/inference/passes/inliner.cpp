#include "inliner.h"

#include "../exceptions.h"
#include "../macros.h"

namespace inference::passes::inliner {

/**
 * Used to check if the method call is being made to a module which already
 * has an observer. This means that submodules which have a separate observer
 * from the current module will keep their own observers, and their functions
 * will not be in-lined. This is done to support composition of separately
 * calibrated modules.
 */
bool is_call_to_observed_module(Node* n) {
    NODE_CHECK(n->kind() == prim::CallMethod, n, "Unexpected argument to `is_call_to_observed_module`");
    const std::string& name = n->s(attr::name);
    if (auto class_type = n->input(0)->type()->cast<ClassType>()) {
        return class_type->hasAttribute(OBSERVER_NAME);
    }
    return false;
}

GraphFunction* try_to_graph_function(Node* n) {
    if (n->kind() == prim::CallFunction) {
        NODE_CHECK(n->input(0)->node()->kind() == prim::Constant, n, "Unexpected function name type");
        auto function_constant = n->input(0)->node();
        auto fun_type = function_constant->output()->type()->expect<FunctionType>();
        return tryToGraphFunction(*fun_type->function());
    }
    if (n->kind() == prim::CallMethod) {
        const std::string& name = n->s(attr::name);
        if (auto class_type = n->input(0)->type()->cast<ClassType>()) {
            Function& function = class_type->getMethod(name);
            return tryToGraphFunction(function);
        }
    }
    return nullptr;
}

bool inline_calls(Block* block) {
    bool modified = false;

    for (auto it = block->nodes().begin(), end = block->nodes().end(); it != end;) {
        Node* cur = *it++;
        switch (cur->kind()) {
            case prim::CallFunction: {
                if (auto graphFunction = try_to_graph_function(cur)) {
                    auto function_constant = cur->input(0)->node();
                    auto fun_type = function_constant->output()->type()->expect<FunctionType>();

                    cur->removeInput(0);

                    std::shared_ptr<Graph> g = nullptr;
                    bool fallback = function_constant->hasAttribute(Symbol::attr("fallback"));
                    if (fallback && graphFunction->get_executor().isOptimized()) {
                        auto exec_plans = graphFunction->get_executor().getDebugState().execution_plans;
                        if (exec_plans.size() != 0) {
                            g = exec_plans.begin()->second.graph;
                            modified |= Inliner(*g.get());
                        }
                    }
                    if (g == nullptr) {
                        g = graphFunction->optimized_graph();
                    }

                    inlineCallTo(cur, graphFunction, g.get());
                    modified = true;
                }
            } break;
            case prim::CallMethod: {
                if (!is_call_to_observed_module(cur)) {
                    if (auto graphFunction = try_to_graph_function(cur)) {
                        inlineCallTo(cur, graphFunction);
                        modified = true;
                    }
                }
            } break;
            default: {
                for (auto b : cur->blocks()) {
                    modified |= inline_calls(b);
                }
            } break;
        }
    }
    return modified;
}

bool Inliner(Graph& graph) { return inline_calls(graph.block()); }

bool Inliner(std::shared_ptr<Graph>& graph) { return inline_calls(graph->block()); }

}  // namespace inference::passes::inliner
