#include "params.h"

namespace inference::quantization::params {

QuantParams::State QuantParams::serialize() { return {bins, upsample_rate}; }

QuantParams QuantParams::deserialize(const QuantParams::State& state) { return {state}; }

Params::State Params::serialize() {
    return {fake_quantize_enabled, observer_enabled, track_quant_stats, quant->serialize()};
}

Params Params::deserialize(const Params::State& state) { return {state}; }

}  // namespace inference::quantization::params
