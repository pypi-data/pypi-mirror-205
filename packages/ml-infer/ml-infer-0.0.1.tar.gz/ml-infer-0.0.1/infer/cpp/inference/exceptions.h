#pragma once

#include <pybind11/pybind11.h>
#include <torch/extension.h>

#include "utils.h"

using namespace torch::jit;

namespace inference::exceptions {

// Maximum number of errors to show at a time, if there are multiple errors.
static const size_t MAX_ERRORS = 25;

class NodeException : public c10::Error {
    const char *file;
    uint32_t line;
    const char *func;
    const char *info;

   public:
    NodeException(const char *msg, const char *file_, uint32_t line_, const char *func_, const char *info_ = "")
        : c10::Error(file_, line_, "", msg, ""), file(file_), line(line_), func(func_), info(info_) {}

    const char *get_file() const { return file; }
    uint32_t get_line() const { return line; }
    const char *get_func() const { return func; }
    const char *get_info() const { return info; }
};

// General-purpose exceptions.
template <typename... Args>
[[noreturn]] void throw_error(const char *file, int line, const char *func, Args &&...args) {
    std::stringstream ss;
    size_t i = 0;
    (
        [&](auto &arg) {
            if (i++ != 0) ss << " ";
            ss << arg;
        }(args),
        ...);
    throw NodeException(ss.str().c_str(), file, line, func);
}
#define MERROR(...) inference::exceptions::throw_error(__FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
#define MCHECK(stmt, ...) \
    if (!(stmt)) inference::exceptions::throw_error(__FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)

// Exceptions for a specific node.
template <typename... Args>
[[noreturn]] void throw_node_error(const Node *node, const char *file, int line, const char *func, Args &&...args) {
    std::stringstream ss;
    ss << inference::utils::to_string(node);
    ([&](auto &arg) { ss << arg; }(args), ...);
    throw NodeException(ss.str().c_str(), file, line, func);
}
#define NODE_ERROR(node, ...) \
    inference::exceptions::throw_node_error(node, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
#define NODE_CHECK(stmt, node, ...) \
    if (!(stmt)) inference::exceptions::throw_node_error(node, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)

// Exceptions for a specific value.
template <typename... Args>
[[noreturn]] void throw_value_error(const Value *value, const char *file, int line, const char *func, Args &&...args) {
    std::stringstream ss;
    ss << inference::utils::to_string(value, /* with_node */ true);
    ([&](auto &arg) { ss << arg; }(args), ...);
    throw NodeException(ss.str().c_str(), file, line, func);
}
#define VALUE_ERROR(node, ...) \
    inference::exceptions::throw_value_error(node, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
#define VALUE_CHECK(stmt, node, ...) \
    if (!(stmt)) inference::exceptions::throw_value_error(node, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)

// Throw an exception if a vector of values is non-empty.
template <typename... Args>
void throw_if_more_than(std::vector<NodeException> errs, size_t max_errs, const char *file, int line, const char *func,
                        Args &&...args) {
    if (errs.size() <= max_errs) return;
    std::stringstream ss;
    for (size_t i = 0; i < std::min(errs.size(), inference::exceptions::MAX_ERRORS); i++)
        ss << "Exception " << (i + 1) << ": " << errs[i].what() << "\n\n";
    ss << errs.size() << " total exception(s)\n\n";
    ([&](auto &arg) { ss << arg; }(args), ...);
    throw NodeException(ss.str().c_str(), file, line, func);
}
#define EMPTY_CHECK(errors, ...) \
    inference::exceptions::throw_if_more_than(errors, 0, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__)
#define EMPTY_CHECK_INTERMEDIATE(errors, ...)                                                                \
    inference::exceptions::throw_if_more_than(errors, inference::exceptions::MAX_ERRORS, __FILE__, __LINE__, \
                                              __FUNCTION__, __VA_ARGS__)
#define FEWER_THAN_CHECK(errors, max, ...) \
    inference::exceptions::throw_if_more_than(errors, max, __FILE__, __LINE__, __FUNCTION__, __VA_ARGS__);

void add_module(pybind11::module &m);

}  // namespace inference::exceptions
