#pragma once

#include <pybind11/pybind11.h>

namespace inference::config {

struct Config {
    enum Target { TensorRT = 0 };
    Target target = Target::TensorRT;
    std::unordered_set<std::string> exclude_funcs = {};
    bool default_fake_quantize_enabled = false;
    bool default_observer_enabled = true;
    bool default_track_quant_stats = false;
    int64_t default_histogram_bins = 2048;
    int64_t default_histogram_upsample_rate = 128;
    std::string export_func = "forward";
};

void add_module(pybind11::module &m);

}  // namespace inference::config
