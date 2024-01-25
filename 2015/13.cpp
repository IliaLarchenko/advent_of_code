#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>

int get_happiness(std::set<std::string> names,
                  std::map<std::pair<std::string, std::string>, int> happiness,
                  std::string first_name, std::string last_name) {
  if (names.size() == 0) {
    return happiness[std::make_pair(first_name, last_name)] +
           happiness[std::make_pair(last_name, first_name)];
  }

  int max_happiness = 0;
  std::set<std::string> new_names = names;

  for (auto name : names) {
    new_names.erase(name);
    int new_happiness = happiness[std::make_pair(name, last_name)] +
                        happiness[std::make_pair(last_name, name)];
    max_happiness = std::max(
        max_happiness,
        get_happiness(new_names, happiness, first_name, name) + new_happiness);
    new_names.insert(name);
  }

  return max_happiness;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, token, direction, name1, name2;
  std::set<std::string> names;
  int gain;
  std::map<std::pair<std::string, std::string>, int> happiness;

  int ans1, ans2 = 0;

  while (std::getline(file, line)) {
    line.pop_back();
    std::istringstream iss(line);

    iss >> name1 >> token >> direction >> gain >> token >> token >> token >>
        token >> token >> token >> name2;

    names.insert(name1);
    names.insert(name2);

    if (direction == "lose") {
      gain = -gain;
    }
    happiness[std::make_pair(name1, name2)] = gain;
  }

  names.erase(name1);
  ans1 = get_happiness(names, happiness, name1, name1);

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  for (auto name : names) {
    happiness[std::make_pair(name, "me")] = 0;
    happiness[std::make_pair("me", name)] = 0;
  }
  names.insert("me");

  ans2 = get_happiness(names, happiness, name1, name1);

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
