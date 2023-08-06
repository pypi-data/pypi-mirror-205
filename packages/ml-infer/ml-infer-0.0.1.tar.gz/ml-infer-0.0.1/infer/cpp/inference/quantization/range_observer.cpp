#include "range_observer.h"

#include "observer_utils.h"

namespace inference::quantization::range_observer {

bool RangeObserver::is_floating_point(torch::Tensor &t) {
    const bool t_fp = t.is_floating_point();
    if (is_fp.has_value()) {
        const bool o_fp = is_fp.value();
        MCHECK(t_fp == o_fp, "Found datatype disagreement; observer expected", o_fp ? "floating point" : "integer",
               "type while tensor has", t_fp ? "floating point" : "integer", "type for range ID =", range_id);
    } else {
        is_fp.emplace(t_fp);
    }
    return t_fp;
}

void RangeObserver::observe(torch::Tensor &t) {
    if (!is_floating_point(t)) return;  // Don't do anything for non-FP tensors.

    if (static_range) {
        MCHECK(range.has_value(), "Tensors with a static range should already have range values");
    } else {
        auto [min_val, max_val] = t.aminmax();
        auto new_min = min_val.cpu().item().toDouble(), new_max = max_val.cpu().item().toDouble();
        if (range.has_value()) {
            auto &[cur_min, cur_max] = range.value();
            range = {std::min(new_min, cur_min), std::max(new_max, cur_max)};
        } else {
            range = {new_min, new_max};
        }
    }
}

void RangeObserver::set_static_range(double min_val, double max_val) {
    if (static_range) {
        MCHECK(range.has_value(), "Tensors with a static range should already have range values");
    }

    if (range.has_value()) {
        auto &[range_min_val, range_max_val] = range.value();
        MCHECK(abs(range_min_val - min_val) < 1e-4 && abs(range_max_val - max_val) < 1e-4,
               "Can't change an existing static range to a different range!");
    } else {
        range = {min_val, max_val};
        static_range = true;
    }
}

range_t RangeObserver::get_range() { return range; }
c10::optional<bool> RangeObserver::get_is_fp() { return is_fp; }

torch::Tensor RangeObserver::fake_quantize(torch::Tensor &t) {
    if (!is_floating_point(t)) return t;  // Don't do anything for non-FP tensors.

    MCHECK(range.has_value(), "Cannot fake quantize before observing tensor range");
    const auto &[min_val, max_val] = range.value();
    const double scale = std::max(-min_val, max_val * 128 / 127) / 256;

    // Necessary since fake quantize isn't implemented for bFloat16 yet.
    torch::Tensor fq_tensor = torch::fake_quantize_per_tensor_affine(
                                  t.dtype() == torch::kBFloat16 ? t.to(torch::kFloat16) : t, scale, 0, -128, 127)
                                  .to(t.dtype());

    return fq_tensor;
}

void RangeObserver::set_static_range_for(const Value *tensor) {
    const auto &node_kind = tensor->node()->kind();

    switch (node_kind) {
        case aten::one_hot:
        case aten::softmax:

            /* Range should always be from zero to one. */
            set_static_range(0.0, 1.0);
            return;
    }
}

void RangeObserver::make_groups(disjoint_set::DisjointSet<const Value *> &range_groups, const Value *tensor) {
    if (observer_utils::make_common_groups(range_groups, tensor)) return;

    const auto &node_kind = tensor->node()->kind();

    switch (node_kind) {
        /* In-place ops at export time */
        case aten::batch_norm:
        case aten::clamp_:
        case aten::clamp_max_:
        case aten::clamp_max:
        case aten::clamp_min_:
        case aten::clamp_min:
        case aten::clamp:
        case aten::hardtanh_:
        case aten::hardtanh:
        case aten::relu_:
        case aten::relu:
        case aten::relu6_:
        case aten::relu6:

        /* Memory manipulation ops */
        case aten::clone:
        case aten::copy_:
        case aten::copy:
        case aten::flatten:
        case aten::squeeze_:
        case aten::squeeze:
        case aten::transpose_:
        case aten::transpose:
        case aten::unflatten:
        case aten::unsqueeze_:
        case aten::unsqueeze:
        case prim::FusedConcat:

            /* Merge all inputs and outputs */
            for (const Value *input_tensor : tensor->node()->inputs()) range_groups.maybe_join(tensor, input_tensor);
            return;
    }

    // Custom operations.
    if (node_kind == c10::Symbol::fromQualString("inference::chunk") ||
        node_kind == c10::Symbol::fromQualString("inference::cat")) {
        for (const Value *input_tensor : tensor->node()->inputs()) range_groups.maybe_join(tensor, input_tensor);
        return;
    }
}

RangeObserver::State RangeObserver::serialize() { return {range, static_range, is_fp}; }

RangeObserver RangeObserver::deserialize(std::shared_ptr<params::Params> &params_, int64_t range_id_,
                                         const RangeObserver::State &state) {
    const auto &[range_, static_range_, is_fp_] = state;
    return {params_, range_id_, range_, static_range_, is_fp_};
}

}  // namespace inference::quantization::range_observer
