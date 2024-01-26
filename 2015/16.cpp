#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>

bool check(std::string name, int num, std::map<std::string, int> facts) {
  if (name == "cats:" || name == "trees:") {
    return num > facts[name];
  } else if (name == "pomeranians:" || name == "goldfish:") {
    return num < facts[name];
  } else {
    return num == facts[name];
  }
}

int main() {
  std::ifstream file("input.txt");
  std::string line, token, name1, name2, name3;
  int num1, num2, num3;
  int ans1, ans2 = 0;
  int i = 0;
  std::map<std::string, int> facts;

  facts["children:"] = 3;
  facts["cats:"] = 7;
  facts["samoyeds:"] = 2;
  facts["pomeranians:"] = 3;
  facts["akitas:"] = 0;
  facts["vizslas:"] = 0;
  facts["goldfish:"] = 5;
  facts["trees:"] = 3;
  facts["cars:"] = 2;
  facts["perfumes:"] = 1;

  while (std::getline(file, line)) {
    for (int j = 0; j < 2; j++) {
      line.replace(line.find(","), 1, "");
    }
    std::istringstream iss(line);
    iss >> token >> token >> name1 >> num1 >> name2 >> num2 >> name3 >> num3;
    i++;

    if (facts[name1] == num1 && facts[name2] == num2 && facts[name3] == num3) {
      ans1 = i;
    }

    if (check(name1, num1, facts) && check(name2, num2, facts) &&
        check(name3, num3, facts)) {
      ans2 = i;
    }
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
