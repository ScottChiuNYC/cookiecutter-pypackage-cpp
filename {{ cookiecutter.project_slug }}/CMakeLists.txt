cmake_minimum_required(VERSION {{ cookiecutter.cmake_min_version }})
project({{ cookiecutter.module_name }})

include(CTest)
enable_testing()

set(CMAKE_CXX_STANDARD {{ cookiecutter.cpp_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)     # Optional: Force CMake to error if the compiler doesn't support C++{{ cookiecutter.cpp_standard }}
set(CMAKE_CXX_EXTENSIONS OFF)

add_subdirectory(cpp)
add_subdirectory(examples/cpp)
add_subdirectory(tests/cpp)