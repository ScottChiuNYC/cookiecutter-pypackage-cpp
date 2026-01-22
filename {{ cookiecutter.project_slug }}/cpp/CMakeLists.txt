cmake_minimum_required(VERSION {{ cookiecutter.cmake_min_version }})
project({{ cookiecutter.module_name }}_core)

# Add the core library from all .cpp files in src/
file(GLOB CORE_SOURCES src/*.cpp)
add_library({{ cookiecutter.module_name }}_core_static STATIC ${CORE_SOURCES})

# Include directories for the core library
# Add more include directories as needed
target_include_directories({{ cookiecutter.module_name }}_core_static PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# pybind11 CMake integration:

# Easy
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module({{ cookiecutter.module_name }}_core bindings/point_bindings.cpp)
target_link_libraries({{ cookiecutter.module_name }}_core PRIVATE {{ cookiecutter.module_name }}_core_static)

# # Advanced
# find_package(Python COMPONENTS Interpreter Development)
# find_package(pybind11 CONFIG REQUIRED)
# Python_add_library(MyModule2 src2.cpp)
# target_link_libraries(MyModule2 PRIVATE pybind11::headers)