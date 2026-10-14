# Copier Python Package with C++ Component

Poetry packaging, a C++17 static core and a pybind11 extension. This repository is migrated in place from Cookiecutter; its GitHub name stays the same.

## Generate and update a project

```bash
pip install copier==9.19.1
copier copy gh:ScottChiuNYC/cookiecutter-pypackage-cpp my-project
cd my-project
git init
git add .
git commit -m "Generate project"
# After committing your project changes, update to the latest template revision:
copier update
```

Copier records answers and the template version in `.copier-answers.yml`; commit it. Release versions are Git tags. The template lives under `template/`, so template metadata and its Git history are not copied into generated projects. Existing Cookiecutter-generated projects need deliberate adoption and review before using Copier updates; this migration does not rewrite those projects.

## Fresh Work / Codex / developer setup

Prerequisites: Python 3.12+, Git, and a C++17 compiler. Linux needs GCC or Clang plus curl, zip, unzip and tar. Windows needs Visual Studio 2022 with Desktop development with C++ and a Windows SDK (the `windows-2022` Actions image supplies them). Native compilers are platform prerequisites, not installed by pip.

From a fresh clone, on either Windows or Linux:

```bash
python scripts/bootstrap.py
python scripts/validate_template.py
```

Bootstrap installs the exact tool versions in `template/scripts/tool-requirements.txt` into `.dev-tools/venv`, checks out the vcpkg baseline declared in `template/vcpkg-configuration.json`, and bootstraps it. Validation needs no activation, manual PATH changes, or exported variables. Both platforms supply the installed Ninja path to nested vcpkg processes; Linux also pins the parent configure path. Compiler tracking stays enabled, and Windows retains the Visual Studio preset.

To reuse an already pinned vcpkg checkout:

```bash
python scripts/bootstrap.py --vcpkg-root /absolute/path/to/vcpkg
```

That checkout must already match the declared baseline and is not checked out to another version. Re-running bootstrap reuses installed tools and downloads. Use `--work-dir .validation` on validation to keep generated artifacts; that directory must be empty. The two repositories maintain their own scripts and their independent project architectures.

## Validation and CI

The validation script exercises default/custom Copier copy, real `v1.0.0` → `v1.1.0` updates in an isolated fixture, preservation of local README edits, answer/version persistence, identifier rejection and GitHub expression rendering. It then configures/builds the updated sample and runs its original tests. It also builds an sdist, rebuilds a platform wheel from that sdist, installs the wheel in a clean virtual environment, and imports its native extension outside the source checkout.

`.github/workflows/template-acceptance.yml` runs these same two commands on Linux and Windows. Generated projects include their own bootstrap/validation scripts and a Windows/Linux workflow using those scripts. The vcpkg GoogleTest overlay remains local and validation checks that `pkgconf` was not installed or acquired.

No Docker, services, shell activation, personal vcpkg registry or custom infrastructure is needed. The first run downloads tools and compiles dependencies; later runs reuse local caches. Template acceptance on push allows Windows/Linux checks to finish before opening the migration PR.
