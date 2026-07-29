# Cookiecutter PyPackage With C++ Component

A cross-platform project template combining Poetry, pybind11, CMake, vcpkg, GoogleTest, and pytest.

Generated projects include:

- a C++17 static core library by default;
- a pybind11 Python extension;
- Poetry packaging and Python tests;
- vcpkg manifest dependencies and GoogleTest;
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

The generated `vcpkg-configuration.json` pins the registry baseline. Both generated CI and this template's acceptance CI read that baseline directly before checking out vcpkg.

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
2. checks out the vcpkg baseline from the generated configuration;
3. configures and builds the C++ core and pybind module;
4. runs CTest;
5. runs pytest.

This protects the template itself, rather than only testing one previously generated repository.

## Notes

- pybind11 is fetched from its GitHub repository through CMake `FetchContent`.
- generated Windows helpers and VS Code files target the `windows-vcpkg` preset layout;
- generated CI is path-filtered so documentation-only pull requests do not consume the Windows/Linux matrix;
- when the vcpkg baseline changes, update only `vcpkg-configuration.json`; CI derives the checkout commit from it.
