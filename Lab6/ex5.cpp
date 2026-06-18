/*
 * Compile: g++ -std=c++17 -o ex5 ex5.cpp
 */
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::map<std::string, std::vector<int>> gradebook = {
        {"alice",   {90, 85, 92}},
        {"bob",     {78, 88}},
        {"charlie", {95, 70, 80}},
    };

    std::map<std::string, int> averages;
    for (auto& [name, scores] : gradebook) {
        int sum = 0;
        for (int s : scores) sum += s;
        averages[name] = sum / scores.size();
    }

    std::sort(averages.begin(), averages.end());

    std::cout << "Rankings:" << std::endl;
    for (auto& [name, avg] : averages) {
        std::cout << "  " << name << ": " << avg << std::endl;
    }

    return 0;
}
