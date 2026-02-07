poetry install
poetry run python -c "from {{ cookiecutter.module_name }} import hello; print(hello())"