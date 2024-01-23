#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>

int dfs(std::map<std::pair<std::string, std::string>, int> distances,
        std::set<std::string> cities, std::string current, bool min = true) {
  if (cities.size() == 0) {
    return 0;
  }

  int ans = min ? 1000000000 : 0;
  int current_dist = 0;

  std::set<std::string> new_cities = cities;

  for (std::set<std::string>::iterator it = cities.begin(); it != cities.end();
       ++it) {
    std::string city = *it;

    new_cities.erase(city);

    if (current == "") {
      current_dist = 0;
    } else {
      current_dist = distances[std::make_pair(current, city)];
    }

    if (min) {
      ans = std::min(ans, dfs(distances, new_cities, city) + current_dist);
    } else {
      ans =
          std::max(ans, dfs(distances, new_cities, city, false) + current_dist);
    }

    new_cities.insert(city);
  }

  return ans;
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  std::map<std::pair<std::string, std::string>, int> distances;
  std::string from, to, token;
  std::set<std::string> cities;
  int distance;

  int ans1, ans2 = 0;

  while (std::getline(file, line)) {
    std::istringstream iss(line);
    iss >> from >> token >> to >> token >> distance;
    distances[std::make_pair(from, to)] = distance;
    distances[std::make_pair(to, from)] = distance;
    if (std::find(cities.begin(), cities.end(), from) == cities.end()) {
      cities.insert(from);
    }
    if (std::find(cities.begin(), cities.end(), to) == cities.end()) {
      cities.insert(to);
    }
  }

  ans1 = dfs(distances, cities, "");

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  ans2 = dfs(distances, cities, "", false);

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
