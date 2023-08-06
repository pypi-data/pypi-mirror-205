#include "fuse_list_ops.h"

#include <torch/csrc/jit/runtime/custom_operator.h>

#include "../exceptions.h"

namespace inference::passes::fuse_list_ops {

torch::jit::RegisterOperators reg_fuse_ops({
    Operator(
        "inference::cat(...) -> Tensor",
        [](const Node* node) -> Operation {
            int64_t dim = node->i(attr::dim);
            size_t num_inputs = node->inputs().size();
            return [dim, num_inputs](Stack& stack) {
                auto result = at::cat(fmap(last(stack, num_inputs), [](const IValue& i) { return i.toTensor(); }), dim);
                drop(stack, num_inputs);
                pack(stack, std::move(result));
            };
        },
        c10::AliasAnalysisKind::FROM_SCHEMA),
    Operator(
        "inference::chunk(...) -> Tensor",
        [](const Node* node) -> Operation {
            int64_t dim = node->i(attr::dim);
            size_t num_outputs = node->outputs().size();
            return [dim, num_outputs](Stack& stack) {
                auto result = at::tensor_split(last(stack, 1).at(0).toTensor(), num_outputs, dim);
                MCHECK(result.size() == num_outputs, "Expected", num_outputs, "outputs, got", result.size());
                drop(stack, 1);
                for (auto& elem : fmap(result, [](const torch::Tensor& t) { return IValue(std::move(t)); }))
                    push(stack, elem);
            };
        },
        c10::AliasAnalysisKind::FROM_SCHEMA),
});

bool fuse_chunk(Node* node) {
    // Fortunately these functions have the same signature.
    NODE_CHECK(node->kind() == aten::chunk || node->kind() == aten::tensor_split, node,
               "Internal error; `fuse_chunk` called with non-chunk node");

    // Gets the tensor to chunk and the number of chunks.
    Value *in_tensor = node->input(0), *chunk_val = node->input(1), *dim_val = node->input(2);

    // Gets the number of output chunks.
    c10::optional<int64_t> const_num_chunks_opt = constant_as<int64_t>(chunk_val);
    if (!const_num_chunks_opt.has_value() || const_num_chunks_opt.value() <= 0) return false;
    size_t const_num_chunks = (size_t)const_num_chunks_opt.value();

    // Gets the chunk dimension.
    c10::optional<int64_t> const_dim_opt = constant_as<int64_t>(dim_val);
    if (!const_dim_opt.has_value()) return false;

    // Creates fused chunk operation.
    Node* chunk_node = node->owningGraph()
                           ->create(c10::Symbol::fromQualString("inference::chunk"), {in_tensor}, const_num_chunks)
                           ->insertBefore(node)
                           ->i_(attr::dim, const_dim_opt.value());

    // Creates a new list from the chunk outputs.
    std::vector<Value*> chunk_outputs;
    for (Value* output : chunk_node->outputs()) {
        output->setType(in_tensor->type());
        chunk_outputs.push_back(output);
    }
    Node* list_node = node->owningGraph()->createList(in_tensor->type(), chunk_outputs)->insertAfter(chunk_node);

    // Replaces the original output usages with the new output usages.
    node->output()->replaceAllUsesWith(list_node->output());

    return true;
}

bool fuse_cat(Node* node) {
    NODE_CHECK(node->kind() == aten::cat, node, "Internal error; `fuse_cat` called with non-cat node");

    // Gets the tensor to concat.
    Value *in_list = node->input(0), *dim_val = node->input(1);

    // Gets the cta dimension.
    c10::optional<int64_t> const_dim_opt = constant_as<int64_t>(dim_val);
    if (!const_dim_opt.has_value()) return false;

    // Gets the input tensors.
    if (in_list->node()->kind() != prim::ListConstruct) return false;

    // Unpacks the list to it's component parts.
    Node* list_unpack_node =
        node->owningGraph()->createListUnpack(in_list, in_list->node()->inputs().size())->insertBefore(node);

    // Creates a fused concat operation.
    Node* cat_node = node->owningGraph()
                         ->create(c10::Symbol::fromQualString("inference::cat"), list_unpack_node->outputs(), 1)
                         ->insertAfter(list_unpack_node)
                         ->i_(attr::dim, const_dim_opt.value());

    // Replaces the original output usages with the new output usages.
    node->output()->replaceAllUsesWith(cat_node->output());

    return true;
}

bool fuse_list_ops(Block* block) {
    bool modified = false;

    for (Node* node : block->nodes()) {
        for (Block* subblock : node->blocks()) modified |= fuse_list_ops(subblock);

        switch (node->kind()) {
            case aten::chunk:
            case aten::tensor_split:
                modified |= fuse_chunk(node);
                break;
            case aten::cat:
                modified |= fuse_cat(node);
                break;
        }
    }

    return modified;
}

bool FuseListOps(std::shared_ptr<Graph>& graph) { return fuse_list_ops(graph->block()); }

}  // namespace inference::passes::fuse_list_ops
