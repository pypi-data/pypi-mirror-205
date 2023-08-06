#pragma once

#include <torch/extension.h>

#include "params.h"

namespace inference::quantization::stats {

/**
 * Tracks quantization statistics for a given observer.
 *
 * Metrics:
 *  - Signal to Quantization Noise Ratio (SQNR)
 *  - L1 Error
 */
class Stats {
   private:
    size_t num_samples;
    double total_sqnr, total_l1_err;

    std::shared_ptr<params::Params> params;

   public:
    Stats(std::shared_ptr<params::Params> &params_)
        : params(params_), num_samples(0), total_sqnr(0.0), total_l1_err(0.0) {}
    Stats(std::shared_ptr<params::Params> &params_, size_t num_samples_, double total_sqnr_, double total_l1_err_)
        : params(params_), num_samples(num_samples_), total_sqnr(total_sqnr_), total_l1_err(total_l1_err_) {}

    /* Adds quantization error metrics */
    void add_quant_err(torch::Tensor &ref, torch::Tensor &quantized);

    /* Accessors for statistics. */
    double mean_sqnr();
    double mean_l1_err();

    /* Serialization */
    using State = std::tuple<int64_t, double, double>;
    State serialize();
    static Stats deserialize(std::shared_ptr<params::Params> &params, const State &state);
};

}  // namespace inference::quantization::stats
