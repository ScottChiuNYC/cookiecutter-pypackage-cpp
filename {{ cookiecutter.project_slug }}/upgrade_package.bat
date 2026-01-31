poetry install
poetry run python -c "from {{ cookiecutter.module_name }} import Point; p = Point(0, 0); print(p.GetCoordinates())"