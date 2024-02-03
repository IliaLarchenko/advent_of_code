#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

// simple bruteforce is enough for this problem

void min_quant(int i, int sums[3], long long prods[3], int counts[3],
               long target, std::vector<int> &presents, int &best_count,
               long long &best_prod) {
  if (i < 0) {
    if (sums[0] == target && sums[1] == target && sums[2] == target) {
      if (counts[0] <= counts[1] && counts[0] <= counts[2]) {
        if (counts[0] <= best_count && prods[0] < best_prod) {
          best_prod = prods[0];
          best_count = counts[0];
        }
      }
    }
    return;
  }

  if (sums[0] > target || sums[1] > target || sums[2] > target) {
    return;
  }

  if (counts[0] > best_count || prods[0] > best_prod) {
    return;
  }

  if (sums[0] + (best_count - counts[0]) * presents[i] < target) {
    return;
  }

  for (int j = 0; j < 3; j++) {
    int new_sums[3] = {sums[0], sums[1], sums[2]};
    long long new_prods[3] = {prods[0], prods[1], prods[2]};
    int new_counts[3] = {counts[0], counts[1], counts[2]};

    new_sums[j] += presents[i];
    new_prods[j] *= presents[i];
    new_counts[j]++;
    min_quant(i - 1, new_sums, new_prods, new_counts, target, presents,
              best_count, best_prod);
  }
  return;
}

void min_quant2(int i, int sums[4], long long prods[4], int counts[4],
                long target, std::vector<int> &presents, int &best_count,
                long long &best_prod) {
  if (i < 0) {
    if (sums[0] == target && sums[1] == target && sums[2] == target &&
        sums[3] == target) {
      if (counts[0] <= counts[1] && counts[0] <= counts[2] &&
          counts[0] <= counts[3]) {
        if (counts[0] <= best_count && prods[0] < best_prod) {
          best_prod = prods[0];
          best_count = counts[0];
        }
      }
    }
    return;
  }

  if (sums[0] > target || sums[1] > target || sums[2] > target ||
      sums[3] > target) {
    return;
  }

  if (counts[0] > best_count || prods[0] > best_prod) {
    return;
  }

  if (sums[0] + (best_count - counts[0]) * presents[i] < target) {
    return;
  }

  for (int j = 0; j < 4; j++) {
    int new_sums[4] = {sums[0], sums[1], sums[2], sums[3]};
    long long new_prods[4] = {prods[0], prods[1], prods[2], prods[3]};
    int new_counts[4] = {counts[0], counts[1], counts[2], counts[3]};

    new_sums[j] += presents[i];
    new_prods[j] *= presents[i];
    new_counts[j]++;
    min_quant2(i - 1, new_sums, new_prods, new_counts, target, presents,
               best_count, best_prod);
  }
  return;
}

int main() {
  std::ifstream file("input.txt");
  std::string line, name, token;
  int num;
  std::vector<int> presents;
  long long ans1, ans2 = 0;

  while (std::getline(file, line)) {
    std::istringstream ss(line);
    ss >> num;
    presents.push_back(num);
  }

  int total = 0;
  for (int i = 0; i < presents.size(); i++) {
    total += presents[i];
  }

  int target = total / 3;

  int sums[3] = {0, 0, 0};
  long long prods[3] = {1, 1, 1};
  int counts[3] = {0, 0, 0};

  int best_count = 6;
  long long best_prod = 999999999999999;

  min_quant(presents.size() - 1, sums, prods, counts, target, presents,
            best_count, best_prod);
  ans1 = best_prod;

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  int sums2[4] = {0, 0, 0, 0};
  long long prods2[4] = {1, 1, 1, 1};
  int counts2[4] = {0, 0, 0, 0};

  best_count = 6;
  best_prod = 999999999999999;

  target = total / 4;
  min_quant2(presents.size() - 1, sums2, prods2, counts2, target, presents,
             best_count, best_prod);

  ans2 = best_prod;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << ans2 << std::endl;

  file.close();
  return 0;
}
