#pragma once

#include <pybind11/pybind11.h>

#include "utils.h"

template <typename... Args>
void SLOG(Args&&... args) {
    size_t i = 0;
    (
        [&](auto& arg) {
            if (i++ != 0) std::cout << " ";
            std::cout << arg;
        }(args),
        ...);
    std::cout << "\n";
}

#define NODE_LOG(node, ...) SLOG("LOG: ", utils::to_string(node), __VA_ARGS__)
#define VALUE_LOG(value, ...) SLOG("LOG: ", utils::to_string(value), __VA_ARGS__)

#define OBSERVER_NAME "_observer"
