from {{ cookiecutter.module_name }}._core import hello_from_bin


def hello() -> str:
    print(hello_from_bin())
