#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>

int evaluate_wire(
    std::string token, std::map<std::string, int> &value_map,
    std::map<std::string, std::vector<std::string>> &operations_map) {

  if (value_map.find(token) != value_map.end()) {
    return value_map[token];
  } else if (std::all_of(token.begin(), token.end(), ::isdigit)) {
    return std::stoi(token);
  } else {
    std::vector<std::string> operation = operations_map[token];
    int input1, input2, output;

    if (operation[0] == "SIGNAL") {
      output = evaluate_wire(operation[1], value_map, operations_map);
    } else if (operation[0] == "NOT") {
      output = ~evaluate_wire(operation[1], value_map, operations_map);
    } else if (operation[0] == "AND") {
      input1 = evaluate_wire(operation[1], value_map, operations_map);
      input2 = evaluate_wire(operation[2], value_map, operations_map);
      output = input1 & input2;
    } else if (operation[0] == "OR") {
      input1 = evaluate_wire(operation[1], value_map, operations_map);
      input2 = evaluate_wire(operation[2], value_map, operations_map);
      output = input1 | input2;
    } else if (operation[0] == "LSHIFT") {
      input1 = evaluate_wire(operation[1], value_map, operations_map);
      input2 = evaluate_wire(operation[2], value_map, operations_map);
      output = input1 << input2;
    } else if (operation[0] == "RSHIFT") {
      input1 = evaluate_wire(operation[1], value_map, operations_map);
      input2 = evaluate_wire(operation[2], value_map, operations_map);
      output = input1 >> input2;
    }

    value_map[token] = output;
    return output;
  }

  return 0;
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  int ans1, ans2;
  std::string token1, token2, token3, token4, token5;
  std::map<std::string, int> value_map;
  std::map<std::string, std::vector<std::string>>
      operations_map; // key: wire, value: operation, input1, optional[input2]

  while (std::getline(file, line)) {
    std::istringstream iss(line);
    iss >> token1 >> token2 >> token3;

    if (token2 == "->") {
      operations_map[token3] = {"SIGNAL", token1};
    } else if (token3 == "->") {
      iss >> token4;
      operations_map[token4] = {"NOT", token2};
    } else {
      iss >> token4 >> token5;
      operations_map[token5] = {token2, token1, token3};
    }
  }

  ans1 = evaluate_wire("a", value_map, operations_map);

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  value_map.clear();
  value_map["b"] = ans1;

  ans2 = evaluate_wire("a", value_map, operations_map);

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
