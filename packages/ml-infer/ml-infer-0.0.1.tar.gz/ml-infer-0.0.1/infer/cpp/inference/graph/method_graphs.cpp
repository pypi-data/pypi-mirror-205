#include "method_graphs.h"

namespace inference::graph::method_graphs {

std::unordered_map<std::string, std::shared_ptr<torch::jit::Graph>> get_method_graphs(const torch::jit::Module &mod,
                                                                                      const config::Config &config) {
    std::unordered_map<std::string, std::shared_ptr<torch::jit::Graph>> graphs;

    // Runs config checks.
    MCHECK(config.exclude_funcs.find(config.export_func) == config.exclude_funcs.end(), "Function being exported [",
           config.export_func, "] is also excluded");

    // Checks that the requested export function
    if (!mod.find_method(config.export_func).has_value()) {
        std::ostringstream ss;
        bool comma_flag = false;
        for (auto &method : mod.get_methods()) {
            if (comma_flag)
                ss << ", ";
            else
                comma_flag = true;
            ss << method.name();
        }
        MERROR("Requested export function [", config.export_func, "] not found in the module. Options are [", ss.str(),
               "]");
    }

    // Checks that all of the config functions are valid.
    for (std::string func_name : config.exclude_funcs)
        MCHECK(mod.find_method(func_name).has_value(),
               "Function name specified in config `exclude_funcs` doesn't exist:", func_name);

    for (torch::jit::Method method : mod.get_methods()) {
        if (config.exclude_funcs.find(method.name()) != config.exclude_funcs.end()) continue;
        graphs.emplace(method.name(), method.graph());
    }

    return graphs;
}

}  // namespace inference::graph::method_graphs
