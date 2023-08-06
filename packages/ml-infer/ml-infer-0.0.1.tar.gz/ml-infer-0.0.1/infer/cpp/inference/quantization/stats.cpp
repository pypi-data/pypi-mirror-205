#include "stats.h"

#include "../exceptions.h"

namespace inference::quantization::stats {

double compute_l1_err(torch::Tensor &ref, torch::Tensor &quantized) {
    return torch::norm(ref - quantized, /* p */ 1).item().toDouble();
}

// Reference:
// https://pytorch.org/tutorials/prototype/numeric_suite_tutorial.html#compare-the-weights-of-float-and-quantized-models
double compute_sqnr(torch::Tensor &ref, torch::Tensor &quantized) {
    torch::Tensor Ps = torch::norm(ref), Pn = torch::norm(ref - quantized);
    return 20.0 * torch::log10(Ps / Pn).item().toDouble();
}

void Stats::add_quant_err(torch::Tensor &ref, torch::Tensor &quantized) {
    num_samples++;
    total_sqnr += compute_sqnr(ref, quantized);
    total_l1_err += compute_l1_err(ref, quantized);
}

double Stats::mean_sqnr() { return num_samples == 0 ? 0 : total_sqnr / num_samples; }
double Stats::mean_l1_err() { return num_samples == 0 ? 0 : total_l1_err / num_samples; }

Stats::State Stats::serialize() { return {num_samples, total_sqnr, total_l1_err}; }

Stats Stats::deserialize(std::shared_ptr<params::Params> &params, const Stats::State &state) {
    const auto &[num_samples_, total_sqnr_, total_l1_err_] = state;
    MCHECK(num_samples_ >= 0, "`num_samples` should be non-negative");
    return {params, (size_t)num_samples_, total_sqnr_, total_l1_err_};
}

}  // namespace inference::quantization::stats
