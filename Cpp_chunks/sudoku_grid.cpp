class SudokuGrid {
private:
    int n ;
    vector<int> I, Omega;
    vector<vector<SudokuCell>> grid;
    int boxOf(int row, int col){
        int root = sqrt(n);
        return root*(row/root)+col/root;
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
    }
};
