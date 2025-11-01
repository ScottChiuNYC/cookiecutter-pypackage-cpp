cmake_minimum_required(VERSION {{ cookiecutter.cmake_min_version }})
project({{ cookiecutter.project_slug }} LANGUAGES CXX)
set(CMAKE_CXX_STANDARD {{ cookiecutter.cpp_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(pybind11_DIR ".venv/Lib/site-packages/pybind11/share/cmake/pybind11")
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core MODULE 
    src/main.cpp
)
install(TARGETS _core DESTINATION {{ cookiecutter.module_name }})

add_executable(_core_exe    # build an executable to debug; one must specify a main function
    src/main.cpp
)

target_link_libraries(_core_exe PRIVATE pybind11::module)
