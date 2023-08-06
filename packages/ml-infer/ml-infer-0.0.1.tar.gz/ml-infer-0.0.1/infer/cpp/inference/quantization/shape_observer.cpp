#include "shape_observer.h"

#include "observer_utils.h"

namespace inference::quantization::shape_observer {

shape_t ShapeObserver::get_shape() { return shape; }

std::vector<c10::optional<int64_t>> tensor_shape_to_vec(const torch::Tensor &t) {
    const auto sizes = t.sizes();
    std::vector<c10::optional<int64_t>> new_vector;
    std::copy(sizes.begin(), sizes.end(), std::back_inserter(new_vector));
    return new_vector;
}

void ShapeObserver::observe(torch::Tensor &t) {
    // If calling for the first time, just copy the shape from the tensor.
    if (!shape.has_value()) {
        shape.emplace(tensor_shape_to_vec(t));
        return;
    }

    // The number of dimensions should always be constant.
    const auto tensor_shape = tensor_shape_to_vec(t);
    auto &shape_vec = shape.value();
    MCHECK(shape_vec.size() == tensor_shape.size(), "Number of dimensions is not constant!");

    // Checks for disagreeing dimensions; dimensions which disagree are nulled.
    for (int i = 0; i < tensor_shape.size(); i++) {
        if (shape_vec[i].has_value() && shape_vec[i].value() != tensor_shape[i]) {
            shape_vec[i] = c10::nullopt;
        }
    }
}

void ShapeObserver::make_groups(disjoint_set::DisjointSet<const Value *> &shape_groups, const Value *tensor) {
    if (observer_utils::make_common_groups(shape_groups, tensor)) return;

    switch (tensor->node()->kind()) {
        /* In-place ops at export time */
        case aten::batch_norm:
        case aten::relu:
        case aten::relu_:
        case aten::relu6:
        case aten::relu6_:
        case aten::hardtanh:
        case aten::hardtanh_:
        case aten::clamp:
        case aten::clamp_:
        case aten::clamp_min:
        case aten::clamp_min_:
        case aten::clamp_max:
        case aten::clamp_max_:
            shape_groups.maybe_join(tensor, tensor->node()->input(0));
            return;
    }
}

ShapeObserver::State ShapeObserver::serialize() { return {shape}; }

ShapeObserver ShapeObserver::deserialize(std::shared_ptr<params::Params> &params_, int64_t shape_id_,
                                         const ShapeObserver::State &state) {
    const auto &[shape_] = state;
    return {params_, shape_id_, shape_};
}

}  // namespace inference::quantization::shape_observer
