#include <fstream>
#include <iostream>
#include <string>

std::string next_word(std::string word) {
  if (word.size() == 0) {
    return "a";
  }
  if (word.back() == 'z') {
    return next_word(word.substr(0, word.size() - 1)) + "a";
  }

  if (word.back() == 'i' || word.back() == 'o' || word.back() == 'l') {
    word.back()++;
  }

  word.back()++;
  return word;
}

bool check_three(std::string word) {
  for (int i = 0; i < word.size() - 2; i++) {
    if (word[i + 1] == word[i] + 1 && word[i + 2] == word[i] + 2) {
      return true;
    }
  }
  return false;
}

bool check_doubles(std::string word) {
  int count = 0;
  for (int i = 0; i < word.size() - 1; i++) {
    if (word[i] == word[i + 1]) {
      count++;
      i++;
      if (count >= 2) {
        return true;
      }
    }
  }
  return false;
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  std::string ans1, ans2 = "";

  std::getline(file, line);

  while (ans1 == "" || ans2 == "") {
    line = next_word(line);
    if (check_three(line) && check_doubles(line)) {
      if (ans1 == "") {
        ans1 = line;
      } else {
        ans2 = line;
      }
    }
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
