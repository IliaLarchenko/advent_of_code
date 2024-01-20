#include <fstream>
#include <iostream>

int main() {
  std::ifstream file("input.txt");
  std::string line;
  std::getline(file, line);
  bool found = false;

  int floor = 0;

  for (int i = 0; i < line.length(); i++) {
    if (line[i] == '(') {
      floor++;
    } else if (line[i] == ')') {
      floor--;
    }
    if (floor == -1 && !found) {
      std::cout << "Part 2 answer:" << std::endl;
      std::cout << i + 1 << std::endl;
      found = true;
    }
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << floor << std::endl;

  return 0;
}
