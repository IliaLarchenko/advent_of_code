#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

std::string look_ans_say(std::string input) {
  std::string output;
  int count;
  char n;
  count = 0;
  n = ' ';

  for (int i = 0; i < input.size(); i++) {
    if (input[i] == n) {
      count++;
    } else {
      if (count > 0) {
        output += std::to_string(count);
        output += n;
      }
      n = input[i];
      count = 1;
    }
  }

  if (count > 0) {
    output += std::to_string(count);
    output += n;
  }

  return output;
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int ans1, ans2 = 0;

  std::getline(file, line);

  for (int i = 0; i < 40; i++) {
    line = look_ans_say(line);
  }

  ans1 = line.size();
  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  for (int i = 0; i < 10; i++) {
    line = look_ans_say(line);
  }

  ans2 = line.size();

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
