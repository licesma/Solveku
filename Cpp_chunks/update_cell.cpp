class SudokuGrid {
private:
    /*...*/
    void updateNeighborsAvailableSet(int row, int col, int num) {
        int it;
        vector <pair<int, int>> boxIdx = boxIndexes(row, col);
        for (it = 0; it < n; it++) {
            Grid[row][it].safeAvSetRemove(num);
            Grid[it][col].safeAvSetRemove(num);
            Grid[boxIdx[it].first][boxIdx[it].second].safeAvSetRemove(num);
        }
    }

    void updateCell(int row, int col, int num) {
        Grid[row][col].value = num;
        Grid[row][col].avSet = nullptr;
        RowValues[row].add(num);
        ColValues[col].add(num);
        BoxValues[boxOf(row, col)].add(num);
        updateNeighborsAvailableSet(row, col, num);
    }
    /*...*/
};