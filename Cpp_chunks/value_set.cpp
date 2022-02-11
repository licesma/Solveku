
class ValueSet{
public:
    vector<bool> array;
    int size = 0, n;
    ValueSet(int n){
        this->n = n;
        this->array = vector<bool>(n);
    }

    bool get(int index){
        if(index < 1 || array.size() < index){
            stringstream ss;
            ss<<"Value must be in [1,";   ss<<n;   ss<<"].";
            throw std::invalid_argument( ss.str() );
        }
        return array[index-1];
    }

    void set(int index, bool value){
        if(index < 1 || n < index){
            stringstream ss;
            ss<<"Value must be in [1,";   ss<<n;   ss<<"].";
            throw std::invalid_argument( ss.str() );
        }
        array[index-1] = value;
    }
};