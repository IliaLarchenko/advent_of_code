#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
  std::ifstream file("input.txt");
  std::string line, name;
  int ans1, ans2 = 0;
  int num;
  int sum = 0;
  std::vector<int> nums;
  int i = 0;

  i = 0;
  while (std::getline(file, line)) {
    std::istringstream iss(line);
    iss >> num;
    nums.push_back(num);
    i++;
  }

  int bitmap = 0;
  int min_fit = 1000;
  while (bitmap < (1 << nums.size())) {
    sum = 0;
    for (i = 0; i < nums.size(); i++) {
      if (bitmap >> i & 1) {
        sum += nums[i];
      }
    }
    if (sum == 150) {
      ans1++;
    }

    if (sum == 150 && __builtin_popcount(bitmap) < min_fit) {
      min_fit = __builtin_popcount(bitmap);
      ans2 = 1;
    } else if (sum == 150 && __builtin_popcount(bitmap) == min_fit) {
      ans2++;
    }

    bitmap++;
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
