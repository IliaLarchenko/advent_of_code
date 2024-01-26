#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int count_lights(char lights[102][102], bool toggle_corner = false) {
  int ans = 0;
  for (int n = 0; n < 100; n++) {
    if (toggle_corner) {
      lights[1][1] = '#';
      lights[1][100] = '#';
      lights[100][1] = '#';
      lights[100][100] = '#';
    }

    char new_lights[102][102] = {'.'};

    for (int i = 0; i < 100; i++) {
      for (int j = 0; j < 100; j++) {
        int count = 0;
        for (int k = i; k < i + 3; k++) {
          for (int l = j; l < j + 3; l++) {
            if (lights[k][l] == '#') {
              count++;
            }
          }
        }
        if (lights[i + 1][j + 1] == '#') {
          count--;
          if (count == 2 || count == 3) {
            new_lights[i + 1][j + 1] = '#';
          }
        } else if (count == 3) {
          new_lights[i + 1][j + 1] = '#';
        }
      }
    }

    for (int i = 0; i < 102; i++) {
      for (int j = 0; j < 102; j++) {
        lights[i][j] = new_lights[i][j];
      }
    }
  }

  for (int i = 0; i < 102; i++) {
    for (int j = 0; j < 102; j++) {
      if (lights[i][j] == '#') {
        ans++;
      } else if (toggle_corner && (i == 1 || i == 100) &&
                 (j == 1 || j == 100)) {
        ans++;
      }
    }
  }

  return ans;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, name;
  int ans1, ans2 = 0;
  char lights[102][102], temp[102][102] = {'.'};

  int i = 0;
  while (std::getline(file, line)) {
    for (int j = 0; j < line.size(); j++) {
      lights[i + 1][j + 1] = line[j];
    }
    i++;
  }

  for (int i = 0; i < 102; i++) {
    for (int j = 0; j < 102; j++) {
      temp[i][j] = lights[i][j];
    }
  }

  ans1 = count_lights(temp);

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  ans2 = count_lights(lights, true);
  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
