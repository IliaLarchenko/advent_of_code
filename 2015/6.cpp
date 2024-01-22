#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main() {
  std::ifstream file("input.txt");
  std::string line;
  std::string token;
  int x1, y1, x2, y2;
  int lights1[1000][1000] = {0};
  int lights2[1000][1000] = {0};
  std::string action;
  int ans1 = 0;
  int ans2 = 0;

  while (std::getline(file, line)) {
    std::replace(line.begin(), line.end(), ',', ' ');
    std::replace(line.begin(), line.end(), 'l', ' ');
    std::istringstream iss(line);

    iss >> token >> action >> x1 >> y1 >> token >> x2 >> y2;

    for (int i = x1; i <= x2; i++) {
      for (int j = y1; j <= y2; j++) {
        if (action == "on") {
          lights1[i][j] = 1;
        } else if (action == "off") {
          lights1[i][j] = 0;
        } else if (action == "e") {
          lights1[i][j] = !lights1[i][j];
        }
      }
    }

    for (int i = x1; i <= x2; i++) {
      for (int j = y1; j <= y2; j++) {
        if (action == "on") {
          lights2[i][j]++;
        } else if (action == "off") {
          lights2[i][j] = std::max(0, lights2[i][j] - 1);
        } else if (action == "e") {
          lights2[i][j] += 2;
        }
      }
    }
  }

  for (int i = 0; i < 1000; i++) {
    for (int j = 0; j < 1000; j++) {
      ans1 += lights1[i][j];
      ans2 += lights2[i][j];
    }
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
