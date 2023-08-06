#include "utils.h"

namespace inference::utils {

std::string to_string(const Block *block) {
    std::stringstream ss;
    ss << "Block for node of type " << block->owningNode()->kind().toDisplayString() << " with "
       << block->inputs().size() << " input(s) and " << block->outputs().size() << " output(s)\n";

    // Renders input and output values.
    for (const Value *input : block->inputs()) ss << "  -> " << to_string(input, false) << "\n";
    for (const Value *output : block->outputs()) ss << "  <- " << to_string(output, false) << "\n";

    return ss.str();
}

std::string get_source_loc(const Node *node, bool msg_if_missing = false) {
    std::stringstream ss;

    // Renders the source range, if available.
    if (auto flc = node->sourceRange().file_line_col()) {
        const std::string &file = std::get<0>(flc.value());
        const int line = std::get<1>(flc.value()), col = std::get<2>(flc.value());
        ss << file << ":" << line << ":" << col;
    } else if (msg_if_missing) {
        ss << "(Couldn't find source range)";
    }

    return ss.str();
}

std::string to_string(const Node *node) {
    std::stringstream ss;
    ss << node->kind().toDisplayString() << " with " << node->inputs().size() << " input(s) and "
       << node->outputs().size() << " output(s)\n";
    ss << "  " << get_source_loc(node, /* msg_if_missing */ true) << "\n";

    // Renders input and output values.
    for (const Value *input : node->inputs())
        ss << "  -> " << to_string(input, false) << " " << get_source_loc(input->node()) << "\n";
    for (const Value *output : node->outputs())
        ss << "  <- " << to_string(output, false) << " " << get_source_loc(output->node()) << "\n";

    for (const Block *block : node->blocks()) {
        ss << "\n" << to_string(block);
    }

    return ss.str();
}

std::string to_string(const Value *value, bool with_node) {
    std::stringstream ss;
    ss << value->debugName() << " of type " << value->type()->repr_str();
    if (with_node) ss << "\n\n" << to_string(value->node());
    return ss.str();
}

}  // namespace inference::utils
