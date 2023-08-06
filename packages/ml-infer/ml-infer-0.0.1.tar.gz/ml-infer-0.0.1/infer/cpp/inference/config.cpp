#include "config.h"

#include <pybind11/stl.h>

using namespace pybind11::literals;

namespace inference::config {

void add_module(pybind11::module &m) {
    pybind11::class_<Config> config(m, "Config");

    config.def(pybind11::init<>())
        .def(pybind11::init<Config>())
        .def_readwrite("target", &Config::target)
        .def_readwrite("exclude_funcs", &Config::exclude_funcs)
        .def_readwrite("default_fake_quantize_enabled", &Config::default_fake_quantize_enabled)
        .def_readwrite("default_observer_enabled", &Config::default_observer_enabled)
        .def_readwrite("default_track_quant_stats", &Config::default_track_quant_stats)
        .def_readwrite("default_histogram_bins", &Config::default_histogram_bins)
        .def_readwrite("default_histogram_upsample_rate", &Config::default_histogram_upsample_rate)
        .def_readwrite("export_func", &Config::export_func);

    pybind11::enum_<Config::Target>(config, "Target").value("TensorRT", Config::Target::TensorRT).export_values();
}

}  // namespace inference::config
