import textwrap

msg = textwrap.dedent(
    """
    Project '{{ cookiecutter.project_name }}' generated.

    Windows:
      1) Set VCPKG_ROOT to a vcpkg checkout.
      2) Configure: cmake --preset windows-vcpkg
      3) Build: cmake --build --preset windows-release
      4) Run C++ tests: ctest --preset windows-release-tests
      5) Run Python tests: poetry run pytest

    Linux:
      1) Set VCPKG_ROOT to a vcpkg checkout and install Ninja.
      2) Configure: cmake --preset linux-vcpkg-release
      3) Build: cmake --build --preset linux-release
      4) Run C++ tests: ctest --preset linux-release-tests
      5) Run Python tests: poetry run pytest

    Requirements:
      - CMake {{ cookiecutter.cmake_min_version }}+
      - Python {{ cookiecutter.python_version }}
      - Poetry
      - vcpkg (configured in vcpkg-configuration.json)
      - Visual Studio 2022 on Windows or a C++{{ cookiecutter.cpp_standard }} compiler plus Ninja on Linux
    """
)
print(msg)
