#include "preprocess.h"

#include "exceptions.h"
#include "graph/method_graphs.h"
#include "macros.h"
#include "passes/passes.h"
#include "quantization/quantization.h"

#define EXPORT_ONCE_NAME "__export_once__"

namespace inference::preprocess {

struct QuantizeProps {
    bool export_once = false;
};

QuantizeProps parse_quantize_props(Module &mod) {
    QuantizeProps props_obj;

    if (mod.hasattr(EXPORT_ONCE_NAME)) props_obj.export_once = mod.attr(EXPORT_ONCE_NAME).toBool();

    return props_obj;
}

Module insert_all_observers(Module &mod, const config::Config &config, bool copy) {
    if (copy) mod = mod.clone();

    for (auto [name, attribute] : mod.named_attributes(/* recurse */ false)) {
        // Gets the submodule, if the attribute is a module.
        if (!attribute.isModule()) continue;
        auto submod = attribute.toModule();

        // Parses the quantization properties from the dictionary.
        auto quantize_props = parse_quantize_props(submod);

        // If the submodule is `shared`, recursively update it.
        if (quantize_props.export_once) {
            auto new_submod = insert_all_observers(submod, config, /* copy */ false);
            auto new_submod_ivalue = c10::IValue(new_submod._ivalue());
            mod.setattr(name, new_submod_ivalue);
        }
    }

    // Applies passes and inserts observers.
    mod = passes::apply_all_passes(mod, config, /* copy */ false);
    mod = quantization::insert_observers(mod, config, /* copy */ false);

    return mod;
}

void add_module(pybind11::module &m) {
    m.def("insert_all_observers", &insert_all_observers, "mod"_a, "config"_a, "copy"_a);
    m.def("quantize_props", []() -> std::vector<std::string> { return {EXPORT_ONCE_NAME}; });
}

}  // namespace inference::preprocess
