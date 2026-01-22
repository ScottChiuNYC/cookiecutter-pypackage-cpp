#include "{{ cookiecutter.module_name }}_core/point.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE({{ cookiecutter.module_name }}_core, m) {
  // m.doc() = "pybind11 hello module";

  // m.def("hello_from_bin", &hello_from_bin, R"pbdoc(
  //     A function that returns a Hello string.
  // )pbdoc");

  py::class_<Point>(m, "Point")
    .def(py::init<const double&, const double&>())
    .def("Step",            &Point::Step)
    .def("GetCoordinates",  &Point::GetCoordinates)
    .def("GetPursuitCurve", &Point::GetPursuitCurve)
    .def("SetTarget",       &Point::SetTarget)
    .def("SetStepSize",     &Point::SetStepSize);
}