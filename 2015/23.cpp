#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int run(int a, int b, std::vector<std::string> &input) {
  std::string name, token;
  int i = 0;
  int n = 0;

  while (i >= 0 && i < input.size()) {
    std::istringstream iss(input[i]);
    iss >> token;
    if (token == "hlf") {
      iss >> name;
      if (name == "a") {
        a = a / 2;
      } else {
        b = b / 2;
      }
    } else if (token == "tpl") {
      iss >> name;
      if (name == "a") {
        a = a * 3;
      } else {
        b = b * 3;
      }
    } else if (token == "inc") {
      iss >> name;
      if (name == "a") {
        a++;
      } else {
        b++;
      }
    } else if (token == "jmp") {
      iss >> n;
      i += n;
      continue;
    } else if (token == "jie") {
      iss >> name;
      iss >> n;
      if (name == "a,") {
        if (a % 2 == 0) {
          i += n;
          continue;
        }
      } else {
        if (b % 2 == 0) {
          i += n;
          continue;
        }
      }
    } else if (token == "jio") {
      iss >> name;
      iss >> n;
      if (name == "a,") {
        if (a == 1) {
          i += n;
          continue;
        }
      } else {
        if (b == 1) {
          i += n;
          continue;
        }
      }
    }
    i++;
  }
  return b;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, name, token;
  std::vector<std::string> input;
  int ans1, ans2 = 0;

  while (std::getline(file, line)) {
    input.push_back(line);
  }

  ans1 = run(0, 0, input);

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  ans2 = run(1, 0, input);

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
