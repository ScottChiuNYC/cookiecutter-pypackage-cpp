# Cookiecutter PyPackage With C++ Component

Poetry + pybind11 + CMake + vcpkg + GTest

## Usage

* pip install and call cookiecutter: 
```
pip install cookiecutter
cookiecutter gh:scottchiunyc/cookiecutter-pypackage-cpp
```
* Or, if you already have `uv` installed: 
```
uvx cookiecutter gh:scottchiunyc/cookiecutter-pypackage-cpp
```

## vcpkg + GoogleTest

* [One time initial vcpkg setup](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-cmd)
    * `git clone https://github.com/microsoft/vcpkg.git`
    * `cd vcpkg && bootstrap-vcpkg.bat`
    * `set "VCPKG_ROOT=C:\path\to\vcpkg"`
    * `set PATH=%VCPKG_ROOT%;%PATH%`
    * In project root `vcpkg new --application`
        * In `vcpkg-configuration.json`, the `baseline` in `default-registry` is the HEAD commit of the vcpkg registry at the time running `vcpkg new --application`
    * The `CMakePresets.json` in this guide has `"generator": "Ninja",` which should be replaced by the default generator in the current platform
        * `cmake --help` to check
* To configure cmake and build and run gtest: 
    * Run `cnb` if not using VS Code,
        * Comment out `cmake --preset=vcpkg` to skip repeated config step
        * `cmake --preset=vcpkg` does what `cmake -S . -B build` does which is to configure cmake
        * `cd build & ctest` also runs the test but I like gtest output format more
        * CTest looks for `CTestTestfile.cmake` which is in `build`, as CTest is included and enabled in project root's `CMakeLists.txt`
    * `F5` if using VS Code
        * In `.vscode/launch.json`, use `"preLaunchTask": "CMake: build"` instead of `"preLaunchTask": "CMake: config and build"` to skip repeated config step
    * When to reconfigured: 
        * New cpp/h files added
        * `build` folder deleted, clean rebuild
* `vcpkg add port fmt` to add the `fmt` library to C++ dependencies

## Python Development

* `poetry shell` to create/activate venv for the project
    * This requires `poetry` and `poetry-plugin-shell` pip installed in the system
* `poetry install` to install packages as specified in `pyproject.toml`
* `poetry add numpy` to add `numpy` to Python dependencies
* `poetry build` to build wheel
* Run `update_package.bat` to pip uninstall and pip install the {{ cookiecutter.module_name }} package in the project venv

## Notes

* Currently this project has an examples folder compiled but the executable is not run by `cnb.bat` nor `.vscode/launch.json`
* AI recommends to keep both examples and (not yet created) docs folders and have docs reference examples so that docs is synced
    * Look into sphinx `literalinclude` and `sphinx-gallery`
    * Examples can be smoked-tested in CI (build and optionally run with a CMake toggle `BUILD_EXAMPLES`) to ensure docs stay accurate
* pybind11 is currently fetched from the pybind11 repo on GitHub. It was added by vcpkg from the registry but the dependencies might fail to download if the user is behind a corporate corporate firewall. The fetch-from-repo trick works well with header-only libraries like pybin11 but for compiled libraries the setup will be more complicated
* TODO: pytest, jupyter notebook demo, sphinx docs
* TODO: Is `.vscode/c_cpp_properties.json` needed in order for IntelliSense to work properly? That's not the case for dlc
* TODO: After poetry upgrade, run `poetry config --migrate` to fix `pyproject.toml` for broken projects