class SudokuCell {
public:
    int value;
    Set *avSet = nullptr;
    bool fixed;
    /*...*/
    void safeAvSetRemove(int num){
        if(!hasValue()  && avSet->has(num)){
            this->avSet->remove(num);
        }
    }
};