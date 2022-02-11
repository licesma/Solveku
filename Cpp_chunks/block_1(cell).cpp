//
// Created by lices on 01/02/2022.
//
#include <vector>
#include <stdexcept>
using namespace std;
class AvailableSet{
public:
    bool *array;
    int n;
    AvailableSet(int n){
        this->n = n;
        array = new bool[n]();
    }

    bool& at(int i){
        if(i < 1 || n < i){
            throw invalid_argument( "Value must be in [1,n]" );
        }
        return *(array+i-1);
    }
};
class SudokuCell {
public:
    int value;
    AvailableSet *avSet;
    bool fixed;
    SudokuCell(int n, int value = 0, bool fixed = false){
        this->value = value;
        this->avSet = new AvailableSet(n);
        this->fixed = fixed;
    }
};