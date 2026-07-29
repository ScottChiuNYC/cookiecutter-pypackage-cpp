cmake_minimum_required(VERSION {{ cookiecutter.cmake_min_version }})
project({{ cookiecutter.module_name }}_core LANGUAGES CXX)

file(GLOB CORE_SOURCES CONFIGURE_DEPENDS src/*.cpp)
add_library({{ cookiecutter.module_name }}_core_static STATIC ${CORE_SOURCES})
set_target_properties(
    {{ cookiecutter.module_name }}_core_static
    PROPERTIES POSITION_INDEPENDENT_CODE ON
)

target_include_directories(
    {{ cookiecutter.module_name }}_core_static
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
)

include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v3.0.1
)
FetchContent_MakeAvailable(pybind11)

set(PYBIND11_FINDPYTHON ON)
pybind11_add_module({{ cookiecutter.module_name }}_core bindings/hello_bindings.cpp)
target_link_libraries({{ cookiecutter.module_name }}_core PRIVATE {{ cookiecutter.module_name }}_core_static)

# Put the extension directly beside the Python package sources on every
# platform and for every multi-config build configuration. This avoids
# generator-specific copy logic in build.py.
set(PYTHON_PACKAGE_DIR "${CMAKE_SOURCE_DIR}/src/{{ cookiecutter.module_name }}")
set_target_properties(
    {{ cookiecutter.module_name }}_core
    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${PYTHON_PACKAGE_DIR}"
        RUNTIME_OUTPUT_DIRECTORY "${PYTHON_PACKAGE_DIR}"
)

foreach(config Debug Release RelWithDebInfo MinSizeRel)
    string(TOUPPER "${config}" config_upper)
    set_target_properties(
        {{ cookiecutter.module_name }}_core
        PROPERTIES
            LIBRARY_OUTPUT_DIRECTORY_${config_upper} "${PYTHON_PACKAGE_DIR}"
            RUNTIME_OUTPUT_DIRECTORY_${config_upper} "${PYTHON_PACKAGE_DIR}"
    )
endforeach()
