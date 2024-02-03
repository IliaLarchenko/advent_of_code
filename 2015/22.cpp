#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

int turn(int player_hp, int player_mana, int boss_hp, int boss_damage,
         std::map<std::string, int[6]> &spells_map,
         std::set<std::string> &effects,
         std::map<std::string, int> active_effects, bool player_turn = true,
         int turn_count = 0, bool hard_mode = false) {

  if (hard_mode && player_turn) {
    player_hp--;
  }
  if (turn_count > 15) {
    return -1;
  }

  int player_armor = 0;

  if (boss_hp <= 0) {
    return 0;
  }
  if (player_hp <= 0) {
    return -1;
  }
  if (player_mana < 0) {
    return -1;
  }

  // apply active effects
  std::set<std::string> to_remove;
  for (auto effect : active_effects) {
    player_armor += spells_map[effect.first][2];
    boss_hp -= spells_map[effect.first][1];
    player_mana += spells_map[effect.first][4];
    active_effects[effect.first] -= 1;

    if (active_effects[effect.first] == 0) {
      to_remove.insert(effect.first);
    }
  }
  for (auto effect : to_remove) {
    active_effects.erase(effect);
  }

  if (boss_hp <= 0) {
    return 0;
  }

  int min_mana_spent = -1;
  if (player_turn) {
    for (auto spell : spells_map) {
      if (active_effects.find(spell.first) != active_effects.end()) {
        continue;
      }
      if (player_mana <= spell.second[0]) {
        continue;
      }
      int new_mana_spent = 0;
      if (effects.find(spell.first) != effects.end()) {
        std::map<std::string, int> new_active_effects = active_effects;
        new_active_effects[spell.first] = spell.second[5];
        new_mana_spent =
            turn(player_hp, player_mana - spell.second[0], boss_hp, boss_damage,
                 spells_map, effects, new_active_effects, false, turn_count + 1,
                 hard_mode);
      } else {
        new_mana_spent =
            turn(player_hp + spell.second[3], player_mana - spell.second[0],
                 boss_hp - spell.second[1], boss_damage, spells_map, effects,
                 active_effects, false, turn_count + 1, hard_mode);
      }
      if ((new_mana_spent + spell.second[0] < min_mana_spent ||
           min_mana_spent == -1) &&
          new_mana_spent != -1) {
        min_mana_spent = new_mana_spent + spell.second[0];
      }
    }
  } else {
    return turn(player_hp - std::max(1, boss_damage - player_armor),
                player_mana, boss_hp, boss_damage, spells_map, effects,
                active_effects, true, turn_count + 1, hard_mode);
  }

  return min_mana_spent;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, token;
  int cost, damage, armor;
  int boss_hp, boss_damage;
  std::map<std::string, int[6]>
      spells_map; // cost, damage, armor, heal, mana, duration
  std::set<std::string> effects = {"Shield", "Poison", "Recharge"};
  int ans1, ans2 = 0;
  int num;

  std::getline(file, line);
  std::istringstream iss(line);
  iss >> token >> token >> boss_hp;
  std::getline(file, line);
  std::istringstream iss2(line);
  iss2 >> token >> boss_damage;
  file.close();

  spells_map["Missile"][0] = 53;
  spells_map["Missile"][1] = 4;

  spells_map["Drain"][0] = 73;
  spells_map["Drain"][1] = 2;
  spells_map["Drain"][3] = 2;

  spells_map["Shield"][0] = 113;
  spells_map["Shield"][2] = 7;
  spells_map["Shield"][5] = 6;

  spells_map["Poison"][0] = 173;
  spells_map["Poison"][1] = 3;
  spells_map["Poison"][5] = 6;

  spells_map["Recharge"][0] = 229;
  spells_map["Recharge"][4] = 101;
  spells_map["Recharge"][5] = 5;

  ans1 = turn(50, 500, boss_hp, boss_damage, spells_map, effects, {}, true, 0);

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  ans2 = turn(50, 500, boss_hp, boss_damage, spells_map, effects, {}, true, 0,
              true);

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
