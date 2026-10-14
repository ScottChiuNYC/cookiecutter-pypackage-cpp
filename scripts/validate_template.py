"""Validate Copier copy, tagged update with local edits, and the resulting build."""
from pathlib import Path
import argparse
import json
import os
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "template/scripts"))
from bootstrap import run, tool_environment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, help="Keep generated projects and build results in this empty directory.")
    args = parser.parse_args()
    tools = ROOT / ".dev-tools"
    selected = tools / "vcpkg-root.txt"
    if selected.exists():
        os.environ["VCPKG_ROOT"] = selected.read_text(encoding="utf-8")
    py, env, _ = tool_environment(ROOT / "template", tools)
    if Path(sys.prefix).resolve() != (tools / "venv").resolve():
        run([py, __file__, *sys.argv[1:]], env=env)
        return
    temporary = tempfile.TemporaryDirectory(prefix="template-validation-") if args.work_dir is None else None
    work = Path(temporary.name) if temporary else args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        raise SystemExit("--work-dir must be empty; validation will not overwrite existing projects.")
    copier = [py, "-m", "copier"]
    # Exercise real Git tags without publishing test tags or changing the source repo.
    fixture = work / "template"
    fixture.mkdir()
    for name in ("copier.yml", "template"):
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, fixture / name, ignore=shutil.ignore_patterns(".dev-tools", "__pycache__", "build", "dist"))
        else:
            shutil.copy2(source, fixture / name)
    run(["git", "init"], cwd=fixture)
    for key, value in (("user.name", "Template Validation"), ("user.email", "template@example.com"), ("core.autocrlf", "false")):
        run(["git", "config", key, value], cwd=fixture)
    run(["git", "add", "."], cwd=fixture)
    run(["git", "commit", "-m", "Template v1"], cwd=fixture)
    run(["git", "tag", "v1.0.0"], cwd=fixture)
    default = work / "defaults"
    run([*copier, "copy", "--defaults", "--vcs-ref", "v1.0.0", fixture, default], env=env)
    python_package = (default / "pyproject.toml").exists()
    project = work / "sample"
    data = ["-d", "project_name=CI Sample", "-d", "project_slug=ci_sample"]
    if python_package:
        data += ["-d", "module_name=ci_sample"]
    run([*copier, "copy", "--defaults", "--vcs-ref", "v1.0.0", *data, fixture, project], env=env)
    import yaml
    answers = yaml.safe_load((project / ".copier-answers.yml").read_text(encoding="utf-8"))
    assert answers["_commit"] == "v1.0.0"
    workflow = (project / ".github/workflows/build-and-test.yml").read_text(encoding="utf-8")
    assert "${{ matrix.os }}" in workflow and "{%" not in workflow and "cookiecutter." not in workflow
    config = json.loads((project / "vcpkg-configuration.json").read_text(encoding="utf-8"))
    assert config["default-registry"]["repository"] == "https://github.com/microsoft/vcpkg"
    assert config["overlay-ports"] == ["vcpkg-ports"]
    assert "vcpkg_fixup_pkgconfig(SKIP_CHECK)" in (project / "vcpkg-ports/gtest/portfile.cmake").read_text(encoding="utf-8")
    assert not (project / ".git").exists() and not (project / "copier.yml").exists()
    readme = project / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nLocal project note.\n", encoding="utf-8", newline="\n")
    run(["git", "init"], cwd=project)
    for key, value in (("user.name", "Template Validation"), ("user.email", "template@example.com"), ("core.autocrlf", "false")):
        run(["git", "config", key, value], cwd=project)
    run(["git", "add", "."], cwd=project)
    run(["git", "commit", "-m", "Generated project with local edits"], cwd=project)
    template_readme = next((fixture / "template").glob("README.md*"))
    template_readme.write_text("Template update marker.\n\n" + template_readme.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    (fixture / "template/update-marker.txt.jinja").write_text("Tagged update passed.\n", encoding="utf-8", newline="\n")
    run(["git", "add", "."], cwd=fixture)
    run(["git", "commit", "-m", "Template v2"], cwd=fixture)
    run(["git", "tag", "v1.1.0"], cwd=fixture)
    run([*copier, "update", "--defaults", "--vcs-ref", "v1.1.0"], cwd=project, env=env)
    updated = yaml.safe_load((project / ".copier-answers.yml").read_text(encoding="utf-8"))
    assert updated["_commit"] == "v1.1.0"
    assert "Local project note." in readme.read_text(encoding="utf-8")
    assert "Template update marker." in readme.read_text(encoding="utf-8")
    assert (project / "update-marker.txt").read_text(encoding="utf-8") == "Tagged update passed.\n"
    assert not list(project.rglob("*.rej"))
    # Invalid identifiers must fail at question validation, before writing a project.
    bad = ["-d", "module_name=not-valid"] if python_package else ["-d", "project_slug=not-valid"]
    import subprocess
    result = subprocess.run([str(x) for x in [*copier, "copy", "--defaults", *bad, fixture, work / "invalid"]], env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.returncode != 0 and "Use a valid identifier." in result.stdout, result.stdout
    print(f"Identifier rejection passed (expected exit {result.returncode}).", flush=True)
    run([py, project / "scripts/validate.py", *(["--wheel"] if python_package else [])], env=env)
    print("Template validation passed: defaults, custom answers, tagged update, retained local edits, identifier validation, and actual build/tests.")
    if temporary:
        temporary.cleanup()


if __name__ == "__main__":
    main()
