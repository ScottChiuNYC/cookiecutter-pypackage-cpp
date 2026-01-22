import subprocess, shutil

subprocess.check_call(['cmake', '--preset=vcpkg'])
subprocess.check_call(['cmake', '--build', 'build', '--config', 'Release'])
shutil.copyfile('./build/cpp/Release/{{ cookiecutter.module_name }}_core.cp312-win_amd64.pyd', './src/{{ cookiecutter.module_name }}/{{ cookiecutter.module_name }}_core.pyd')