#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

void refine_input() {
  // refine the input file
  std::ifstream inputFile("input.txt");
  std::ofstream outputFile("refined_input.txt");

  std::map<std::string, std::string> replacements = {
      {"Al", "L"}, {"Si", "S"}, {"Ti", "I"}, {"Th", "T"},
      {"Mg", "M"}, {"Ar", "R"}, {"Ca", "C"}, {"Rn", "Q"},
  };

  std::string line;
  while (getline(inputFile, line)) {
    for (const auto &pair : replacements) {
      size_t pos = 0;
      while ((pos = line.find(pair.first, pos)) != std::string::npos) {
        line.replace(pos, pair.first.length(), pair.second);
        pos += pair.second.length();
      }
    }
    outputFile << line << std::endl;
  }

  inputFile.close();
  outputFile.close();
  return;
}

std::set<std::string>
get_next_step(std::set<std::string> molecules,
              std::map<char, std::vector<std::string>> replacements) {
  std::set<std::string> new_molecules;

  for (auto &molecule : molecules) {
    for (auto &replacement : replacements) {
      for (int i = 0; i < molecule.size(); i++) {
        if (molecule[i] == replacement.first) {
          for (auto &to : replacement.second) {
            std::string new_molecule = molecule;
            new_molecule.replace(i, 1, to);
            new_molecules.insert(new_molecule);
          }
        }
      }
    }
  }

  return new_molecules;
}

std::map<char, std::vector<std::string>> generate_next_steps_replacements(
    std::map<char, std::vector<std::string>> original_replacements,
    std::map<char, std::vector<std::string>> latest_replacements) {
  std::map<char, std::vector<std::string>> new_replacements;

  for (auto &replacement : original_replacements) {
    for (auto &to : replacement.second) {
      for (auto &latest : latest_replacements) {
        for (auto &latest_to : latest.second) {
          if (replacement.first == latest_to[0]) {
            new_replacements[latest.first].push_back(
                to + latest_to.substr(1, latest_to.size() - 1));
          }
        }
      }
    }
  }

  return new_replacements;
}

std::map<char, std::vector<std::pair<std::string, int>>>
get_n_step_replacements(std::map<char, std::vector<std::string>> replacements,
                        int max_num_replacements) {
  std::map<char, std::vector<std::pair<std::string, int>>> n_step_replacements;
  std::map<char, std::vector<std::string>> temp_replacements = replacements;

  for (auto &replacement : temp_replacements) {
    n_step_replacements[replacement.first].push_back(
        std::make_pair(std::string("") + replacement.first, 0));
  }

  n_step_replacements['Q'].push_back(std::make_pair("Q", 0));
  n_step_replacements['R'].push_back(std::make_pair("R", 0));
  n_step_replacements['Y'].push_back(std::make_pair("Y", 0));

  for (int i = 0; i < max_num_replacements; i++) {
    for (auto &replacement : temp_replacements) {
      for (auto &to : replacement.second) {
        n_step_replacements[replacement.first].push_back(
            std::make_pair(to, i + 1));
      }
    }
    if (i < max_num_replacements - 1) {
      temp_replacements =
          generate_next_steps_replacements(replacements, temp_replacements);
    }
  }
  return n_step_replacements;
}
std::map<std::string, int> generate_valid_molecules(
    std::map<std::string, int> &molecules,
    std::map<char, std::vector<std::pair<std::string, int>>>
        &n_step_replacements,
    char target_symbol) {
  std::map<std::string, int> new_molecules;

  for (auto &molecule : molecules) {
    char from = molecule.first[0];
    if (n_step_replacements.find(from) != n_step_replacements.end()) {
      for (auto &replacement : n_step_replacements[from]) {
        if (replacement.first[0] == target_symbol) {
          std::string new_molecule = molecule.first;
          new_molecule.replace(
              0, 1, replacement.first.substr(1, replacement.first.size() - 1));
          if (new_molecules.find(new_molecule) == new_molecules.end() ||
              new_molecules[new_molecule] >
                  molecule.second + replacement.second) {
            new_molecules[new_molecule] = molecule.second + replacement.second;
          }
        }
      }
    }
  }
  return new_molecules;
}

std::map<std::string, int>
filter_longest_molecules(std::map<std::string, int> molecules) {
  std::map<std::string, int> new_molecules;
  int max_length = 0;
  int max_count = 0;

  for (auto &molecule : molecules) {
    if (molecule.first.size() > max_length) {
      max_length = molecule.first.size();
      max_count = molecule.second;
    }
  }

  for (auto &molecule : molecules) {
    if (molecule.first.size() != max_length && molecule.second != max_count) {
      new_molecules[molecule.first] = molecule.second;
    }
  }

  return new_molecules;
}

int main() {
  refine_input();

  std::ifstream file("refined_input.txt");
  std::string line, token;
  std::map<char, std::vector<std::string>> replacements;
  std::set<std::string> molecules;
  std::set<int> lengths;
  int ans1, ans2 = 0;

  while (std::getline(file, line)) {
    if (line == "") {
      break;
    }
    std::istringstream iss(line);
    std::string from, to;
    iss >> from >> token >> to;
    replacements[from[0]].push_back(to);
    lengths.insert(from.size());
  }

  std::getline(file, line);
  std::string molecule = line;
  molecules = {molecule};

  molecules = get_next_step(molecules, replacements);

  ans1 = molecules.size();

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::map<std::string, int> solved;
  solved["e"] = 0;

  std::map<char, std::vector<std::pair<std::string, int>>> n_step_replacements,
      n_step_replacements_small;

  n_step_replacements = get_n_step_replacements(replacements, 3);

  for (int i = 0; i < molecule.size(); i++) {
    solved = generate_valid_molecules(solved, n_step_replacements, molecule[i]);
    while (solved.size() > 100) {
      solved = filter_longest_molecules(solved);
    }
  }

  for (auto &s : solved) {
    if (s.first == "") {
      ans2 = s.second;
    }
  }

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
