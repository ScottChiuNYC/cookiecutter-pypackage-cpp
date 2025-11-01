{{ cookiecutter.project_name }}

CMake + pybind11 + uv (packaged via scikit-build-core)

## How To Run

* Run `build.bat` to build both executable and pybind
    * This requires [CMake](https://cmake.org/download/), Python {{ cookiecutter.python_version }}, [uv](https://docs.astral.sh/uv/) and a compiler toolchain for C++ installed in your system
* Run `.venv\Scripts\activate` to activate the venv
* Run `python -c "from {{ cookiecutter.module_name }} import hello; hello()"` to confirm the pybind is installed successfully

## Notes

* This project was generated from a Cookiecutter template, originally modified from the skeleton obtained by running `uv init dcc --lib --build-backend=scikit` 
* The `_core` module is built with pybind11 and installed under `{{ cookiecutter.module_name }}`
* Currently `uv.lock` is gitignored
* Comment out the below in `CMakeLists.txt` if not building pybind
```cmake
pybind11_add_module(_core MODULE src/main.cpp)
install(TARGETS _core DESTINATION dcc)
```
* Run `git clean -ffdx -e .venv` to wipe out everything except the venv
