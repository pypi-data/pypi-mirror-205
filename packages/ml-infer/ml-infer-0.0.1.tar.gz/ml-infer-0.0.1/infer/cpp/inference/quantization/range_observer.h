#pragma once

#include <torch/extension.h>

#include "disjoint_set.h"
#include "params.h"

using namespace torch::jit;

namespace inference::quantization::range_observer {

typedef c10::optional<std::tuple<double, double>> range_t;

class RangeObserver {
   private:
    range_t range;
    int64_t range_id;
    bool static_range;
    c10::optional<bool> is_fp;

    std::shared_ptr<params::Params> params;
    std::shared_ptr<params::QuantParams> quant_params;

   public:
    /* Constructor */
    RangeObserver(std::shared_ptr<params::Params>& params_, int64_t range_id_)
        : params(params_),
          quant_params(params_->get_quant_params()),
          range_id(range_id_),
          range(),
          static_range(false),
          is_fp(c10::nullopt) {}
    RangeObserver(std::shared_ptr<params::Params>& params_, int64_t range_id_, range_t range_, bool static_range_,
                  c10::optional<bool> is_fp_)
        : params(params_),
          quant_params(params_->get_quant_params()),
          range_id(range_id_),
          range(range_),
          static_range(static_range_),
          is_fp(is_fp_) {}

    /* Functions that are called on the tensor */
    bool is_floating_point(torch::Tensor& t);
    void observe(torch::Tensor& t);
    torch::Tensor fake_quantize(torch::Tensor& t);

    /* Accessors */
    range_t get_range();
    c10::optional<bool> get_is_fp();
    void set_static_range(double min_val, double max_val);

    /* Determines */
    void set_static_range_for(const Value* tensor);

    /* Determmines tensor grouping */
    static void make_groups(disjoint_set::DisjointSet<const Value*>& range_groups, const Value* tensor);

    /* Serialization */
    using State = std::tuple<range_t, bool, c10::optional<bool>>;
    State serialize();
    static RangeObserver deserialize(std::shared_ptr<params::Params>& params_, int64_t range_id_, const State& state);
};

}  // namespace inference::quantization::range_observer
