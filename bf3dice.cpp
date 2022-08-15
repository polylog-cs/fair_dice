#include <bits/stdc++.h>

using namespace std;

bool check(string s) {
  vector < int > counts(27, 0); //counts of permutations, only 6 positions in this array are used
  for (int i = 0; i < 18; ++i) {
    for (int j = i + 1; j < 18; ++j) {
      if (s[i] != s[j]) {
        for (int k = j + 1; k < 18; ++k) {
          if (s[i] != s[k] && s[j] != s[k]) {
            ++counts[(s[k] - 'A') + 3 * (s[j] - 'A') + 9 * (s[k] - 'A')];
          }
        }
      }
    }
  }
  if (count(counts.begin(), counts.end(), 36) == 6) {
    return true;
  }
  return false;
}

void gen_all_triples(string s, int A, int B, int C) {
  if (s.size() == 18) {
    if (check(s)) {
      cout << s << endl;
    }
  } else {
    if (A < 6) {
      gen_all_triples(s + "A", A + 1, B, C);
    }
    if (B < 6) {
      gen_all_triples(s + "B", A, B + 1, C);
    }
    if (C < 6) {
      gen_all_triples(s + "C", A, B, C + 1);
    }
  }

}

int main() {
  gen_all_triples("", 0, 0, 0);
}