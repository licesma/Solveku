class SudokuGrid {
    /*...*/
public:
    void stageOne() {
        int row, col;
        SudokuCell *cell;
        bool affectedCells = false;
        for (row = 0; row < n; row++) {
            for (col = 0; col < n; col++) {
                cell = &Grid[row][col];
                if (!cell->hasValue() && cell->avSet->size == 1) {
                    affectedCells = true;
                    updateCell(row, col, cell->avSet->values()[0]);
                }

            }
        }
        if (affectedCells) {
            stageOne();
        }
    }
};