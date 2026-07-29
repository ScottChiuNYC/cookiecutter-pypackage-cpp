# {{ cookiecutter.module_name }}

Poetry + pybind11 + CMake + vcpkg + GoogleTest + pytest.

## Requirements

- Python {{ cookiecutter.python_version }}
- CMake {{ cookiecutter.cmake_min_version }}+
- Poetry
- a vcpkg checkout referenced by `VCPKG_ROOT`
- Visual Studio 2022 on Windows, or Ninja plus a C++{{ cookiecutter.cpp_standard }} compiler on Linux

## vcpkg registries

`vcpkg-configuration.json` keeps Microsoft vcpkg as the default registry for general dependencies. The `gtest` package is explicitly routed to the public `ScottChiuNYC/vcpkg-registry` baseline pinned by this project.

The custom GoogleTest port preserves the standard `GTest::*` CMake targets but skips the pkg-config executable check, preventing vcpkg from downloading or executing `pkgconf`. When the custom port is updated, change the custom registry baseline only after the new registry commit has passed its Windows/Linux validation.

## Windows

```powershell
cmake --preset windows-vcpkg
cmake --build --preset windows-release
ctest --preset windows-release-tests
$env:PYTHONPATH = "$PWD/src"
poetry run pytest tests/python
```

For a Debug developer build, `cnb.bat` configures, builds, and runs CTest.

## Linux

```bash
cmake --preset linux-vcpkg-release
cmake --build --preset linux-release
ctest --preset linux-release-tests
PYTHONPATH="$PWD/src" poetry run pytest tests/python
```

The pybind extension is emitted directly into `src/{{ cookiecutter.module_name }}` on both platforms, so Python tests import the freshly built native module without generator-specific copy logic.

## Continuous integration

`.github/workflows/build-and-test.yml` runs the Release build, CTest, and pytest on Windows and Linux whenever implementation, dependency, build-system, or test files change. It reads the Microsoft vcpkg checkout commit directly from `vcpkg-configuration.json` and verifies after configure that `pkgconf` was neither installed nor acquired.
