#include "pass_utils.h"

#include "../exceptions.h"

namespace inference::passes::pass_utils {

void assert_well_formed_loop(const Node* loop_node) {
    NODE_CHECK(loop_node->kind() == c10::prim::Loop, loop_node, "Internal error; checking a non-loop statement");

    const Block* block = loop_node->blocks().at(0);

    // Checks that sizes match everywhere.
    NODE_CHECK(loop_node->inputs().size() == loop_node->outputs().size() + 2, loop_node, "Mismatched loop inputs size",
               loop_node->inputs().size(), "and outputs size", loop_node->outputs().size());
    NODE_CHECK(loop_node->inputs().size() == block->inputs().size() + 1, loop_node, "Mismatched loop input size",
               loop_node->inputs().size(), "and block inputs size", block->inputs().size());
    NODE_CHECK(block->inputs().size() == block->outputs().size(), loop_node, "Mismatched loop block inputs size",
               block->inputs().size(), "and block outputs size", block->outputs().size());

    // Checks that types match everywhere.
    for (size_t i = 0; i < loop_node->outputs().size(); i++) {
        NODE_CHECK(loop_node->inputs().at(i + 2)->type()->kind() == loop_node->outputs().at(i)->type()->kind(),
                   loop_node, "Mismatch loop for node types at input index", i + 2, "and output index", i);
        NODE_CHECK(loop_node->inputs().at(i + 2)->type()->kind() == block->inputs().at(i + 1)->type()->kind(),
                   loop_node, "Mismatch loop for node types at input index", i + 2, "and block input index", i + 1);
        NODE_CHECK(block->inputs().at(i + 1)->type()->kind() == block->outputs().at(i + 1)->type()->kind(), loop_node,
                   "Mismatch loop for node types at block input index", i + 1, "and block output index", i + 1);
    }
}

void assert_well_formed_if(const Node* if_node) {
    NODE_CHECK(if_node->kind() == c10::prim::If, if_node, "Internal error; checking a non-if statement");

    const Block *true_block = if_node->blocks().at(0), *false_block = if_node->blocks().at(1);

    // Checks that the sizes match everywhere.
    NODE_CHECK(if_node->outputs().size() == true_block->outputs().size(), if_node,
               "Mismatched if statement output size with true block output size");
    NODE_CHECK(if_node->outputs().size() == false_block->outputs().size(), if_node,
               "Mismatched if statement output size with false block output size");
    NODE_CHECK(if_node->inputs().size() == 1, if_node, "If statement should have exactly one input, got",
               if_node->inputs().size());
    NODE_CHECK(true_block->inputs().size() == 0, if_node, "If statement true block should not have any inputs, got",
               true_block->inputs().size());
    NODE_CHECK(false_block->inputs().size() == 0, if_node, "If statement false block should not have any inputs, got",
               false_block->inputs().size());

    // Checks that types match everywhere.
    for (size_t i = 0; i < if_node->outputs().size(); i++) {
        NODE_CHECK(if_node->outputs().at(i)->type()->kind() == true_block->outputs().at(i)->type()->kind(), if_node,
                   "Mismatched if statement output type with true block output type at index", i);
        NODE_CHECK(if_node->outputs().at(i)->type()->kind() == false_block->outputs().at(i)->type()->kind(), if_node,
                   "Mismatched if statement output type with false block output type at index", i);
    }
}

void run_all_checks(const Block* block, bool recurse) {
    for (const Node* node : block->nodes()) {
        if (recurse)
            for (const Block* subblock : node->blocks()) run_all_checks(subblock, recurse);

        switch (node->kind()) {
            case c10::prim::Loop:
                assert_well_formed_loop(node);
                break;
            case c10::prim::If:
                assert_well_formed_if(node);
                break;
        }
    }
}

void run_all_checks(const std::shared_ptr<Graph>& graph, bool recurse) {
    graph->lint();
    run_all_checks(graph->block(), recurse);
}

std::deque<Block*> blocks_between(Block* child, Block* parent) {
    std::deque<Block*> blocks;
    while (child != parent) {
        MCHECK(child->owningNode() != nullptr, "Child's owning node is null");
        blocks.push_back(child);
        child = child->owningNode()->owningBlock();
    }
    return blocks;
}

size_t count_distance(Block* child, Block* parent) {
    size_t dist = 0;
    while (child != parent) {
        MCHECK(child->owningNode() != nullptr, "Child's owning node is null");
        child = child->owningNode()->owningBlock();
    }
    return dist;
}

size_t block_depth(Block* block) { return count_distance(block, block->owningGraph()->block()); }

Block* common_block(Block* lhs, Block* rhs) {
    MCHECK(lhs->owningGraph() == rhs->owningGraph(), "Blocks are in different graphs");

    // Simple heuristic for most cases.
    if (lhs == rhs) return lhs;

    // Gets the distance to the graph block.
    Block* gblock = lhs->owningGraph()->block();
    size_t d_lhs = count_distance(lhs, gblock), d_rhs = count_distance(rhs, gblock);

    // Gets blocks which are on the same level.
    while (d_lhs > d_rhs) {
        MCHECK(lhs->owningNode() != nullptr, "LHS owning node is null");
        lhs = lhs->owningNode()->owningBlock();
        d_lhs--;
    }
    while (d_rhs > d_lhs) {
        MCHECK(rhs->owningNode() != nullptr, "RHS owning node is null");
        rhs = rhs->owningNode()->owningBlock();
        d_rhs--;
    }

    // Iterate upwards until both are the same.
    while (lhs != rhs) {
        MCHECK(lhs->owningNode() != nullptr && rhs->owningNode() != nullptr, "LHS or RHS owning node is null");
        lhs = lhs->owningNode()->owningBlock();
        rhs = rhs->owningNode()->owningBlock();
    }

    MCHECK(lhs != nullptr, "Common block is null");
    return lhs;
}

}  // namespace inference::passes::pass_utils
