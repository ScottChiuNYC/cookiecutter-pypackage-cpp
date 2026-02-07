@echo off
setlocal

set "PYEXE="
if defined VIRTUAL_ENV (
	set "PYEXE=%VIRTUAL_ENV%\Scripts\python.exe"
)

if not defined PYEXE (
	for /f "delims=" %%P in ('where python') do (
		set "PYEXE=%%P"
		goto :found_python
	)
)

:found_python
if defined PYEXE (
	cmake --preset=vcpkg -DPython_EXECUTABLE="%PYEXE%" -DPython3_EXECUTABLE="%PYEXE%"
) else (
	cmake --preset=vcpkg
)

cmake --preset=vcpkg
@REM cmake --build build --config Release
@REM .\build\tests\cpp\Release\{{ cookiecutter.module_name }}_core_test.exe
cmake --build build --config Debug
.\build\tests\cpp\Debug\{{ cookiecutter.module_name }}_core_test.exe