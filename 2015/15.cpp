#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main() {
  std::ifstream file("input.txt");
  std::string line, token, name;
  int ans1, ans2 = 0;
  int stats[4][5];
  int i = 0;

  while (std::getline(file, line)) {
    for (int j = 0; j < 4; j++) {
      line.replace(line.find(","), 1, "");
    }
    std::istringstream iss(line);
    iss >> token >> token >> stats[i][0] >> token >> stats[i][1] >> token >>
        stats[i][2] >> token >> stats[i][3] >> token >> stats[i][4];
    i++;
  }

  for (int a = 0; a <= 100; a++) {
    for (int b = 0; b <= 100 - a; b++) {
      for (int c = 0; c <= 100 - a - b; c++) {
        int d = 100 - a - b - c;

        int capacity = a * stats[0][0] + b * stats[1][0] + c * stats[2][0] +
                       d * stats[3][0];
        int durability = a * stats[0][1] + b * stats[1][1] + c * stats[2][1] +
                         d * stats[3][1];
        int flavor = a * stats[0][2] + b * stats[1][2] + c * stats[2][2] +
                     d * stats[3][2];
        int texture = a * stats[0][3] + b * stats[1][3] + c * stats[2][3] +
                      d * stats[3][3];
        int calories = a * stats[0][4] + b * stats[1][4] + c * stats[2][4] +
                       d * stats[3][4];

        if (capacity < 0 || durability < 0 || flavor < 0 || texture < 0) {
          continue;
        }

        int score = capacity * durability * flavor * texture;

        if (score > ans1) {
          ans1 = score;
        }

        if (calories == 500 && score > ans2) {
          ans2 = score;
        }
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
