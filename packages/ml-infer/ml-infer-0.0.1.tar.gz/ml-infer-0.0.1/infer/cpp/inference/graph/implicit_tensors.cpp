#include "implicit_tensors.h"

#include "../config.h"
#include "../exceptions.h"
#include "../macros.h"
#include "method_graphs.h"

namespace inference::graph::implicit_tensors {

bool is_tensor_type(const TypePtr &type) { return type->cast<TensorType>() != nullptr; }

bool is_module_type(const TypePtr &type) { return type->cast<ClassType>() != nullptr; }

bool is_tensor_or_tensor_container_type(const TypePtr &type) {
    if (type->containedTypeSize() == 0) return is_tensor_type(type);
    if (type->cast<ListType>() != nullptr || type->cast<DictType>() != nullptr || type->cast<TupleType>() != nullptr ||
        type->cast<OptionalType>() != nullptr)
        for (const TypePtr contained_type : type->containedTypes())
            if (is_tensor_or_tensor_container_type(contained_type)) return true;
    return false;
}

bool is_tensor_container_type(const TypePtr &type) {
    return !is_tensor_type(type) && is_tensor_or_tensor_container_type(type);
}

void get_input_tensors(Value *v, std::unordered_set<Value *> &values, std::deque<Value *> &to_visit) {
    if (is_tensor_type(v->type())) {
        if (values.find(v) == values.end()) {
            values.emplace(v);
            to_visit.emplace_back(v);
        }
    } else if (is_tensor_or_tensor_container_type(v->type())) {
        for (Use use : v->uses()) {
            for (Value *use_val : use.user->outputs()) {
                get_input_tensors(use_val, values, to_visit);
            }
        }
    }
}

void get_output_tensors(Value *v, std::unordered_set<Node *> &terminals) {
    if (is_tensor_container_type(v->type())) {
        terminals.emplace(v->node());
        for (Value *in_val : v->node()->inputs()) get_output_tensors(in_val, terminals);
    }
}

std::unordered_map<std::string, std::unordered_set<Value *>> get_implicit_tensors(Module &mod,
                                                                                  const config::Config &config) {
    std::unordered_map<std::string, std::unordered_set<Value *>> values_map;
    std::vector<exceptions::NodeException> errs;

    // Simply does BFS to visit all user tensors for each method.
    for (auto &[method_name, graph] : method_graphs::get_method_graphs(mod, config)) {
        std::unordered_set<Value *> values, visited;
        std::unordered_set<Node *> terminals;

        std::deque<Value *> to_visit;
        for (Value *input_value : graph->inputs()) get_input_tensors(input_value, values, to_visit);
        for (Value *output_value : graph->outputs()) get_output_tensors(output_value, terminals);

        // Visits the value, adding it to the set. If it is not a terminal
        // tensor, also add it to the BFS queue. This is done to ensure that
        // any tensor containers are at the end of the graph.
        auto visit = [&](Value *v) -> void {
            if (terminals.find(v->node()) != terminals.end()) return;
            if (visited.find(v) != visited.end()) return;

            visited.emplace(v);

            try {
                VALUE_CHECK(!is_tensor_container_type(v->type()), v,
                            "Found a container of tensors which don't have concrete values at export time");
            } catch (exceptions::NodeException &e) {
                errs.push_back(e);
            }

            // Checks errors here, to avoid checking too many errors.
            EMPTY_CHECK_INTERMEDIATE(errs, "Caught exception(s) while attempting to get implicit tensors");

            // Adds the value, if it is a tensor.
            if (is_tensor_type(v->type())) values.emplace(v);

            // Visits the value.
            to_visit.emplace_back(v);
        };

        while (!to_visit.empty()) {
            const Value *value = to_visit.front();
            to_visit.pop_front();
            for (Use use : value->uses()) {
                for (Value *output : use.user->outputs()) visit(output);

                // Handles statements across lists.
                switch (use.user->kind()) {
                    case c10::prim::Loop:
                        if (use.offset >= 2) visit(use.user->output(use.offset - 2));
                        if (use.offset >= 1) visit(use.user->blocks().at(0)->inputs().at(use.offset - 1));
                        break;
                    case c10::prim::Return:
                        if (use.user->owningBlock()->owningNode() != nullptr &&
                            use.user->owningBlock()->owningNode()->kind() == c10::prim::If)
                            visit(use.user->owningBlock()->owningNode()->output(use.offset));
                        break;
                }
            }
        }

        values_map.emplace(method_name, values);
    }

    // Throw an error if we caught any exceptions.
    EMPTY_CHECK(errs, "Caught exception(s) while attempting to get implicit tensors");

    return values_map;
}

std::unordered_map<std::string, std::unordered_set<std::string>> get_implicit_tensor_names(
    Module &mod, const config::Config &config) {
    std::unordered_map<std::string, std::unordered_set<Value *>> values_map = get_implicit_tensors(mod, config);

    // Gets the debug name for each value pointer.
    std::unordered_map<std::string, std::unordered_set<std::string>> value_names_map;
    value_names_map.reserve(values_map.size());
    for (const auto &[method_name, values] : values_map) {
        std::unordered_set<std::string> value_names;
        value_names.reserve(values.size());
        for (const Value *value : values) value_names.emplace(value->debugName());
        value_names_map.emplace(method_name, value_names);
    }

    return value_names_map;
}

void add_module(pybind11::module &m) { m.def("get_implicit_tensors", &get_implicit_tensor_names, "mod"_a, "config"_a); }

}  // namespace inference::graph::implicit_tensors
