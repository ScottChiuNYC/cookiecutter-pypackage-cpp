poetry run pip uninstall -y {{ cookiecutter.module_name }}
poetry run pip install ./dist/{{ cookiecutter.module_name }}-{{ cookiecutter.version }}-cp312-cp312-win_amd64.whl
poetry run python -c "from {{ cookiecutter.module_name }} import Point; p = Point(0, 0); print(p.GetCoordinates())"