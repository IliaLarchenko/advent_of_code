#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>

bool fight(int player_hp, int player_damage, int player_armor, int boss_hp,
           int boss_damage, int boss_armor) {
  int player_turns = (boss_hp) / std::max(1, player_damage - boss_armor);
  if ((boss_hp) % std::max(1, player_damage - boss_armor) != 0) {
    player_turns++;
  }
  int boss_turns = (player_hp) / std::max(1, boss_damage - player_armor);
  if ((player_hp) % std::max(1, boss_damage - player_armor) != 0) {
    boss_turns++;
  }
  return player_turns <= boss_turns;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, token;
  int cost, damage, armor;
  int boss_hp, boss_damage, boss_armor;
  std::map<std::string, int[3]> weapon_map, armor_map, ring_map;
  int ans1, ans2 = 0;
  int num;

  std::getline(file, line);
  std::istringstream iss(line);
  iss >> token >> token >> boss_hp;
  std::getline(file, line);
  std::istringstream iss2(line);
  iss2 >> token >> boss_damage;
  std::getline(file, line);
  std::istringstream iss3(line);
  iss3 >> token >> boss_armor;
  file.close();

  file.open("weapons.txt");
  while (std::getline(file, line)) {
    std::istringstream iss(line);
    iss >> token >> cost >> damage >> armor;
    weapon_map[token][0] = cost;
    weapon_map[token][1] = damage;
    weapon_map[token][2] = armor;
  }
  file.close();

  file.open("armor.txt");
  while (std::getline(file, line)) {
    std::istringstream iss(line);
    iss >> token >> cost >> damage >> armor;
    armor_map[token][0] = cost;
    armor_map[token][1] = damage;
    armor_map[token][2] = armor;
  }
  armor_map["none"][0] = 0;
  armor_map["none"][1] = 0;
  armor_map["none"][2] = 0;
  file.close();

  file.open("rings.txt");
  while (std::getline(file, line)) {
    std::istringstream iss(line);
    iss >> token >> cost >> damage >> armor;
    ring_map[token][0] = cost;
    ring_map[token][1] = damage;
    ring_map[token][2] = armor;
  }
  ring_map["none1"][0] = 0;
  ring_map["none1"][1] = 0;
  ring_map["none1"][2] = 0;
  ring_map["none2"][0] = 0;
  ring_map["none2"][1] = 0;
  ring_map["none2"][2] = 0;
  file.close();

  for (auto weapon : weapon_map) {
    for (auto armor : armor_map) {
      for (auto ring1 : ring_map) {
        for (auto ring2 : ring_map) {
          if (ring1.first == ring2.first) {
            continue;
          }
          int cost = weapon.second[0] + armor.second[0] + ring1.second[0] +
                     ring2.second[0];
          int damage_pl = weapon.second[1] + armor.second[1] + ring1.second[1] +
                          ring2.second[1];
          int armor_pl = weapon.second[2] + armor.second[2] + ring1.second[2] +
                         ring2.second[2];
          if (fight(100, damage_pl, armor_pl, boss_hp, boss_damage,
                    boss_armor)) {
            if (ans1 == 0 || cost < ans1) {
              ans1 = cost;
            }
          } else {
            if (cost > ans2) {
              ans2 = cost;
            }
          }
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
