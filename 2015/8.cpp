#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int ans1, ans2 = 0;
  int len_code, len_mem, len_code_adj = 0;

  while (std::getline(file, line)) {
    len_code += line.length();
    len_code_adj += 4;
    len_mem -= 2;

    for (int i = 0; i < line.length(); i++) {
      if (line[i] == '\\') {
        if (line[i + 1] == '\\' || line[i + 1] == '\"') {
          len_mem++;
          i++;
          len_code_adj += 2;
        } else if (line[i + 1] == 'x') {
          len_mem++;
          i += 3;
          len_code_adj += 1;
        }
      } else {
        len_mem++;
      }
    }
  }

  std::cout << len_code << std::endl;
  std::cout << len_mem << std::endl;

  ans1 = len_code - len_mem;

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  ans2 = len_code + len_code_adj - len_code;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
