import textwrap

msg = textwrap.dedent(
    f"""
    Project '{{{{ cookiecutter.project_name }}}}' generated.

    Next steps (Windows):
      1) uv venv
      2) uv sync
      3) uv build
      4) cmake -S . -B build
      5) cmake --build build
      6) .venv\\Scripts\\activate && python -c "from {{{{ cookiecutter.module_name }}}} import hello; hello()"

    Requirements: CMake, Python {{{{ cookiecutter.python_version }}}}, uv.
    """
)
print(msg)
