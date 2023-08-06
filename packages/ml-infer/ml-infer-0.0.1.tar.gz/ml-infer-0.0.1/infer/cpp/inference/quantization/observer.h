#pragma once

#include <pybind11/pybind11.h>
#include <torch/custom_class.h>
#include <torch/extension.h>

#include "../config.h"
#include "params.h"
#include "range_observer.h"
#include "shape_observer.h"
#include "stats.h"

using namespace pybind11::literals;

namespace inference::quantization::observer {

struct Observer : torch::CustomClassHolder {
    bool has_been_called;

    /* Contains the observer's parameters. */
    std::shared_ptr<params::Params> params;

    /* Contains the range and shape observers. */
    std::vector<range_observer::RangeObserver> range_observers;
    std::vector<shape_observer::ShapeObserver> shape_observers;

    /* Contains the quantization statistics tracker. */
    std::vector<stats::Stats> stats;

    /* Constructors */
    Observer(bool has_been_called_, std::shared_ptr<params::Params> params_,
             std::vector<range_observer::RangeObserver> range_observers_,
             std::vector<shape_observer::ShapeObserver> shape_observers_, std::vector<stats::Stats> stats_)
        : has_been_called(has_been_called_),
          params(params_),
          range_observers(range_observers_),
          shape_observers(shape_observers_),
          stats(stats_) {}

    /* Functions that are called in the graph */
    torch::Tensor observe(torch::Tensor &t, std::tuple<int64_t, int64_t, int64_t, bool> ids);

    /* Params accessors */
    void set_fake_quantize_enabled(bool val);
    bool get_fake_quantize_enabled();
    void set_observer_enabled(bool val);
    bool get_observer_enabled();
    void set_track_quant_stats(bool val);
    bool get_track_quant_stats();
    bool get_has_been_called();

    /* Observer accessors. */
    int64_t num_ranges();
    int64_t num_shapes();
    int64_t num_tensors();
    shape_observer::shape_t get_shape(int64_t shape_id);
    range_observer::range_t get_range(int64_t range_id);
    c10::optional<bool> is_floating_point(int64_t range_id);
    double get_mean_sqnr(int64_t tensor_id);
    double get_mean_l1_err(int64_t tensor_id);

    /* Serialization */
    using State = std::tuple<bool, params::Params::State, std::vector<range_observer::RangeObserver::State>,
                             std::vector<shape_observer::ShapeObserver::State>, std::vector<stats::Stats::State>>;
    State serialize();
    static Observer deserialize(const State &state);
};

void add_module(pybind11::module &m);

void add_torch_module(torch::Library &m);

}  // namespace inference::quantization::observer
