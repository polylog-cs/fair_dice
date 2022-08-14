#include <iostream>
#include <cassert>
#include <fstream>
#include <vector>
#include <random>
#include <string>
#include <algorithm>
#include <iterator>
#include <map>
#include <thread>
#include <mutex>
#include <unordered_set>
using namespace std;
typedef long long ll; 

const int LEN = 12;
const ll P = 999983;
vector<string> triplets;
ofstream dump_triplets("triplets.txt");
mutex mtx;


void dp_step(vector<ll>& oldvec, vector<ll>& newvec, string& dice, char c){
    newvec.resize(oldvec.size(), 0);
    for(int i = 0; i < dice.size(); ++i){
        newvec[i+1] = newvec[i];
        if(dice[i] == c){
            newvec[i+1] += oldvec[i]; 
        }
    }
}

bool check_fair(string dice){
    // assume alphabet ABC
    map<string, vector<ll>> dp; 
    dp[""] = vector<ll>(dice.size()+1, 1);

    for(char c : {'A', 'B', 'C'}){
        dp_step(dp[""], dp[""+string(1,c)], dice, c);
    }


    for(char c1 : {'A', 'B', 'C'}){
        for(char c2 : {'A', 'B', 'C'}){
            if(c1 == c2) continue;
            string s = string(1,c1) + string(1,c2);
            dp_step(dp[string(1,c1)], dp[s], dice, c2);
        }
    }

    for(char c1 : {'A', 'B', 'C'}){
        for(char c2 : {'A', 'B', 'C'}){
            if(c1 == c2) continue;
            for(char c3 : {'A', 'B', 'C'}){
                if(c1 == c3 || c2 == c3) continue;
                string s = string(1,c1) + string(1,c2) + string(1,c3);
                dp_step(dp[string(1,c1)+string(1,c2)], dp[s], dice, c3);
            }
        }
    }

    /*
    cout << dice << endl;
    for(auto p : dp){
        string s = p.first;
        vector<ll> vec = p.second;
        cout << s << "  ";
        for(int i = 0; i < vec.size(); ++i){
            cout << vec[i] << " ";
        }cout << endl;
    }*/
    
    ll val = -1;
    for(auto p : dp){
        string s = p.first;
        vector<ll> vec = p.second;
        if(s.size() == 3){
            if(val == -1){
                val = vec[dice.size()];
            }
            else if(val != vec[dice.size()]){
                return false;
            }
        }
    }

    return true;
}   

vector<string> load(string filename){

    ifstream f(filename);
    string s;
    vector<string> ret;
    while(f >> s){
        ret.push_back(s);
    }
    return ret;
}

vector<string> rename(vector<string>& dices, map<char, char> m){
    vector<string> ret;
    for(int i = 0; i < dices.size(); ++i){
        string s;
        for(int j = 0; j < dices[i].size(); ++j){
            s.push_back(m[dices[i][j]]);
        }
        ret.push_back(s);
    }
    return ret;
}

unordered_set<ll> compute_prefix_hashes(vector<string>& dices){
    unordered_set<ll> ret;
    for(int i = 0; i < dices.size(); ++i){
        ll u = 0;
        for(int j = 0; j < dices[i].size(); ++j){
            u += dices[i][j] - 'A' + 1;
            u *= P;
            ret.insert(u);
        }
    }
    return ret;
}

