#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>

std::vector<std::string> tokenize(const std::string& text) {
    std::vector<std::string> words;
    std::istringstream stream(text);
    std::string word;
    while (stream >> word) {
        for (auto& c : word) c = std::tolower(c);
        words.push_back(word);
    }
    return words;
}

std::vector<std::string> unique_words(const std::vector<std::string>& words) {
    std::vector<std::string> seen;
    for (const auto& w : words) {
        bool found = false;
        for (const auto& s : seen) {   
            if (s == w) { found = true; break; }
        }
        if (!found) seen.push_back(w);
    }
    return seen;
}

int count_word(const std::vector<std::string>& words, const std::string& target) {
    int n = 0;
    for (const auto& w : words) {   
        if (w == target) n++;
    }
    return n;
}

int main(int argc, char* argv[]) {
    const char* filename = argc > 1 ? argv[1] : "big.txt";
    std::ifstream file(filename);
    if (!file) { std::cerr << "cannot open " << filename << std::endl; return 1; }

    std::string text((std::istreambuf_iterator<char>(file)),
                      std::istreambuf_iterator<char>());

    auto words = tokenize(text);
    auto vocab = unique_words(words);

    std::vector<std::pair<std::string, int>> freqs;
    for (const auto& w : vocab) {
        freqs.push_back({w, count_word(words, w)});
    }

    std::partial_sort(freqs.begin(),
        freqs.begin() + std::min<size_t>(10, freqs.size()),
        freqs.end(),
        [](const auto& a, const auto& b) { return a.second > b.second; });

    for (int i = 0; i < 10 && i < (int)freqs.size(); i++) {
        std::cout << freqs[i].first << " " << freqs[i].second << std::endl;
    }
    return 0;
}
