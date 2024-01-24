#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int sum_nums(std::string json) {
  int current = 0;
  int sum = 0;
  bool is_neg = false;

  for (int i = 0; i < json.size(); i++) {
    if (json[i] == '-') {
      is_neg = true;
    } else if (json[i] >= '0' && json[i] <= '9') {
      current = current * 10 + (json[i] - '0');
    } else {
      if (is_neg) {
        current = -current;
      }
      sum += current;
      current = 0;
      is_neg = false;
    }
  }

  if (is_neg) {
    current = -current;
  }

  sum += current;

  return sum;
}

int sum_red(std::string json) {
  int sum = 0;
  std::vector<int> open_brackets;
  std::vector<std::pair<int, int>> reds;
  int first_red = -1;

  for (int i = 0; i < json.size(); i++) {
    if (json[i] == '{') {
      open_brackets.push_back(i);
    } else if (json[i] == '}') {
      if (first_red == open_brackets.size()) {
        reds.push_back(std::make_pair(open_brackets.back(), i));
        first_red = -1;
      }
      open_brackets.pop_back();
    } else if (i + 4 < json.size() && json[i] == ':' && json[i + 1] == '\"' &&
               json[i + 2] == 'r' && json[i + 3] == 'e' && json[i + 4] == 'd') {
      if (first_red == -1) {
        first_red = open_brackets.size();
      }
    }
  }

  int left, right;
  for (int i = reds.size() - 1; i >= 0; i--) {
    left = reds[i].first;
    right = reds[i].second;
    sum += sum_nums(json.substr(left, right - left + 1));
    while (i > 0 && reds[i - 1].first >= left && reds[i - 1].second <= right) {
      i--;
    }
  }

  return sum;
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int ans1, ans2 = 0;

  std::getline(file, line);

  ans1 = sum_nums(line);

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  ans2 = ans1 - sum_red(line);
  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
