#include "{{ cookiecutter.module_name }}_core/hello.h"
#include <iostream>

int main() {
  std::cout << hello() << std::endl;
  return 0;
}