void gen(string& diceAB, int posAB, string& diceAC, int posAC, string partial, ll partial_hash, unordered_set<ll>& hash_set, char status){
    if(posAB == 2*LEN){
        //assert(partial.size() + (24 - posAC) == 36);
        string triplet = partial + diceAC.substr(posAC);
        if(check_fair(triplet)){
            //cout << triplet << endl;
            //dump_triplets << triplet << endl;
            mtx.lock();
            triplets.push_back(triplet);
            mtx.unlock();
        }
        return;
    }

    if(posAC == 2*LEN){
        //assert(partial.size() + (24 - posAB) == 36);
        string triplet = partial + diceAB.substr(posAB);
        if(check_fair(triplet)){
            //cout << triplet << endl;
            //dump_triplets << triplet << endl;
            mtx.lock();
            triplets.push_back(triplet);
            mtx.unlock();
        }
        return;
    }

    //now we can index by posAB and posAC

    if(diceAB[posAB] == 'A' && diceAC[posAC] == 'A'){//lucky case of two As
        gen(diceAB, posAB+1, diceAC, posAC+1, partial + "A", partial_hash, hash_set, status | 1);
    }
    else{
        // continue with AB string
        if(diceAB[posAB] == 'B'){
            ll newpartial_hash = partial_hash + 2;
            newpartial_hash *= P;
            if(hash_set.count(newpartial_hash) && (status & 1)){
                gen(diceAB, posAB+1, diceAC, posAC, partial + diceAB[posAB], newpartial_hash, hash_set, status | 2);
            }
        }

        // continue with AC string
        if(diceAC[posAC] == 'C'){
            ll newpartial_hash = partial_hash + 3;
            newpartial_hash *= P;
            if(hash_set.count(newpartial_hash) && ((status & 3) == 3)){
                gen(diceAB, posAB, diceAC, posAC+1, partial + diceAC[posAC], newpartial_hash, hash_set, status);//todo volat bez statusu?
            }
        }
    }
}

void gen_fair_triplets(vector<string> dicesAB, vector<string> dicesAC, unordered_set<ll> hash_set, int from, int to){

    for(int i = from; i < to; ++i){
        string diceAB = dicesAB[i];
        cout << i << " " << i - from << "/" << to-from << " " << diceAB << " " << triplets.size() << endl;
        for(string diceAC : dicesAC){
            //cout << diceAB << " " << diceAC << endl;
            //return;
            gen(diceAB, 0, diceAC, 0, "", 0, hash_set, 0);
            //return;
        }
        //return;
    }
}

int main(int argc, char** argv){

    auto dicesAB = load("AB"+to_string(LEN)+".txt");
    //sort(dicesAB.begin(), dicesAB.end());
    random_device rd;
    mt19937 g(rd());
    shuffle(dicesAB.begin(), dicesAB.end(), g);
    
    auto dicesBC = rename(dicesAB, {{'A', 'B'}, {'B', 'C'}});
    auto dicesAC = rename(dicesAB, {{'A', 'A'}, {'B', 'C'}});
    //cout << dicesAB[0] << endl << dicesBC[0] << endl << dicesAC[0] << endl;

    auto hash_set = compute_prefix_hashes(dicesBC);

  //gen_fair_triplets(dicesAB, dicesAC, hash_set, (0 * dicesAB.size()), (1 * dicesAB.size()));



    int T = 7;
    thread th1(gen_fair_triplets, dicesAB, dicesAC, hash_set, (0 * dicesAB.size())/T, (1 * dicesAB.size())/T);
    thread th2(gen_fair_triplets, dicesAB, dicesAC, hash_set, (1 * dicesAB.size())/T, (2 * dicesAB.size())/T);
    thread th3(gen_fair_triplets, dicesAB, dicesAC, hash_set, (2 * dicesAB.size())/T, (3 * dicesAB.size())/T);
    thread th4(gen_fair_triplets, dicesAB, dicesAC, hash_set, (3 * dicesAB.size())/T, (4 * dicesAB.size())/T);
    thread th5(gen_fair_triplets, dicesAB, dicesAC, hash_set, (4 * dicesAB.size())/T, (5 * dicesAB.size())/T);
    thread th6(gen_fair_triplets, dicesAB, dicesAC, hash_set, (5 * dicesAB.size())/T, (6 * dicesAB.size())/T);
    thread th7(gen_fair_triplets, dicesAB, dicesAC, hash_set, (6 * dicesAB.size())/T, (7 * dicesAB.size())/T);
    
    th1.join();
    th2.join();
    th3.join();
    th4.join();
    th5.join();
    th6.join();
    th7.join();

    dump_triplets << endl << endl << endl;
    cout << triplets.size() << endl;
    for(auto triplet : triplets){
        cout << triplet << endl;
        dump_triplets << triplet <<  endl;
    }
    
}