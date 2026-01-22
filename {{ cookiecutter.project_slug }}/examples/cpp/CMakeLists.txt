add_executable(demo demo.cpp)

target_link_libraries(demo PRIVATE {{ cookiecutter.module_name }}_core_static)
