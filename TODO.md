# TODO

- [ ] **Package the generated C++ library as an installable vcpkg port.** Add CMake install/export targets and package configuration, vcpkg port metadata (`vcpkg.json`) and `portfile.cmake`, plus a downstream consumer test that installs the port and uses `find_package()` / `target_link_libraries()`. This is distinct from using vcpkg to consume dependencies. For the Python/C++ template, retain wheel/pybind11 packaging alongside the C++ package. Defer implementation until an actual project (such as the PDE solver) needs it; do not expand the current migration scope.
