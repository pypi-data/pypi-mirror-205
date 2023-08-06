#include "loop_unrolling.h"

#include <torch/csrc/jit/passes/dead_code_elimination.h>

#include "../exceptions.h"

namespace inference::passes::loop_unrolling {

const static size_t MAX_LOOP_COUNT_TO_UNROLL = 32;

bool is_true_constant(Value* val) {
    c10::optional<bool> maybe_value = constant_as<bool>(val);
    return maybe_value && *maybe_value;
}

bool is_for_loop(Node* node) {
    if (node->kind() != prim::Loop) return false;
    Value* start_cond = node->inputs().at(1);
    Value* continue_cond = node->blocks().at(0)->outputs().at(0);
    return is_true_constant(start_cond) && is_true_constant(continue_cond);
}

void inline_body(Node* loop) {
    auto graph = loop->owningGraph();
    auto body = loop->blocks().at(0);
    WithInsertPoint insert_point_guard{loop};

    std::unordered_map<Value*, Value*> value_map;
    auto get_value = [&](Value* v) {
        auto it = value_map.find(v);
        if (it != value_map.end()) return it->second;
        return v;
    };

    for (size_t i = 2; i < loop->inputs().size(); ++i) {
        value_map[body->inputs()[i - 1]] = loop->inputs()[i];
    }

    for (Node* orig : body->nodes()) {
        Node* clone = graph->insertNode(graph->createClone(orig, get_value));
        for (size_t i = 0; i < orig->outputs().size(); ++i) {
            value_map[orig->outputs()[i]] = clone->outputs()[i];
        }
    }
    for (size_t i = 0; i < loop->outputs().size(); ++i) {
        loop->outputs().at(i)->replaceAllUsesWith(get_value(body->outputs().at(i + 1)));
    }

    loop->destroy();
}

std::vector<Value*> insert_block_copy(Graph& graph, Block* body, at::ArrayRef<Value*> inputs) {
    NODE_CHECK(inputs.size() == body->inputs().size(), body->owningNode(),
               "Inputs size doesn't match body inputs size");

    std::unordered_map<Value*, Value*> value_map;
    auto get_value = [&](Value* v) {
        auto it = value_map.find(v);
        if (it != value_map.end()) return it->second;
        return v;
    };
    auto inputs_it = inputs.begin();
    for (Value* input : body->inputs()) {
        value_map[input] = *inputs_it++;
    }
    for (Node* node : body->nodes()) {
        Node* new_node = graph.insertNode(graph.createClone(node, get_value));
        auto outputs_it = new_node->outputs().begin();
        for (Value* output : node->outputs()) {
            value_map[output] = *outputs_it++;
        }
    }
    return fmap(body->outputs(), get_value);
}

void repeat_body(Block* body, size_t times, Block* dest) {
    auto graph = body->owningGraph();
    WithInsertPoint insert_point_guard(dest);
    for (Value* input : body->inputs()) {
        dest->addInput()->copyMetadata(input);
    }

    std::vector<Value*> io = dest->inputs().vec();
    NODE_CHECK(!body->inputs().at(0)->hasUses(), body->owningNode(), "Loop counter should be unused");

    for (const auto i : c10::irange(times)) {
        (void)i;  // Suppress unused variable warning
        io[0] = body->inputs().at(0);
        io = insert_block_copy(*graph, body, io);
    }
    for (Value* output : io) {
        dest->registerOutput(output);
    }

    EliminateDeadCode(dest, false);
}

void replace_loop_counter(Node* loop) {
    Graph* graph = loop->owningGraph();
    Block* body = loop->blocks().at(0);
    WithInsertPoint guard(loop);
    Value* init_counter = graph->insertConstant(0);

    loop->insertInput(2, init_counter);
    loop->insertOutput(0)->setType(IntType::get());

    Value* internal_counter = body->insertInput(1)->setType(init_counter->type());
    body->inputs()[0]->replaceAllUsesWith(internal_counter);

    WithInsertPoint insertPointGuard{body->return_node()};
    Value* result = graph->insert(aten::add, {internal_counter, 1});
    body->insertOutput(1, result);
}

bool unroll_loop(Node* loop) {
    MCHECK(loop->kind() == c10::prim::Loop, "Internal assertion; node is not a loop");

    // If the loop is not a for loop, don't unroll.
    if (!is_for_loop(loop)) return false;

    Graph* graph = loop->owningGraph();
    Block* body = loop->blocks().at(0);

    // If the loop counter doesn't have any uses, don't unroll.
    if (!body->inputs()[0]->hasUses()) return false;

    // We will be using a "mutable" counter outside of the loop instead of the
    // default one, because this will allow us to share it between the unrolled
    // loop and its epilogue. This is necessary only if the loop counter is
    // actually used in the body.
    replace_loop_counter(loop);

    Value* trip_count = loop->inputs().at(0);
    c10::optional<int64_t> const_len = constant_as<int64_t>(trip_count);

    // If the trip count is not constant or is very large, don't unroll.
    // This could be smarter - this depends on the expectation on the TensorRT
    // side for what the module parameters should be.
    if (!const_len || *const_len > MAX_LOOP_COUNT_TO_UNROLL) return true;

    Block* dest = loop->addBlock();
    repeat_body(body, *const_len, dest);
    loop->eraseBlock(0);
    inline_body(loop);
    return true;
}

bool unroll_loops(Block* block) {
    bool modified = false;

    for (Node* node : block->nodes()) {
        for (Block* subblock : node->blocks()) modified |= unroll_loops(subblock);

        switch (node->kind()) {
            case c10::prim::Loop:
                modified |= unroll_loop(node);
                break;
        }
    }

    return modified;
}

bool UnrollLoops(std::shared_ptr<Graph>& graph) { return unroll_loops(graph->block()); }

}  // namespace inference::passes::loop_unrolling
