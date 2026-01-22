import textwrap

msg = textwrap.dedent(
    """
    Project '{{ cookiecutter.project_name }}' generated.

    Next steps (Windows):
      1) poetry build
      2) Test: .\\build\\tests\\cpp\\Release\\{{ cookiecutter.module_name }}_core_test.exe
      3) Install: Run update_package.bat
      4) Python: poetry run python -c "from {{ cookiecutter.module_name }} import Point; p = Point(0, 0); print(p.GetCoordinates())"

    Requirements: 
      - CMake {{ cookiecutter.cmake_min_version }}+
      - Python {{ cookiecutter.python_version }}
      - Poetry
      - vcpkg (configured in vcpkg-configuration.json)
      - MSVC or compatible C++ compiler with C++{{ cookiecutter.cpp_standard }} support
    """
)
print(msg)
