#include "passes.h"

#include <torch/csrc/jit/passes/canonicalize.h>
#include <torch/csrc/jit/passes/clear_profiling.h>
#include <torch/csrc/jit/passes/common_subexpression_elimination.h>
#include <torch/csrc/jit/passes/constant_pooling.h>
#include <torch/csrc/jit/passes/constant_propagation.h>
#include <torch/csrc/jit/passes/dead_code_elimination.h>
#include <torch/csrc/jit/passes/erase_number_types.h>
#include <torch/csrc/jit/passes/fuse_linear.h>
#include <torch/csrc/jit/passes/fuse_relu.h>
#include <torch/csrc/jit/passes/inplace_check.h>
#include <torch/csrc/jit/passes/insert_guards.h>
#include <torch/csrc/jit/passes/integer_value_refinement.h>
#include <torch/csrc/jit/passes/lower_tuples.h>
#include <torch/csrc/jit/passes/peephole.h>
#include <torch/csrc/jit/passes/remove_exceptions.h>
#include <torch/csrc/jit/passes/remove_expands.h>
#include <torch/csrc/jit/passes/remove_inplace_ops.h>
#include <torch/csrc/jit/passes/remove_mutation.h>
#include <torch/extension.h>

#include "../exceptions.h"
#include "../graph/method_graphs.h"
#include "../macros.h"
#include "fuse_list_ops.h"
#include "inliner.h"
#include "loop_unrolling.h"
#include "lower_block_lists.h"
#include "lower_block_tuples.h"

namespace inference::passes {

bool RemoveOps(std::shared_ptr<Graph> &graph) {
    // Commented out since this seems to be breaking for certain graphs.
    // RemoveInplaceOps(graph);
    RemoveExpands(graph);
    EliminateExceptions(graph);
    return true;
}

bool apply_cleanup_passes(std::shared_ptr<Graph> &graph) {
    bool modified = RemoveListMutation(graph);
    modified |= RemoveTensorMutation(graph);
    modified |= PeepholeOptimize(graph);
    modified |= RefineIntegerValues(graph);
    modified |= ConstantPropagation(graph);
    Canonicalize(graph);
    CanonicalizeOutputs(graph);
    LowerSimpleTuples(graph);
    ConstantPooling(graph);
    modified |= EliminateCommonSubexpression(graph);
    EliminateDeadCode(graph);
    return modified;
}

bool apply_pass_to_graph(std::shared_ptr<Graph> &graph, bool (*func)(std::shared_ptr<Graph> &), std::string pass_name) {
    try {
        bool modified = func(graph);
        if (modified) apply_cleanup_passes(graph);
        return modified;
    } catch (std::exception &e) {
        MERROR("Exception while applying pass", pass_name, "-", e.what());
    }
}

void apply_passes_to_graph(std::shared_ptr<Graph> &graph) {
    // Applies initial passes to the graph.
    bool modified = false;
    modified |= apply_pass_to_graph(graph, inliner::Inliner, "Inliner");
    modified |= apply_pass_to_graph(graph, RemoveOps, "RemoveOps");

    // If initial passes didn't change anything, apply cleanup passes anyway.
    if (!modified) {
        apply_cleanup_passes(graph);
        modified = true;
    }

    // Applies additional steps until no more modifications are made.
    while (modified) {
        modified = false;
        modified |= apply_pass_to_graph(graph, loop_unrolling::UnrollLoops, "UnrollLoops");
        modified |= apply_pass_to_graph(graph, lower_block_tuples::LowerBlockTuples, "LowerBlockTuples");
        modified |= apply_pass_to_graph(graph, lower_block_lists::LowerBlockLists, "LowerBlockLists");
        modified |= apply_pass_to_graph(graph, fuse_list_ops::FuseListOps, "FuseListOps");
    }

    // Applies final passes to the graph.
    FuseLinear(graph);
    FuseAddRelu(graph);
    FuseAddMM(graph);
}

Module apply_all_passes(Module &mod, const config::Config &config, bool copy) {
    if (copy) mod = mod.clone();
    auto method_graphs = graph::method_graphs::get_method_graphs(mod, config);
    std::vector<exceptions::NodeException> errs;
    for (auto &[method_name, graph] : method_graphs) {
        try {
            apply_passes_to_graph(graph);
        } catch (exceptions::NodeException &e) {
            errs.push_back(e);
        }
    }
    EMPTY_CHECK(errs, "Caught exception(s) while applying passes");
    return mod;
}

void add_module(pybind11::module &m) { m.def("apply_all_passes", &apply_all_passes, "mod"_a, "config"_a, "copy"_a); }

}  // namespace inference::passes
