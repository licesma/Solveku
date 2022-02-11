//
// Created by lices on 01/02/2022.
//
#include <vector>
#include <stdexcept>
#include <math.h>
using namespace std;

class ValueSet{
public:
    vector<bool> array;
    ValueSet(int n){
        array = vector<bool>(n);
    }

    bool get(int index){
        if(index < 1 || array.size() < index){
            throw std::invalid_argument( "Value must be in [1,"<<array.size()<<"]" );
        }
        return array[index-1];
    }

    void set(int index, bool value){
        if(index < 1 || array.size() < index){
            throw std::invalid_argument( "Value must be in [1,n]" );
        }
        array[index-1] = value;
    }

\
};
class SudokuCell {
public:
    int value;
    ValueSet avSet;
    bool fixed;
    SudokuCell(int n, int value = 0, bool fixed = false){
        this->value = value;
        this->avSet = ValueSet(n);
        this->fixed = fixed;
    }
    bool hasValue(){
        return value != 0;
    }
};
class SudokuGrid {
public:
    int n;
    vector<vector<SudokuCell>> Grid;
    vector<ValueSet> RowValues;
    vector<ValueSet> ColValues;
    vector<ValueSet> BoxValues;
public: SudokuGrid(vector<vector<int>> numberGrid, int n){
        this->n = n;
        int i, j, value;
        vector<SudokuCell> row;
        row.resize(n, SudokuCell(n));
        Grid.resize(n, row);
        for(i = 0; i < n; i++){
            for(j = 0; j < n; j++){
                value = numberGrid[i][j];
                Grid[i][j].value = value;
                Grid[i][j].fixed = value != 0;
            }
        }
    }
    void print(){
        int root = (int) sqrt(n);
        int i, j;
        for(i = 0; i < n; i++){
            for(j = 0; j < n; j++){
                cout<<Grid[i][j].value<<" ";
                if(j%root == root-1){
                    cout<<"  ";
                }
            }
            cout<<"\n";
            if(i%root == root-1){
                cout<<"\n";
            }
        }
    }
};



#endif //CPP_SUDOKUGRID_H
