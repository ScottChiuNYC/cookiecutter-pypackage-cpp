poetry run pip uninstall -y {{ cookiecutter.module_name }}
poetry run pip install ./dist/{{ cookiecutter.module_name }}-{{ cookiecutter.version }}-cp312-cp312-win_amd64.whl