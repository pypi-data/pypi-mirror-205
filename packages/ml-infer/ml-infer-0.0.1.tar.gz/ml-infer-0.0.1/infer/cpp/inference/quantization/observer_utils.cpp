#include "observer_utils.h"

namespace inference::quantization::observer_utils {

bool make_common_groups(disjoint_set::DisjointSet<const Value*>& groups, const Value* tensor) {
    switch (tensor->node()->kind()) {
        /* Loops */
        case prim::Loop:
            groups.maybe_join(tensor, tensor->node()->blocks().at(0)->inputs().at(tensor->offset() + 1));
            groups.maybe_join(tensor, tensor->node()->blocks().at(0)->outputs().at(tensor->offset() + 1));
            groups.maybe_join(tensor, tensor->node()->inputs().at(tensor->offset() + 2));
            return true;

        /* Conditionals */
        case prim::If:
            groups.maybe_join(tensor, tensor->node()->blocks().at(0)->outputs().at(tensor->offset()));
            groups.maybe_join(tensor, tensor->node()->blocks().at(1)->outputs().at(tensor->offset()));
            return true;

        /* Returns */
        case prim::Return:
            if (tensor->node()->owningBlock()->owningNode() != nullptr) {
                const Node* owning_node = tensor->node()->owningBlock()->owningNode();
                if (owning_node->kind() == c10::prim::If) {
                    groups.maybe_join(tensor, owning_node->output(tensor->offset()));
                } else if (owning_node->kind() == c10::prim::Loop) {
                    groups.maybe_join(tensor, owning_node->blocks().at(0)->inputs().at(tensor->offset()));
                    groups.maybe_join(tensor, owning_node->input(tensor->offset() + 1));
                    groups.maybe_join(tensor, owning_node->output(tensor->offset() - 1));
                }
            }
            return true;

        default:
            return false;
    }
}

}  // namespace inference::quantization::observer_utils
