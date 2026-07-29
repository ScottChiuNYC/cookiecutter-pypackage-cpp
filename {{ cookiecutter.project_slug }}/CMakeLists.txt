cmake_minimum_required(VERSION {{ cookiecutter.cmake_min_version }})
project({{ cookiecutter.module_name }} LANGUAGES CXX)

include(CTest)

set(CMAKE_CXX_STANDARD {{ cookiecutter.cpp_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_subdirectory(cpp)
add_subdirectory(examples/cpp)

if(BUILD_TESTING)
    add_subdirectory(tests/cpp)
endif()
