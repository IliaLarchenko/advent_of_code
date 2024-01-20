#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <string>

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int length, width, height;
  int x = 0;
  int y = 0;
  std::set<std::pair<int, int>> visited;
  visited.insert(std::make_pair(0, 0));

  std::getline(file, line);
  for (size_t i = 0; i < line.size(); ++i) {
    char c = line[i];

    if (c == '^') {
      y++;
    } else if (c == 'v') {
      y--;
    } else if (c == '>') {
      x++;
    } else if (c == '<') {
      x--;
    }
    visited.insert(std::make_pair(x, y));
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << visited.size() << std::endl;

  visited.clear();
  visited.insert(std::make_pair(0, 0));
  bool santa = true;
  int xr = 0;
  int yr = 0;
  x = 0;
  y = 0;

  for (size_t i = 0; i < line.size(); ++i) {
    char c = line[i];

    if (c == '^') {
      if (santa) {
        y++;
      } else {
        yr++;
      }
    } else if (c == 'v') {
      if (santa) {
        y--;
      } else {
        yr--;
      }
    } else if (c == '>') {
      if (santa) {
        x++;
      } else {
        xr++;
      }
    } else if (c == '<') {
      if (santa) {
        x--;
      } else {
        xr--;
      }
    }

    if (santa) {
      visited.insert(std::make_pair(x, y));
      santa = false;
    } else {
      visited.insert(std::make_pair(xr, yr));
      santa = true;
    }
  }

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << visited.size() << std::endl;

  file.close();
  return 0;
}
