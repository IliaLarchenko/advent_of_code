#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>

std::set<int> getDivisors(int num) {
  std::set<int> divisors;
  for (int i = 1; i <= sqrt(num); i++) {
    if (num % i == 0) {
      divisors.insert(i);
      divisors.insert(num / i);
    }
  }
  return divisors;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, token;
  int ans1, ans2 = 0;
  int num;

  std::getline(file, line);
  std::istringstream iss(line);
  iss >> num;

  for (int i = 1; i < num; i++) {
    int sum1 = 0, sum2 = 0;
    std::set<int> divisors = getDivisors(i);
    for (auto divisor : divisors) {
      sum1 += divisor * 10;
      if (i / divisor <= 50) {
        sum2 += divisor * 11;
      }
    }
    if (sum1 >= num && ans1 == 0) {
      ans1 = i;
    }
    if (sum2 >= num && ans2 == 0) {
      ans2 = i;
    }
    if (ans1 != 0 && ans2 != 0) {
      break;
    }
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
