#include <fstream>
#include <iostream>
#include <openssl/md5.h>
#include <sstream>
#include <string>

std::string md5_first_six_chars(const std::string &input) {
  unsigned char digest[MD5_DIGEST_LENGTH];
  MD5((unsigned char *)input.c_str(), input.length(), (unsigned char *)&digest);

  std::stringstream ss;
  for (unsigned int i = 0; i < 3; i++) {
    ss << std::hex << std::setw(2) << std::setfill('0') << (int)digest[i];
    if (i == 2) {
      return ss.str();
    }
  }

  return "";
}

int main() {
  std::ifstream file("input.txt");
  std::string line;
  std::getline(file, line);
  int ans1 = -1;

  int i = 0;
  while (true) {
    std::string input = line + std::to_string(i);
    std::string hash = md5_first_six_chars(input);
    if (ans1 == -1 && hash.substr(0, 5) == "00000") {
      ans1 = i;
    }
    if (hash == "000000") {
      break;
    }
    i++;
  }

  std::cout << "Part 1 answer:" << std::endl;
  std::cout << ans1 << std::endl;

  std::cout << "Part 2 answer:" << std::endl;
  std::cout << i << std::endl;

  file.close();
  return 0;
}
