#include "inference.h"

namespace inference {

PYBIND11_MODULE(inference, m) {
    config::add_module(m);
    exceptions::add_module(m);
    graph::add_module(m);
    passes::add_module(m);
    preprocess::add_module(m);
    quantization::add_module(m);
}

TORCH_LIBRARY(inference, m) { quantization::add_torch_module(m); }

}  // namespace inference
