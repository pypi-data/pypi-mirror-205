#include "lower_block_tuples.h"

#include "../exceptions.h"
#include "../macros.h"
#include "pass_utils.h"

namespace inference::passes::lower_block_tuples {

size_t add_tuple_construct_around_loop(Node* node, size_t idx, bool& modified) {
    NODE_CHECK(node->kind() == c10::prim::Loop, node, "Internal error; expected prim::Loop");

    Block* block = node->blocks().at(0);
    TupleTypePtr tt = node->input(idx)->type()->cast<TupleType>();

    // Ignore non-tuples.
    if (tt == nullptr) return 1;

    Graph* graph = node->owningGraph();

    // Indices for the loop.
    size_t node_in_idx = idx, block_in_idx = idx - 1, block_out_idx = idx - 1, node_out_idx = idx - 2;

    // Unpacks the tuple for the loop input.
    Node* unpack_node_in = graph->createTupleUnpack(node->input(node_in_idx));
    unpack_node_in->copyMetadata(node);
    unpack_node_in->insertBefore(node);
    size_t num_tuple_vals = unpack_node_in->outputs().size();

    // Adds unpack node outputs to the loop closure.
    for (size_t i = 0; i < num_tuple_vals; i++) node->insertInput(node_in_idx + i + 1, unpack_node_in->output(i));
    node->removeInput(node_in_idx);

    // Creates new block inputs to correspond to the new loop closure values.
    std::vector<Value*> new_block_inputs;
    for (size_t i = 0; i < num_tuple_vals; i++) {
        Value* new_input = block->insertInput(block_in_idx + i + 1);
        new_input->setType(unpack_node_in->output(i)->type());
        new_input->copyMetadata(unpack_node_in->output(i));
        new_block_inputs.push_back(new_input);
    }
    Node* pack_node_in = graph->createTuple(new_block_inputs);
    pack_node_in->copyMetadata(block->param_node());
    pack_node_in->insertAfter(block->param_node());
    block->inputs().at(block_in_idx)->replaceAllUsesWith(pack_node_in->output());
    block->eraseInput(block_in_idx);

    // Unpacks the tuple for the loop output.
    Value* block_out_tuple = block->outputs().at(block_out_idx);
    Node* unpack_node_out = graph->createTupleUnpack(block_out_tuple);
    unpack_node_out->copyMetadata(block->return_node());
    unpack_node_out->insertBefore(block->return_node());
    NODE_CHECK(unpack_node_out->outputs().size() == num_tuple_vals, unpack_node_out,
               "Internal error; unpack node output tuple has wrong number of output values");

    // Adds unpack node outputs to the loop return.
    for (size_t i = 0; i < num_tuple_vals; i++) block->insertOutput(block_out_idx + i + 1, unpack_node_out->output(i));
    block->eraseOutput(block_out_idx);

    // Creates new block outputs to correspond to return values.
    std::vector<Value*> new_block_outputs;
    for (size_t i = 0; i < num_tuple_vals; i++) {
        Value* new_output = node->insertOutput(node_out_idx + i + 1);
        new_output->setType(unpack_node_out->output(i)->type());
        new_output->copyMetadata(unpack_node_out->output(i));
        new_block_outputs.push_back(new_output);
    }
    Node* pack_node_out = graph->createTuple(new_block_outputs);
    pack_node_out->copyMetadata(block->return_node());
    pack_node_out->insertAfter(node);
    node->output(node_out_idx)->replaceAllUsesWith(pack_node_out->output());
    node->eraseOutput(node_out_idx);

    modified = true;
    return num_tuple_vals;
}

size_t add_tuple_construct_around_if(Node* node, size_t idx, bool& modified) {
    NODE_CHECK(node->kind() == c10::prim::If, node, "Internal error; expected prim::If");

    Block *true_block = node->blocks().at(0), *false_block = node->blocks().at(1);
    TupleTypePtr tt = node->output(idx)->type()->cast<TupleType>();

    // Ignore non-tuples.
    if (tt == nullptr) return 1;

    Graph* graph = node->owningGraph();

    // Unpacks the tuple for the true block.
    Node* unpack_node_true = graph->createTupleUnpack(true_block->outputs().at(idx));
    unpack_node_true->copyMetadata(node);
    unpack_node_true->insertBefore(true_block->return_node());
    size_t num_tuple_vals = unpack_node_true->outputs().size();
    for (size_t i = 0; i < num_tuple_vals; i++) true_block->insertOutput(idx + i + 1, unpack_node_true->output(i));
    true_block->eraseOutput(idx);

    // Unpacks the tuple for the false block.
    Node* unpack_node_false = graph->createTupleUnpack(false_block->outputs().at(idx));
    unpack_node_false->copyMetadata(node);
    unpack_node_false->insertBefore(false_block->return_node());
    NODE_CHECK(unpack_node_false->outputs().size() == num_tuple_vals, unpack_node_false,
               "Internal error; number of outputs for unpack node for false block doesn't match true block");
    for (size_t i = 0; i < num_tuple_vals; i++) false_block->insertOutput(idx + i + 1, unpack_node_false->output(i));
    false_block->eraseOutput(idx);

    // Packs the node output.
    std::vector<Value*> new_outputs;
    for (size_t i = 0; i < num_tuple_vals; i++) {
        Value* new_output = node->insertOutput(idx + i + 1);
        new_output->setType(unpack_node_true->output(i)->type());
        new_output->copyMetadata(unpack_node_true->output(i));
        new_outputs.push_back(new_output);
    }
    Node* new_pack_node = graph->createTuple(new_outputs);
    new_pack_node->copyMetadata(node);
    new_pack_node->insertAfter(node);
    node->output(idx)->replaceAllUsesWith(new_pack_node->output());
    node->eraseOutput(idx);

    modified = true;
    return num_tuple_vals;
}

bool lower_block_tuples(Block* block) {
    bool modified = false;

    for (Node* node : block->nodes()) {
        switch (node->kind()) {
            case c10::prim::Loop: {
                for (size_t i = 2; i < node->inputs().size();) i += add_tuple_construct_around_loop(node, i, modified);
                break;
            }
            case c10::prim::If: {
                for (size_t i = 0; i < node->outputs().size();) i += add_tuple_construct_around_if(node, i, modified);
                break;
            }
        }

        // Flattens tuples within the child block.
        for (Block* subblock : node->blocks()) modified |= lower_block_tuples(subblock);
    }

    return modified;
}

bool LowerBlockTuples(std::shared_ptr<Graph>& graph) {
    bool modified = lower_block_tuples(graph->block());
    if (modified) pass_utils::run_all_checks(graph);
    return modified;
}

}  // namespace inference::passes::lower_block_tuples
