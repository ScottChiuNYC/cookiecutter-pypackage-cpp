cmake --preset=vcpkg
@REM cmake --build build --config Release
@REM .\build\tests\cpp\Release\{{ cookiecutter.module_name }}_core_test.exe
cmake --build build --config Debug
.\build\tests\cpp\Debug\{{ cookiecutter.module_name }}_core_test.exe