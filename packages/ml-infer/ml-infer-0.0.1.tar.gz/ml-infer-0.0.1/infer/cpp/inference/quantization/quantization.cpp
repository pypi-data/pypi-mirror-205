#include "quantization.h"

#include "../exceptions.h"
#include "../graph/implicit_tensors.h"
#include "../graph/method_graphs.h"
#include "../macros.h"
#include "disjoint_set.h"
#include "observer.h"
#include "range_observer.h"
#include "shape_observer.h"
#include "stats.h"

namespace inference::quantization {

bool is_output(const torch::jit::Node *node) {
    const torch::Symbol kind = node->kind();
    switch (kind) {
        case prim::Return:
            return true;
        case prim::TupleConstruct:
        case prim::ListConstruct:
        case prim::DictConstruct: {
            for (const Use use : node->output()->uses())
                if (is_output(use.user)) return true;
            return false;
        }
        default:
            return false;
    }
}

Module insert_observers(Module &mod, const config::Config &config, bool copy) {
    MCHECK(!mod.hasattr(OBSERVER_NAME), "Module already has a registered observer!");

    if (copy) mod = mod.clone();
    auto method_graphs = graph::method_graphs::get_method_graphs(mod, config);
    auto implicit_tensors = graph::implicit_tensors::get_implicit_tensors(mod, config);

    // Creates the params object from the config.
    std::shared_ptr<params::Params> params = std::make_shared<params::Params>(config);

    // Flattens tensors to a vector and gets unique IDs.
    std::vector<Value *> all_tensors;
    for (auto &[method_name, method_tensors] : implicit_tensors)
        std::copy(method_tensors.begin(), method_tensors.end(), std::back_inserter(all_tensors));
    std::unordered_map<const Value *, int64_t> tensor_ids;
    for (size_t i = 0; i < all_tensors.size(); i++) tensor_ids.emplace(all_tensors[i], i);

    // Gets the range observer groups.
    disjoint_set::DisjointSet<const Value *> range_groups;
    for (const auto &tensor : all_tensors) range_groups.add(tensor);
    for (const auto &tensor : all_tensors) range_observer::RangeObserver::make_groups(range_groups, tensor);
    const std::unordered_map<const Value *, size_t> range_group_ids = range_groups.set_ids();
    const size_t num_range_groups = range_groups.num_sets();
    std::vector<range_observer::RangeObserver> range_observers;
    range_observers.reserve(num_range_groups);
    for (size_t i = 0; i < num_range_groups; i++) {
        range_observer::RangeObserver range_observer(params, i);
        range_observers.push_back(range_observer);
    }

    // Checks each user to see if it has tensors with a different group ID.
    auto has_diff_group_user = [&range_group_ids](const Value *tensor, const size_t group_id) {
        for (const Use use : tensor->uses()) {
            if (is_output(use.user)) return true;
            for (const Value *out_tensor : use.user->outputs()) {
                if (range_group_ids.find(out_tensor) != range_group_ids.end() &&
                    range_group_ids.at(out_tensor) != group_id) {
                    return true;
                }
            }
        }
        return false;
    };

    // Gets the range observer outputs.
    std::unordered_set<const Value *> outputs;
    for (const auto &[tensor, group_id] : range_group_ids) {
        if (has_diff_group_user(tensor, group_id)) outputs.emplace(tensor);
        range_observers[group_id].set_static_range_for(tensor);
    }
    MCHECK(outputs.size() > 0, "Expected at least one output tensor!");

    // Gets the shape observer groups.
    disjoint_set::DisjointSet<const Value *> shape_groups;
    for (const auto &tensor : all_tensors) shape_groups.add(tensor);
    for (const auto &tensor : all_tensors) shape_observer::ShapeObserver::make_groups(shape_groups, tensor);
    const std::unordered_map<const Value *, size_t> shape_group_ids = shape_groups.set_ids();
    const size_t num_shape_groups = shape_groups.num_sets();
    std::vector<shape_observer::ShapeObserver> shape_observers;
    shape_observers.reserve(num_shape_groups);
    for (size_t i = 0; i < num_shape_groups; i++) {
        shape_observer::ShapeObserver shape_observer(params, i);
        shape_observers.push_back(shape_observer);
    }

    // Gets the quantization statistics trackers.
    std::vector<stats::Stats> stats;
    std::unordered_map<const Value *, size_t> stat_ids;
    stats.reserve(all_tensors.size());
    for (size_t i = 0; i < all_tensors.size(); i++) {
        stats::Stats stat(params);
        stats.push_back(stat);
        stat_ids.emplace(all_tensors[i], i);
    }

    // Creates the observer and adds it to the module.
    auto obs_obj = c10::make_intrusive<observer::Observer>(false, params, range_observers, shape_observers, stats);
    auto obs_obj_ivalue = c10::IValue(std::move(obs_obj));
    mod.register_attribute(OBSERVER_NAME, obs_obj_ivalue.type(), obs_obj_ivalue, /* is_parameter */ false,
                           /* is_buffer */ false);

    // Calls the observer after every implicit tensor.
    for (auto &[method_name, method_tensors] : implicit_tensors) {
        Value *obs_acc = nullptr;

        for (auto &tensor : method_tensors) {
            auto graph = tensor->owningGraph();

            // Creates accessor, if one is not created yet.
            if (obs_acc == nullptr) {
                Value *self = graph->inputs().at(0);
                Node *obs_acc_node = graph->createGetAttr(self, OBSERVER_NAME);
                obs_acc_node->insertAfter(graph->param_node());
                obs_acc = obs_acc_node->output();
            }

            // Creates a new observed tensor after the tensor.
            Node *obs_node = graph->create(c10::Symbol::fromQualString("inference::observe"), {obs_acc, tensor}, 1);
            Node *observed_node = tensor->node()->isBefore(obs_acc->node()) ? obs_acc->node() : tensor->node();
            obs_node->copyMetadata(observed_node);
            Value *obs_value =
                obs_node->insertAfter(observed_node)
                    ->i_(c10::Symbol::fromQualString("attr::range"), range_group_ids.at(tensor))
                    ->i_(c10::Symbol::fromQualString("attr::shape"), shape_group_ids.at(tensor))
                    ->i_(c10::Symbol::fromQualString("attr::tensor"), stat_ids.at(tensor))
                    ->i_(c10::Symbol::fromQualString("attr::output"), outputs.find(tensor) == outputs.end() ? 0 : 1)
                    ->output()
                    ->setType(tensor->type());

            // Replaces uses of the tensor with the observed tensor.
            tensor->replaceAllUsesAfterNodeWith(obs_node, obs_value);
        }
    }

    return mod;
}

void add_module(pybind11::module &m) {
    m.def("insert_observers", &insert_observers, "mod"_a, "config"_a, "copy"_a);
    m.def("observer_name", []() -> std::string { return OBSERVER_NAME; });

    observer::add_module(m);
    disjoint_set::add_module(m);
}

void add_torch_module(torch::Library &m) { observer::add_torch_module(m); }

}  // namespace inference::quantization
