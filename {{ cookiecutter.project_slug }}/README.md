# {{ cookiecutter.module_name }}

Poetry + pybind11 + CMake + vcpkg + GoogleTest + pytest.

## Development contract

Before adding implementation, dependencies, bindings, tests, or build-system changes, read [`docs/development/PROJECT_SKELETON_CONTRACT.md`](docs/development/PROJECT_SKELETON_CONTRACT.md). It is the normative guide to this project's C++/Python source layout, dependency wiring, packaging, build, test, and CI extension points.

Domain implementation documents should describe what to implement; the Project Skeleton Contract describes how that implementation fits into this repository.

## Requirements

- Python {{ cookiecutter.python_version }}
- CMake {{ cookiecutter.cmake_min_version }}+
- Poetry
- a vcpkg checkout referenced by `VCPKG_ROOT`
- Visual Studio 2022 on Windows, or Ninja plus a C++{{ cookiecutter.cpp_standard }} compiler on Linux

## vcpkg dependencies

`vcpkg-configuration.json` keeps Microsoft vcpkg as the only package registry and declares the repository-local `vcpkg-ports` directory as an overlay. The `gtest` dependency is resolved from `vcpkg-ports/gtest` before registry lookup; all other ports continue to come from Microsoft vcpkg.

The local GoogleTest port preserves the standard `GTest::*` CMake targets but skips the pkg-config executable check, preventing vcpkg from downloading or executing `pkgconf`. No personal vcpkg registry is required. When this recipe is updated, change the files under `vcpkg-ports/gtest` and validate the project on Windows and Linux.

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

The pybind extension is emitted directly into `src/{{ cookiecutter.module_name }}` on both platforms, so Python tests import the freshly built native module without generator-specific copy logic. pybind11 remains managed by the existing CMake `FetchContent` configuration.

## Continuous integration

`.github/workflows/build-and-test.yml` runs the Release build, CTest, and pytest on Windows and Linux whenever implementation, dependency, build-system, overlay-port, or test files change. It reads the Microsoft vcpkg checkout commit directly from `vcpkg-configuration.json` and verifies after configure that `pkgconf` was neither installed nor acquired.
