#include <fstream>
#include <iostream>
#include <string>

bool check_vowels(std::string s) {
  int count = 0;
  for (char c : s) {
    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
      count++;
      if (count == 3) {
        return true;
      }
    }
  }
  return false;
}

bool check_double(std::string s) {
  for (int i = 0; i < s.size() - 1; i++) {
    if (s[i] == s[i + 1]) {
      return true;
    }
  }
  return false;
}

bool check_forbiden(std::string s) {
  for (int i = 0; i < s.size() - 1; i++) {
    std::string two = s.substr(i, 2);
    if ((two == "ab") || (two == "cd") || (two == "pq") || (two == "xy")) {
      return false;
    }
  }
  return true;
}

bool check_two_pairs(std::string s) {
  for (int i = 0; i < s.size() - 1; i++) {
    std::string two = s.substr(i, 2);
    for (int j = i + 2; j < s.size() - 1; j++) {
      if (two == s.substr(j, 2)) {
        return true;
      }
    }
  }
  return false;
}

bool check_three_letters(std::string s) {
  for (int i = 0; i < s.size() - 2; i++) {
    if (s[i] == s[i + 2]) {
      return true;
    }
  }
  return false;
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int ans1 = 0;
  int ans2 = 0;

  while (std::getline(file, line)) {
    if (check_vowels(line) && check_double(line) && check_forbiden(line)) {
      ans1++;
    }
    if (check_two_pairs(line) && check_three_letters(line)) {
      ans2++;
    }
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
