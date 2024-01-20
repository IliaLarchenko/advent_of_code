#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int length, width, height;
  int paper = 0;
  int ribbon = 0;

  while (std::getline(file, line)) {

    std::replace(line.begin(), line.end(), 'x', ' ');
    std::istringstream iss(line);

    std::cout << line << std::endl;

    iss >> length >> width >> height;

    int sides[3] = {length * width, width * height, height * length};
    int smallest_side;
    smallest_side = std::min(std::min(sides[0], sides[1]), sides[2]);

    paper += 2 * sides[0] + 2 * sides[1] + 2 * sides[2] + smallest_side;

    int perimeters[3] = {2 * length + 2 * width, 2 * width + 2 * height,
                         2 * height + 2 * length};
    int smallest_perimeter;
    smallest_perimeter =
        std::min(std::min(perimeters[0], perimeters[1]), perimeters[2]);

    ribbon += length * width * height + smallest_perimeter;
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << paper << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ribbon << std::endl;

  file.close();
  return 0;
}
