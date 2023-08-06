#include "exceptions.h"

namespace inference::exceptions {

void add_module(pybind11::module &m) {
    pybind11::register_exception<NodeException>(m, "NodeException", PyExc_RuntimeError);
}

}  // namespace inference::exceptions
