from __future__ import annotations

import os
import subprocess
import sys


def _default_presets() -> tuple[str, str]:
    if sys.platform == "win32":
        return "windows-vcpkg", "windows-release"
    return "linux-vcpkg-release", "linux-release"


def build() -> bool:
    """Build the C++ extension module for the active platform."""
    print("Building C++ extension module...")

    configure_preset, build_preset = _default_presets()
    configure_preset = os.environ.get(
        "{{ cookiecutter.module_name.upper() }}_CMAKE_CONFIGURE_PRESET",
        configure_preset,
    )
    build_preset = os.environ.get(
        "{{ cookiecutter.module_name.upper() }}_CMAKE_BUILD_PRESET",
        build_preset,
    )

    if not os.environ.get("VCPKG_ROOT"):
        print(
            "Build failed: VCPKG_ROOT must point to a vcpkg checkout.",
            file=sys.stderr,
        )
        return False

    python_executable = str(sys.executable)

    try:
        subprocess.check_call(
            [
                "cmake",
                "--preset",
                configure_preset,
                f"-DPython_EXECUTABLE:FILEPATH={python_executable}",
                f"-DPython3_EXECUTABLE:FILEPATH={python_executable}",
            ]
        )
        subprocess.check_call(["cmake", "--build", "--preset", build_preset])
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return False

    print("Build completed successfully!")
    return True


if __name__ == "__main__":
    sys.exit(0 if build() else 1)
