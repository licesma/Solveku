class SudokuCell {
public:
    int value;
    Set *avSet;
    bool fixed;

    bool hasValue(){
        return value != 0;
    }
    void safeAvSetRemove(int candidate){
        if(!hasValue()  && avSet->has(candidate)){
            this->avSet->remove(candidate);
        }
    }
};