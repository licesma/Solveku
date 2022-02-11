class BracketImage{
public:
    vector<Set*> allBrackets;
    vector<Set*> row;
    vector<Set*> col;
    vector<Set*> box;
    BracketImage(int n){
        int i;
        for(i = 0; i < 3*n; i++){
            all.push_back(new Set(n));
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
    /*...*/
    BracketImage *images;
    void fillBracketImages() {
        images = new BracketImage(n);
        int num;
        for (int row: I) {
            for (int col: I) {
                num = grid[row][col].value;
                if (num != 0) {
                    images->row[row]->add(num);
                    images->col[col]->add(num);
                    images->box[boxOf(row, col)]->add(num);
                }
            }
        }
    }
public:
    SudokuGrid(vector<vector<int>> numberGrid, int n){
        /*...*/
        fillBracketImages();
    }
};
