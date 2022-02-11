#include <iostream>
using namespace std;
#include <vector>
#include <stdexcept>
#include <numeric>
#include <cmath>
#include <sstream>
class Set{
public:
    vector<bool> array;
    int n, size = 0;
    Set(int n){
        this->n = n;
        this->array = vector<bool>(n, false);
    }
    bool checkValid(int num) const{
        if(num < 1 || n < num){
            stringstream ss;
            ss<<"Value must be in [1,";   ss<<n;   ss<<"].";
            throw std::invalid_argument( ss.str() );
        }
        return true;
    }
    bool checkDoubleInsertion(int num){
        if(array[num-1]){
            throw std::invalid_argument( "Value already in the set" );
        }
        return true;
    }

    bool has(int num){
        checkValid(num);
        return array[num-1];
    }

    void add(int num){
        checkValid(num);
        checkDoubleInsertion(num);
        size++;
        array[num-1] = true;
    }

    void remove(int num){
        checkValid(num);
        size--;
        array[num-1] = false;
    }

    vector<int> values(){
        vector<int> res;
        int i;
        for(i = 0; i < n; i++){
            if(array[i]){
                res.push_back(i+1);
            }
        }
        return res;
    }


    string str(){
        int i, n = array.size();
        bool empty = true;
        stringstream ss;
        ss<<'{';
        for( i = 0; i < n; i++){

            if(array[i]){
                empty = false;
                ss<<' '<<i+1<<',';
            }
        }
        if(empty) {
            return "{ }";
        }
        ss.seekp(-1, ss.cur);
        ss<<" }";
        return ss.str();
    }
};
class SudokuCell {
public:
    int value;
    Set *avSet;
    bool fixed;

    bool hasValue() const{
        return value != 0;
    }
    void safeAvSetRemove(int candidate) const{
        if(!hasValue()  && avSet->has(candidate)){
            this->avSet->remove(candidate);
        }
    }
};
class BracketImage{
public:
    vector<Set*> allBrackets;
    vector<Set*> row;
    vector<Set*> col;
    vector<Set*> box;
    BracketImage(int n){
        int i;
        for(i = 0; i < 3*n; i++){
            allBrackets.push_back(new Set(n));
        }
        for(i = 0; i < n; i++){
            row.push_back(allBrackets[i]);
            col.push_back(allBrackets[n+i]);
            box.push_back(allBrackets[2*n+i]);
        }
    }
};

class SudokuGrid {
private:
    int n ;
    vector<int> I, Omega;
    vector<vector<SudokuCell>> grid;
    BracketImage *images;

    int boxOf(int row, int col){
        int root = sqrt(n);
        return root*(row/root)+col/root;
    }
    void fillBracketImages(){
        images = new BracketImage(n);
        int num;
        for(int row: I) {
            for (int col: I) {
                num = grid[row][col].value;
                if (num != 0) {
                    images->row[row]->add(num);
                    images->col[col]->add(num);
                    images->box[boxOf(row,col)]->add(num);
                }
            }
        }
    }
    vector<pair<int,int>> boxIndexes(int row, int col){
        int root = sqrt(n), startRow = n*(row/n), startCol = n*(col/n), i,j;
        vector<pair<int,int>> res;
        for(i = 0; i < root; i++){
            for(j = 0; j < root; j++){
                res.emplace_back(startRow + i, startCol + j);
            }
        }
        return res;
    };
    void defineAvailableSets(){
        SudokuCell *cell;
        for(int i: I){
            for(int j: I){
                cell = &grid[i][j];
                for(int candidate: Omega) {
                    if (!cell->hasValue() && !images->row[i]->has(candidate) && !images->col[j]->has(candidate) && !images->box[boxOf(i,j)]->has(candidate)){
                            cell->avSet->add(candidate);

                    }
                }
            }
        }
    }

    void updateNeighborsAvailableSet(int row, int col, int num){
        vector<pair<int,int>> boxIdx = boxIndexes(row,col);
        for(int it: I){
            grid[row][it].safeAvSetRemove(num);
            grid[it][col].safeAvSetRemove(num);
            grid[boxIdx[it].first][boxIdx[it].second].safeAvSetRemove(num);
        }
    }

    void updateCell(int row, int col, int num){
        grid[row][col].value = num;
        grid[row][col].avSet = nullptr;
        images->row[row]->add(num);
        images->col[col]->add(num);
        images->box[boxOf(row, col)]->add(num);
        updateNeighborsAvailableSet(row, col, num);
    }

public:
    void stageOne(){
        SudokuCell *cell;
        bool affectedCells = false;
        for(int row: I){
            for(int col: I){
                cell = &grid[row][col];
                if(!cell->hasValue() && cell->avSet->size == 1){
                  //cout<<cell->avSet->values()[0]<<" \n";
                    affectedCells = true;
                    updateCell(row, col, cell->avSet->values()[0]);
                }

            }
        }
        if(affectedCells){
            stageOne();
        }
    }
    void resizeGrid(){
        vector<SudokuCell> rowVector;
        rowVector.resize(n, SudokuCell());
        grid.resize(n, rowVector);
    }
    void initializeGrid(vector<vector<int>> &numberGrid){
        int value;
        for(int row: I){
            for(int col: I){
                value = numberGrid[row][col];
                if(value != 0) {
                    grid[row][col].value = value;
                    grid[row][col].fixed = true;
                }
                else{
                    grid[row][col].avSet = new Set(n);
                }
            }
        }
    }
public:
    SudokuGrid(vector<vector<int>> numberGrid, int n){
        SudokuGrid::n = n;
        I = vector<int>(n);   iota(I.begin(), I.end(), 0);
        Omega = vector<int>(n);   iota(Omega.begin(), Omega.end(), 1);
        images = new BracketImage(n);
        resizeGrid();
        initializeGrid(numberGrid);
        fillBracketImages();
        defineAvailableSets();
    }

    void print(){
        int root = sqrt(n);
        for(int row: I){
            for(int col : I){
                cout<<grid[row][col].value<<" ";
                if(col%root == root-1){
                    cout<<"  ";
                }
            }
            cout<<"\n";
            if(row%root == root-1){
                cout<<"\n";
            }
        }
    }
};


int main() {

    vector<int>
            r0 = {0, 0, 7,   5, 0, 0,   0, 1, 3},
            r1 = {4, 0, 5,   0, 0, 0,   6, 0, 9},
            r2 = {6, 0, 0,   0, 0, 2,   0, 0, 0},

            r3 = {7, 0, 0,   6, 1, 0,   0, 0, 0},
            r4 = {0, 0, 3,   0, 0, 0,   1, 0, 0},
            r5 = {0, 0, 0,   0, 2, 7,   0, 6, 4},

            r6 = {8, 1, 0,   2, 5, 3,   7, 0, 6},
            r7 = {5, 7, 0,   9, 6, 0,   4, 3, 8},
            r8 = {3, 9, 0,   0, 0, 4,   0, 0, 0};

    vector<vector<int>> numberGrid ;
    numberGrid.push_back(r0);
    numberGrid.push_back(r1);
    numberGrid.push_back(r2);
    numberGrid.push_back(r3);
    numberGrid.push_back(r4);
    numberGrid.push_back(r5);
    numberGrid.push_back(r6);
    numberGrid.push_back(r7);
    numberGrid.push_back(r8);
    SudokuGrid g = SudokuGrid(numberGrid, 9);

    g.print();
    g.stageOne();
    g.print();

   // cout<<g.grid[0][1].avSet->str();
}
