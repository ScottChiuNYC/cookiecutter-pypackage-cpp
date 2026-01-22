import textwrap

msg = textwrap.dedent(
    """
    Project '{{ cookiecutter.project_name }}' generated.

    Next steps (Windows):
      1) Build Wheel: poetry build
      2) Run GTest on C++: .\\build\\tests\\cpp\\Release\\{{ cookiecutter.module_name }}_core_test.exe
      3) Install Wheel and Run in Python: update_package.bat

    Requirements: 
      - CMake {{ cookiecutter.cmake_min_version }}+
      - Python {{ cookiecutter.python_version }}
      - Poetry
      - vcpkg (configured in vcpkg-configuration.json)
      - MSVC or compatible C++ compiler with C++{{ cookiecutter.cpp_standard }} support
    """
)
print(msg)
