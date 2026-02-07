#include "{{ cookiecutter.module_name }}_core/hello.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE({{ cookiecutter.module_name }}_core, m) {
  m.doc() = "pybind11 hello world module";

  m.def("hello", &hello, R"pbdoc(
      A function that returns a Hello World string.
  )pbdoc");
}