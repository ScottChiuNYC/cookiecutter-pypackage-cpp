# Cookiecutter PyPackage With C++ Component

A cross-platform project template combining Poetry, pybind11, CMake, vcpkg, GoogleTest, and pytest.

Generated projects include:

- a C++17 static core library by default;
- a pybind11 Python extension;
- Poetry packaging and Python tests;
- vcpkg manifest dependencies and a repository-local GoogleTest overlay port;
- CMake configure, build, and test presets for Windows and Linux;
- a Windows/Linux GitHub Actions build-and-test matrix.

## Usage

```bash
pip install cookiecutter
cookiecutter gh:scottchiunyc/cookiecutter-pypackage-cpp
```

Or with `uv`:

```bash
uvx cookiecutter gh:scottchiunyc/cookiecutter-pypackage-cpp
```

## Toolchain

The default generated project requires:

- Python 3.12 or later;
- CMake 3.23 or later;
- Poetry;
- a vcpkg checkout referenced by `VCPKG_ROOT`;
- Visual Studio 2022 on Windows;
- Ninja and a C++17 compiler on Linux.

The generated `vcpkg-configuration.json` uses Microsoft vcpkg as the only package registry and declares `vcpkg-ports` as a local overlay. The generated `vcpkg-ports/gtest` directory contains `gtest@1.17.0#3`, preserving the normal CMake targets while using `vcpkg_fixup_pkgconfig(SKIP_CHECK)` so vcpkg does not download or execute `pkgconf`.

The overlay is resolved before registry lookup. Other dependencies continue to come from the pinned Microsoft vcpkg baseline. No personal registry URL is present in generated projects.

## Generated build commands

### Windows

```powershell
cmake --preset windows-vcpkg
cmake --build --preset windows-release
ctest --preset windows-release-tests
$env:PYTHONPATH = "$PWD/src"
poetry run pytest tests/python
```

### Linux

```bash
cmake --preset linux-vcpkg-release
cmake --build --preset linux-release
ctest --preset linux-release-tests
PYTHONPATH="$PWD/src" poetry run pytest tests/python
```

The pybind extension is written directly into the generated Python package directory on both platforms. The Poetry build hook selects the appropriate platform presets and no longer depends on Visual Studio-specific output paths.

## Template acceptance testing

`.github/workflows/template-acceptance.yml` generates a fresh sample project from the current cookiecutter on both Windows and Linux, then:

1. verifies that the generated GitHub Actions workflow was rendered correctly;
2. verifies the local `vcpkg-ports/gtest` overlay and confirms that no personal registry is configured;
3. checks out the Microsoft vcpkg baseline from the generated configuration;
4. configures the generated project and confirms that `pkgconf` was neither installed nor acquired;
5. builds the C++ core and pybind module;
6. runs CTest and pytest.

This protects the template itself, rather than only testing one previously generated repository.

## Notes

- pybind11 remains fetched from its GitHub repository through CMake `FetchContent`;
- generated Windows helpers and VS Code files target the `windows-vcpkg` preset layout;
- generated CI is path-filtered so documentation-only pull requests do not consume the Windows/Linux matrix;
- when the Microsoft vcpkg baseline changes, update `default-registry.baseline` in the template's `vcpkg-configuration.json`;
- when the custom gtest recipe changes, update `vcpkg-ports/gtest` in this template and rerun the Windows/Linux acceptance workflow.
