#include "lower_block_lists.h"

#include "../exceptions.h"
#include "../macros.h"
#include "../utils.h"
#include "pass_utils.h"

namespace inference::passes::lower_block_lists {

bool can_remove_list(Value* value) {
    // The list can be removed if it is treated like a tuple.
    for (Use use : value->uses()) {
        switch (use.user->kind()) {
            case c10::aten::_set_item:
            case c10::aten::__getitem__:
            case c10::aten::slice:
            case c10::prim::ListUnpack:
            case c10::aten::len:
                break;
            case c10::prim::Return:
                if (use.user->owningBlock() != value->node()->owningBlock()) return false;
                break;
            case c10::prim::Loop:
                if (!can_remove_list(use.user->blocks().at(0)->inputs().at(use.offset - 1))) return false;
                break;
            default:
                return false;
        }
    }
    return true;
}

size_t add_list_construct_around_loop(Node* node, size_t idx, bool& modified) {
    NODE_CHECK(node->kind() == c10::prim::Loop, node, "Internal error; expected prim::Loop");

    Block* block = node->blocks().at(0);
    Node* list_construct_node = node->input(idx)->node();

    // Ignore non-lists and lists which can't be removed..
    if (list_construct_node->kind() != c10::prim::ListConstruct) return 1;
    if (!can_remove_list(list_construct_node->output())) return 1;

    Graph* graph = node->owningGraph();
    size_t num_list_vals = list_construct_node->inputs().size();
    ListTypePtr lt = list_construct_node->output()->type()->cast<ListType>();
    NODE_CHECK(lt, node, "ListConstruct output is not a list type");

    // Indices for the loop.
    size_t node_in_idx = idx, block_in_idx = idx - 1, block_out_idx = idx - 1, node_out_idx = idx - 2;

    // Unpacks the list for the loop input.
    Node* unpack_node_in = graph->createListUnpack(node->input(node_in_idx), num_list_vals);
    unpack_node_in->copyMetadata(node);
    unpack_node_in->insertBefore(node);

    // Adds unpack node outputs to the loop closure.
    for (size_t i = 0; i < num_list_vals; i++) node->insertInput(node_in_idx + i + 1, unpack_node_in->output(i));
    node->removeInput(node_in_idx);

    // Creates new block inputs to correspond to the new loop closure values.
    std::vector<Value*> new_block_inputs;
    for (size_t i = 0; i < num_list_vals; i++) {
        Value* new_input = block->insertInput(block_in_idx + i + 1);
        new_input->setType(unpack_node_in->output(i)->type());
        new_input->copyMetadata(unpack_node_in->output(i));
        new_block_inputs.push_back(new_input);
    }
    Node* pack_node_in = graph->createList(lt->containedType(0), new_block_inputs);
    pack_node_in->copyMetadata(block->param_node());
    pack_node_in->insertAfter(block->param_node());
    block->inputs().at(block_in_idx)->replaceAllUsesWith(pack_node_in->output());
    block->eraseInput(block_in_idx);

    // Unpacks the list for the loop output.
    Value* block_out_list = block->outputs().at(block_out_idx);
    Node* unpack_node_out = graph->createListUnpack(block_out_list, num_list_vals);
    unpack_node_out->copyMetadata(block->return_node());
    unpack_node_out->insertBefore(block->return_node());
    NODE_CHECK(unpack_node_out->outputs().size() == num_list_vals, unpack_node_out,
               "Internal error; unpack node output list has wrong number of output values");

    // Adds unpack node outputs to the loop return.
    for (size_t i = 0; i < num_list_vals; i++) block->insertOutput(block_out_idx + i + 1, unpack_node_out->output(i));
    block->eraseOutput(block_out_idx);

    // Creates new block outputs to correspond to return values.
    std::vector<Value*> new_block_outputs;
    for (size_t i = 0; i < num_list_vals; i++) {
        Value* new_output = node->insertOutput(node_out_idx + i + 1);
        new_output->setType(unpack_node_out->output(i)->type());
        new_output->copyMetadata(unpack_node_out->output(i));
        new_block_outputs.push_back(new_output);
    }
    Node* pack_node_out = graph->createList(lt->containedType(0), new_block_outputs);
    pack_node_out->copyMetadata(block->return_node());
    pack_node_out->insertAfter(node);
    node->output(node_out_idx)->replaceAllUsesWith(pack_node_out->output());
    node->eraseOutput(node_out_idx);

    modified = true;
    return num_list_vals;
}

size_t add_list_construct_around_if(Node* node, size_t idx, bool& modified) {
    NODE_CHECK(node->kind() == c10::prim::If, node, "Internal error; expected prim::If");

    Block *true_block = node->blocks().at(0), *false_block = node->blocks().at(1);
    Node* list_construct_node = node->output(idx)->node();

    // Ignore non-lists and lists which can't be removed..
    if (list_construct_node->kind() != c10::prim::ListConstruct) return 1;
    if (!can_remove_list(list_construct_node->output())) return 1;

    Graph* graph = node->owningGraph();
    size_t num_list_vals = list_construct_node->inputs().size();
    ListTypePtr lt = list_construct_node->output()->type()->cast<ListType>();
    NODE_CHECK(lt, node, "ListConstruct output is not a list type");

    // Unpacks the list for the true block.
    Node* unpack_node_true = graph->createListUnpack(true_block->outputs().at(idx), num_list_vals);
    unpack_node_true->copyMetadata(node);
    unpack_node_true->insertBefore(true_block->return_node());
    for (size_t i = 0; i < num_list_vals; i++) true_block->insertOutput(idx + i + 1, unpack_node_true->output(i));
    true_block->eraseOutput(idx);

    // Unpacks the list for the false block.
    Node* unpack_node_false = graph->createListUnpack(false_block->outputs().at(idx), num_list_vals);
    unpack_node_false->copyMetadata(node);
    unpack_node_false->insertBefore(false_block->return_node());
    NODE_CHECK(unpack_node_false->outputs().size() == num_list_vals, unpack_node_false,
               "Internal error; number of outputs for unpack node for false block doesn't match true block");
    for (size_t i = 0; i < num_list_vals; i++) false_block->insertOutput(idx + i + 1, unpack_node_false->output(i));
    false_block->eraseOutput(idx);

    // Packs the node output.
    std::vector<Value*> new_outputs;
    for (size_t i = 0; i < num_list_vals; i++) {
        Value* new_output = node->insertOutput(idx + i + 1);
        new_output->setType(unpack_node_true->output(i)->type());
        new_output->copyMetadata(unpack_node_true->output(i));
        new_outputs.push_back(new_output);
    }
    Node* new_pack_node = graph->createList(lt->containedType(0), new_outputs);
    new_pack_node->copyMetadata(node);
    new_pack_node->insertAfter(node);
    node->output(idx)->replaceAllUsesWith(new_pack_node->output());
    node->eraseOutput(idx);

    modified = true;
    return num_list_vals;
}

bool lower_block_lists(Block* block) {
    bool modified = false;

    for (Node* node : block->nodes()) {
        switch (node->kind()) {
            case c10::prim::Loop: {
                for (size_t i = 2; i < node->inputs().size();) i += add_list_construct_around_loop(node, i, modified);
                break;
            }
            case c10::prim::If: {
                for (size_t i = 0; i < node->outputs().size();) i += add_list_construct_around_if(node, i, modified);
                break;
            }
        }

        // Flattens lists within the child block.
        for (Block* subblock : node->blocks()) modified |= lower_block_lists(subblock);
    }

    return modified;
}

bool LowerBlockLists(std::shared_ptr<Graph>& graph) {
    bool modified = lower_block_lists(graph->block());
    if (modified) pass_utils::run_all_checks(graph);
    return modified;
}

}  // namespace inference::passes::lower_block_lists
