cmake_minimum_required(VERSION {{ cookiecutter.cmake_min_version }})
project({{ cookiecutter.module_name }}_core_test)

find_package(GTest CONFIG REQUIRED)

# Add all .cpp files in this directory as test sources
file(GLOB TEST_SOURCES *.cpp)
add_executable({{ cookiecutter.module_name }}_core_test ${TEST_SOURCES})

target_include_directories({{ cookiecutter.module_name }}_core_test PRIVATE
    ${CMAKE_SOURCE_DIR}/cpp/include
)

target_link_libraries({{ cookiecutter.module_name }}_core_test PRIVATE
    {{ cookiecutter.module_name }}_core_static
    GTest::gtest
    GTest::gtest_main
    # GTest::gmock 
    # GTest::gmock_main
)

add_test(NAME {{ cookiecutter.module_name }}_core_test COMMAND {{ cookiecutter.module_name }}_core_test)