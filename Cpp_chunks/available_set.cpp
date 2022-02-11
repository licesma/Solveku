class SudokuGrid {
private:
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
public:
    SudokuGrid(vector<vector<int>> numberGrid, int n){
        /*...*/
        defineAvailableSets();
    }
};
