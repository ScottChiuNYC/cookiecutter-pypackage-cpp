"""Install the development tools; also shared by validation and native builds."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv


def run(command, *, cwd=None, env=None):
    command = [str(part) for part in command]
    print("+ " + subprocess.list2cmdline(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def python_in(directory):
    return Path(directory) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def tool_environment(project, tools=None):
    project = Path(project).resolve()
    tools = Path(tools or os.environ.get("PROJECT_DEV_TOOLS", project / ".dev-tools")).resolve()
    env = os.environ.copy()
    tool_python = python_in(tools / "venv")
    if tool_python.exists():
        env["PATH"] = str(tool_python.parent) + os.pathsep + env["PATH"]
    else:
        tool_python = Path(sys.executable)
    env["PROJECT_DEV_TOOLS"] = str(tools)
    selected = tools / "vcpkg-root.txt"
    default_root = selected.read_text(encoding="utf-8") if selected.exists() else str(tools / "vcpkg")
    env["VCPKG_ROOT"] = env.get("VCPKG_ROOT", default_root)
    env["VCPKG_DISABLE_METRICS"] = "1"
    env["VCPKG_MAX_CONCURRENCY"] = env.get("VCPKG_MAX_CONCURRENCY", "2")
    env["CMAKE_BUILD_PARALLEL_LEVEL"] = env.get("CMAKE_BUILD_PARALLEL_LEVEL", "2")
    env["POETRY_NO_INTERACTION"] = "1"
    ninja = shutil.which("ninja", path=env["PATH"])
    if not ninja or not Path(env["VCPKG_ROOT"], "scripts/buildsystems/vcpkg.cmake").is_file():
        raise SystemExit("Run python scripts/bootstrap.py first (Ninja and pinned vcpkg are required).")
    options = []
    if sys.platform == "linux":
        # Only tool paths change; keep the official x64-linux ABI settings and
        # compiler tracking. Parent -D options alone do not reach vcpkg's CMake.
        triplets = tools / "triplets"
        triplets.mkdir(parents=True, exist_ok=True)
        executable = Path(ninja).resolve().as_posix()
        env["NINJA"] = executable
        env["VCPKG_KEEP_ENV_VARS"] = env.get("VCPKG_KEEP_ENV_VARS", "") + ";NINJA"
        (triplets / "x64-linux.cmake").write_text(
            'include("$ENV{VCPKG_ROOT}/triplets/x64-linux.cmake")\n'
            'set(NINJA "$ENV{NINJA}")\n'
            'list(APPEND VCPKG_CMAKE_CONFIGURE_OPTIONS "-DCMAKE_MAKE_PROGRAM:FILEPATH=${NINJA}")\n',
            encoding="utf-8",
        )
        options = [f"-DCMAKE_MAKE_PROGRAM:FILEPATH={executable}", f"-DVCPKG_OVERLAY_TRIPLETS:STRING={triplets.as_posix()}"]
    elif sys.platform != "win32":
        raise SystemExit("Supported presets are Linux x64 and Windows x64 with Visual Studio 2022.")
    return tool_python, env, options


def main(project=None, tools=None):
    project = Path(project or Path(__file__).resolve().parents[1])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tools-dir", type=Path, default=tools or project / ".dev-tools")
    parser.add_argument("--vcpkg-root", type=Path, help="Reuse a checkout already at the declared baseline; it will not be changed.")
    args = parser.parse_args()
    if sys.version_info < (3, 12) or not shutil.which("git"):
        raise SystemExit("Prerequisites: Python 3.12+ and Git; also GCC/Clang on Linux or Visual Studio 2022 C++ tools on Windows.")
    tools = args.tools_dir.resolve()
    tools.mkdir(parents=True, exist_ok=True)
    py = python_in(tools / "venv")
    if not py.exists():
        venv.EnvBuilder(with_pip=True).create(tools / "venv")
    run([py, "-m", "pip", "install", "-r", project / "scripts/tool-requirements.txt"])
    config = json.loads((project / "vcpkg-configuration.json").read_text(encoding="utf-8"))["default-registry"]
    vcpkg = (args.vcpkg_root or tools / "vcpkg").resolve()
    if not (vcpkg / ".git").exists():
        if args.vcpkg_root:
            raise SystemExit("--vcpkg-root must be an existing checkout at the declared baseline.")
        run(["git", "clone", "--filter=blob:none", "--no-checkout", config["repository"], vcpkg])
        run(["git", "checkout", "--detach", config["baseline"]], cwd=vcpkg)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=vcpkg, text=True).strip()
    if head != config["baseline"]:
        raise SystemExit(f"vcpkg is at {head}; required baseline is {config['baseline']}. Use a fresh --tools-dir or the matching --vcpkg-root.")
    # Persist only the selected local checkout path; no shell activation needed.
    (tools / "vcpkg-root.txt").write_text(str(vcpkg), encoding="utf-8")
    os.environ["VCPKG_ROOT"] = str(vcpkg)
    _, env, _ = tool_environment(project, tools)
    binary = vcpkg / ("vcpkg.exe" if os.name == "nt" else "vcpkg")
    if not binary.exists():
        script = vcpkg / ("bootstrap-vcpkg.bat" if os.name == "nt" else "bootstrap-vcpkg.sh")
        run(["cmd", "/c", script, "-disableMetrics"] if os.name == "nt" else [script, "-disableMetrics"], env=env)
    run([binary, "version"], env=env)
    print("Bootstrap complete. Run the documented validation command; no activation or manual path overrides are required.")


if __name__ == "__main__":
    main()
