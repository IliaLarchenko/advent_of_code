#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

unsigned long long next_number(unsigned long long n) {
  return (n * 252533) % 33554393;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, token;
  unsigned long long n1, n2;
  unsigned long long ans1;

  std::getline(file, line);
  line.replace(0, 80, "");
  line.replace(line.find(","), 1, "");
  line.replace(line.find("."), 1, "");
  std::istringstream iss(line);

  iss >> n1 >> token >> n2;
  ans1 = 20151125;

  for (int i = 0; i < (n1 + n2 - 2) * (n1 + n2 - 1) / 2 + n2 - 1; i++) {
    ans1 = next_number(ans1);
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  file.close();
  return 0;
}
