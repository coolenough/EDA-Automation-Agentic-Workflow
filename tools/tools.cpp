#include <pybind11/pybind11.h>
#include "kernel.h"

namespace py = pybind11;


int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(tools, m) {
    m.def("add", &add);
}