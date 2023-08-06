#include "observer.h"

#include <torch/csrc/jit/runtime/custom_operator.h>

#include "../exceptions.h"
#include "../macros.h"

namespace inference::quantization::observer {

Observer::State Observer::serialize() {
    params::Params::State params_state = params->serialize();

    // Serializes range observers.
    std::vector<range_observer::RangeObserver::State> range_observer_states;
    range_observer_states.reserve(range_observers.size());
    for (auto &elem : range_observers) range_observer_states.push_back(elem.serialize());

    // Serializes shape observers.
    std::vector<shape_observer::ShapeObserver::State> shape_observer_states;
    shape_observer_states.reserve(shape_observers.size());
    for (auto &elem : shape_observers) shape_observer_states.push_back(elem.serialize());

    // Serializes stats trackers.
    std::vector<stats::Stats::State> stats_states;
    stats_states.reserve(stats.size());
    for (auto &elem : stats) stats_states.push_back(elem.serialize());

    return {has_been_called, params_state, range_observer_states, shape_observer_states, stats_states};
}

Observer Observer::deserialize(const Observer::State &state) {
    auto &[has_been_called_, params_state_, range_observer_states_, shape_observer_states_, stats_states_] = state;

    std::shared_ptr<params::Params> params_ =
        std::make_shared<params::Params>(params::Params::deserialize(params_state_));

    // Deserializes range observers.
    std::vector<range_observer::RangeObserver> range_observers_;
    range_observers_.reserve(range_observer_states_.size());
    for (size_t i = 0; i < range_observer_states_.size(); i++) {
        auto observer = range_observer::RangeObserver::deserialize(params_, i, range_observer_states_[i]);
        range_observers_.push_back(observer);
    }

    // Deserializes shape observers.
    std::vector<shape_observer::ShapeObserver> shape_observers_;
    shape_observers_.reserve(shape_observer_states_.size());
    for (size_t i = 0; i < shape_observer_states_.size(); i++) {
        auto observer = shape_observer::ShapeObserver::deserialize(params_, i, shape_observer_states_[i]);
        shape_observers_.push_back(observer);
    }

    // Deserializes stats trackers.
    std::vector<stats::Stats> stats_;
    stats_.reserve(stats_states_.size());
    for (const auto &elem_ : stats_states_) stats_.push_back(stats::Stats::deserialize(params_, elem_));

    return {has_been_called_, params_, range_observers_, shape_observers_, stats_};
}

torch::Tensor Observer::observe(torch::Tensor &t, std::tuple<int64_t, int64_t, int64_t, bool> ids) {
    has_been_called = true;

    const auto &[range_id, shape_id, tensor_id, is_output] = ids;

    if (params->get_observer_enabled()) {
        shape_observers[shape_id].observe(t);
        if (is_output) range_observers[range_id].observe(t);
    }

    if (t.is_floating_point()) {
        if (params->get_fake_quantize_enabled() && is_output) {
            torch::Tensor t_fq = range_observers[range_id].fake_quantize(t);
            if (params->get_track_quant_stats()) {
                stats[tensor_id].add_quant_err(t, t_fq);
            }
            t = t_fq;
        } else if (params->get_track_quant_stats()) {
            torch::Tensor t_fq = range_observers[range_id].fake_quantize(t);
            stats[tensor_id].add_quant_err(t, t_fq);
        }
    }

    return t;
}

void Observer::set_fake_quantize_enabled(bool val) { params->set_fake_quantize_enabled(val); }
bool Observer::get_fake_quantize_enabled() { return params->get_fake_quantize_enabled(); }
void Observer::set_observer_enabled(bool val) { params->set_observer_enabled(val); }
bool Observer::get_observer_enabled() { return params->get_observer_enabled(); }
void Observer::set_track_quant_stats(bool val) { params->set_track_quant_stats(val); }
bool Observer::get_track_quant_stats() { return params->get_track_quant_stats(); }
bool Observer::get_has_been_called() { return has_been_called; }

int64_t Observer::num_shapes() { return shape_observers.size(); }
int64_t Observer::num_ranges() { return range_observers.size(); }
int64_t Observer::num_tensors() { return stats.size(); }
shape_observer::shape_t Observer::get_shape(int64_t shape_id) { return shape_observers[shape_id].get_shape(); }
range_observer::range_t Observer::get_range(int64_t range_id) { return range_observers[range_id].get_range(); }
c10::optional<bool> Observer::is_floating_point(int64_t range_id) { return range_observers[range_id].get_is_fp(); }
double Observer::get_mean_sqnr(int64_t tensor_id) { return stats[tensor_id].mean_sqnr(); }
double Observer::get_mean_l1_err(int64_t tensor_id) { return stats[tensor_id].mean_l1_err(); }

torch::jit::RegisterOperators reg_observer_operators({
    Operator(
        "inference::observe(...) -> Tensor",
        [](const Node *node) -> Operation {
            int64_t range_id = node->i(c10::Symbol::fromQualString("attr::range")),
                    shape_id = node->i(c10::Symbol::fromQualString("attr::shape")),
                    tensor_id = node->i(c10::Symbol::fromQualString("attr::tensor")),
                    is_output = node->i(c10::Symbol::fromQualString("attr::output"));
            size_t num_inputs = node->inputs().size();
            MCHECK(num_inputs == 2, "Expected observer node to have two inputs");
            return [range_id, shape_id, tensor_id, is_output](Stack &stack) {
                at::ArrayRef<IValue> inputs = last(stack, 2);
                auto input_tensor = inputs.at(1).toTensor();
                auto result = inputs.at(0).toCustomClass<Observer>()->observe(
                    input_tensor, {range_id, shape_id, tensor_id, is_output != 0});
                drop(stack, 2);
                pack(stack, IValue(std::move(result)));
            };
        },
        c10::AliasAnalysisKind::FROM_SCHEMA),
});

void add_module(pybind11::module &m) {
    py::class_<Observer>(m, "Observer")
        .def("num_ranges", &Observer::num_ranges)
        .def("num_shapes", &Observer::num_shapes)
        .def("num_tensors", &Observer::num_tensors)
        .def("get_shape", &Observer::get_shape, "shape_id"_a)
        .def("get_range", &Observer::get_range, "range_id"_a)
        .def("is_floating_point", &Observer::is_floating_point, "range_id"_a);
}

void add_torch_module(torch::Library &m) {
    m.class_<Observer>("Observer")
        .def("observe", &Observer::observe)
        .def("set_fake_quantize_enabled", &Observer::set_fake_quantize_enabled)
        .def("get_fake_quantize_enabled", &Observer::get_fake_quantize_enabled)
        .def("set_observer_enabled", &Observer::set_observer_enabled)
        .def("get_observer_enabled", &Observer::get_observer_enabled)
        .def("set_track_quant_stats", &Observer::set_track_quant_stats)
        .def("get_track_quant_stats", &Observer::get_track_quant_stats)
        .def("get_has_been_called", &Observer::get_has_been_called)
        .def("num_ranges", &Observer::num_ranges)
        .def("num_shapes", &Observer::num_shapes)
        .def("num_tensors", &Observer::num_tensors)
        .def("get_shape", &Observer::get_shape)
        .def("get_range", &Observer::get_range)
        .def("is_floating_point", &Observer::is_floating_point)
        .def("get_mean_sqnr", &Observer::get_mean_sqnr)
        .def("get_mean_l1_err", &Observer::get_mean_l1_err)
        .def_pickle(
            [](c10::intrusive_ptr<Observer> self) { return self->serialize(); },
            [](const Observer::State &state) { return c10::make_intrusive<Observer>(Observer::deserialize(state)); });
}

}  // namespace inference::quantization::observer
