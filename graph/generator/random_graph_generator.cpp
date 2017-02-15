#include <fstream>
#include <time.h>
#include <iostream>
#include <cstdlib>
#include <cfloat>
#include <cmath>
using namespace std;

int n;
double p;

int main(int argc, char ** argv) {
    n = atoi(argv[1]);
    p = atof(argv[2]);

    srand(time(0));
    ofstream outFile;
    outFile.open("temp.csv");

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            float r = static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
            if (r <= p) {
                outFile << i << "\t" << j << "\n";
            }
        }
    }

    outFile.close();
    return 0;
}