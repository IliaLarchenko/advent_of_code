#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>

int get_distance(int speed, int period, int rest, int time) {
  int cycle = period + rest;
  int cycles = time / cycle;
  int distance = cycles * period * speed;
  int remaining = time - cycles * cycle;

  distance += std::min(remaining, period) * speed;

  return distance;
}

int main() {
  int time = 2503;
  std::ifstream file("input.txt");
  std::string line, token, name;
  int speed, rest, period;
  std::map<std::string, int> speeds, rests, periods, points;
  std::vector<std::string> names;
  int ans1, ans2 = 0;

  while (std::getline(file, line)) {
    std::istringstream iss(line);

    iss >> name >> token >> token >> speed >> token >> token >> period >>
        token >> token >> token >> token >> token >> token >> rest;

    speeds[name] = speed;
    periods[name] = period;
    rests[name] = rest;
    names.push_back(name);
    points[name] = 0;

    ans1 = std::max(ans1, get_distance(speed, period, rest, time));
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::vector<std::string> leaders;
  int max_points = 0;

  for (int i = 1; i <= time; i++) {
    int max_distance = 0;

    for (int j = 0; j < names.size(); j++) {
      int distance =
          get_distance(speeds[names[j]], periods[names[j]], rests[names[j]], i);
      if (distance > max_distance) {
        leaders.clear();
        leaders.push_back(names[j]);
        max_distance = distance;
      } else if (distance == max_distance) {
        leaders.push_back(names[j]);
      }
    }

    for (int j = 0; j < leaders.size(); j++) {
      points[leaders[j]]++;
    }
  }

  for (int i = 0; i < names.size(); i++) {
    ans2 = std::max(ans2, points[names[i]]);
  }

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
