#include <iostream>
#include <string>
#include <unordered_map>

const std::string valid_alphabet ("abcdefghjkmnpqrstuvwxyz");
const std::string invalid_starts ("ghijklmnoyz");

bool check_pairs(std::string& s_in) {
    char prev = s_in.at(0);
    int found = 0;
    std::string used {""};
    for ( std::string::iterator it=s_in.begin() + 1; it!=s_in.end(); ++it)
        if (*it == prev) {
            found += 1;
            prev = 'A';
            used.push_back(*it);
        }
        else if (used.find(*it) != std::string::npos) {
            continue;
        }
        else {
            prev = *it;
        }
    if (found == 2) {
        return true;
    };
    return false;
}

bool check_straight(std::string& s_in) {
    char c {'A'};
    for (int i = 0; i<s_in.length(); i++) {
        c = s_in.at(i);
        if (invalid_starts.find(c) != std::string::npos) {
           continue; 
        }
        else if (i > s_in.length() - 3) {
            return false;
        }
        else if ((s_in.at(i+1) == valid_alphabet.at(valid_alphabet.find(s_in.at(i)) + 1)) && (s_in.at(i+2) == valid_alphabet.at(valid_alphabet.find(s_in.at(i)) + 2))) {
            return true;            
        }
    }
    return false;
}

void increment_password(std::string& s_in) {
    bool done = false;
    size_t c_idx = s_in.length() - 1;
    size_t s = 1;
    int c_inc = 0;
    while (!done) {
        c_inc = valid_alphabet.find(s_in.at(c_idx)) + 1;
        if (c_inc < valid_alphabet.length()) {
            done = true;
            s_in.replace(c_idx, s, &valid_alphabet.at(c_inc), 1);
        }
        else {
            s_in.replace(c_idx, s, &valid_alphabet.at(0), 1);
            c_idx -= 1;
        }
    }
}

int main() {
    std::string input = "hepxcrrq"; // Part I
    // std::string input = "hepxxyzz"; // Part II

    bool found_new = false;
    bool cond1 = false;
    bool cond2 = false;

    while (!found_new) {
        increment_password(input);
        cond1 = check_pairs(input);
        cond2 = check_straight(input);
        if (cond1 && cond2) {
            found_new = true;
        }
    }
    std::cout << input;

}
