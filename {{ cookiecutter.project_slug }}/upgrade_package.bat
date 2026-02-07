poetry install
poetry run pytest
poetry run python -c "from {{ cookiecutter.module_name }} import hello; print(hello())"