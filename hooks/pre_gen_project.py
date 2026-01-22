import re
import sys

MODULE = "{{ cookiecutter.module_name }}"

if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", MODULE):
    print(f"ERROR: module_name '{MODULE}' is not a valid Python identifier.")
    sys.exit(1)
