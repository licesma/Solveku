// HTML Elements
const statusDiv = document.querySelector('.status');
const resetDiv = document.querySelector('.reset');
const cellDivs = document.querySelectorAll('.cell');
const candidateDivs = document.querySelectorAll('.candidate');
var selectedCell = null ;
// game constants
const xSymbol = '×';
const oSymbol = '○';

// game variables
let gameIsLive = true;
let xIsNext = true;

window.onload = function(){
  document.addEventListener("keydown", keyPush);
}

// functions
const letterToSymbol = (letter) => letter === 'x' ? xSymbol : oSymbol;

const handleWin = (letter) => {
  gameIsLive = false;
  if (letter === 'x') {
    statusDiv.innerHTML = `${letterToSymbol(letter)} has won!`;
  } else {
    statusDiv.innerHTML = `<span>${letterToSymbol(letter)} has won!</span>`;
  }
};

const checkGameStatus = () => {
  const topLeft = cellDivs[0].classList[1];
  const topMiddle = cellDivs[1].classList[1];
  const topRight = cellDivs[2].classList[1];
  const middleLeft = cellDivs[3].classList[1];
  const middleMiddle = cellDivs[4].classList[1];
  const middleRight = cellDivs[5].classList[1];
  const bottomLeft = cellDivs[6].classList[1];
  const bottomMiddle = cellDivs[7].classList[1];
  const bottomRight = cellDivs[8].classList[1];

  // check winner
  if (topLeft && topLeft === topMiddle && topLeft === topRight) {
    handleWin(topLeft);
    cellDivs[0].classList.add('won');
    cellDivs[1].classList.add('won');
    cellDivs[2].classList.add('won');
  } else if (middleLeft && middleLeft === middleMiddle && middleLeft === middleRight) {
    handleWin(middleLeft);
    cellDivs[3].classList.add('won');
    cellDivs[4].classList.add('won');
    cellDivs[5].classList.add('won');
  } else if (bottomLeft && bottomLeft === bottomMiddle && bottomLeft === bottomRight) {
    handleWin(bottomLeft);
    cellDivs[6].classList.add('won');
    cellDivs[7].classList.add('won');
    cellDivs[8].classList.add('won');
  } else if (topLeft && topLeft === middleLeft && topLeft === bottomLeft) {
    handleWin(topLeft);
    cellDivs[0].classList.add('won');
    cellDivs[3].classList.add('won');
    cellDivs[6].classList.add('won');
  } else if (topMiddle && topMiddle === middleMiddle && topMiddle === bottomMiddle) {
    handleWin(topMiddle);
    cellDivs[1].classList.add('won');
    cellDivs[4].classList.add('won');
    cellDivs[7].classList.add('won');
  } else if (topRight && topRight === middleRight && topRight === bottomRight) {
    handleWin(topRight);
    cellDivs[2].classList.add('won');
    cellDivs[5].classList.add('won');
    cellDivs[8].classList.add('won');
  } else if (topLeft && topLeft === middleMiddle && topLeft === bottomRight) {
    handleWin(topLeft);
    cellDivs[0].classList.add('won');
    cellDivs[4].classList.add('won');
    cellDivs[8].classList.add('won');
  } else if (topRight && topRight === middleMiddle && topRight === bottomLeft) {
    handleWin(topRight);
    cellDivs[2].classList.add('won');
    cellDivs[4].classList.add('won');
    cellDivs[6].classList.add('won');
  } else if (topLeft && topMiddle && topRight && middleLeft && middleMiddle && middleRight && bottomLeft && bottomMiddle && bottomRight) {
    gameIsLive = false;
    statusDiv.innerHTML = 'Game is tied!';
  } else {
    xIsNext = !xIsNext;
    if (xIsNext) {
      statusDiv.innerHTML = `${xSymbol} is next`;
    } else {
      statusDiv.innerHTML = `<span>${oSymbol} is next</span>`;
    }
  }
};


// event Handlers
const colorClear = (newCell) => {
  selectedCell = newCell;
};
const handleReset = () => {
  let mat = [];
  for(let i=0; i<9; i++) {
    mat[i] = new Array(9).fill(0);
  }
  let index;

  for(index = 0; index < 81; index++){
    if(!Number.isNaN(parseInt(cellDivs[index].innerHTML))) {
      mat[rowOf(index)][colOf(index)] = parseInt(cellDivs[index].innerHTML);
    }
  }
  let sudo = new  SudokuGrid(mat, 9);
  sudo.solve();
  let row, col;
  let str;
  for(row = 0; row < 9; row++){
    str = "";
    for(col = 0; col < 9; col++){
      let gridCell = sudo.grid[row][col];
      if(gridCell.hasValue()){
        if(!gridCell.fixed) {
          cellDivs[indexOf(row, col)].innerHTML = sudo.grid[row][col].value;
          cellDivs[indexOf(row, col)].style.color = 'blue';
        }
      }
      else{
        let cellNumber = indexOf(row,col), k;
        //console.log(boxN*9 + 3*(row%3) + col%3)
        let cell =  cellDivs[cellNumber];
        cell.style.visibility = "hidden";
        let candidate;
        for(k = 1; k <= 9; k++){
          if(!gridCell.avSet.has(k)){
            candidate = candidateDivs[9* cellNumber + k-1];
            candidate.style.visibility = "hidden";
          }
        }
        str += "0";
      }
    }

  }
  //console.log(sudo.boxIndexes(1,1)[6]);
};
let changeSelectedCell = (newCell)=>{
  if(selectedCell != null){
    selectedCell.style.backgroundColor = "#D1DDE5";
  }
  if(newCell == selectedCell){
    selectedCell = null
  }
  else{
    selectedCell = newCell;
    selectedCell.style.backgroundColor = "#52BBF7";
//  selectedCell.style.visibility = "hidden";
  }
}
const handleCellClick = (e) => {
  let newCell = e.target;
  changeSelectedCell(newCell);
};
function keyPush(key){
  const keyCode = key.keyCode;
  if(37 <= keyCode && keyCode <= 40){
    let index = selectedIndex();
    let row = rowOf(index), col = colOf(index);
    switch (keyCode) {
            case 37: //left arrow
              col = col-1;
              if(col < 0){
                col = 8;
              }
              break;
            case 38://up arrow
              row = (row-1);
              if(row < 0){
                row = 8;
              }
              break;
            case 39://right arrow
              col = (col+1);
              if(8 < col){
                col = 0;
              }
              break;
            case 40://down arrow
              row = (row+1)%9;
              if(8 < row){
                row = 0;
              }
              break;
    }
    let newCell = cellDivs[indexOf(row,col)];
    changeSelectedCell(newCell);
  }
  if(49 <= keyCode && keyCode <= 57){
    if(selectedCell != null){

      selectedCell.innerHTML = String.fromCharCode(keyCode);
    //const classList = selectedCell.classList;
    //let text = "n" + String.fromCharCode(keyCode);
    //classList.remove(classList.item(1));
    //classList.add(text);
    checkGameStatus();
  }
  }
  else if(keyCode == 32 ){
    if(selectedCell != null){
      selectedCell.innerHTML = '';
  }
}
}



// event listeners
resetDiv.addEventListener('click', handleReset);

for (const cellDiv of cellDivs) {
  cellDiv.addEventListener('click', handleCellClick);
}
let selectedIndex = () => {
  for (let i = 0; i < 81; i++) {
    let c = cellDivs[i];
    if (c == selectedCell) {
      return i;
    }
  }
    return -1;

}
let boxOf = (row, col) => 3*Math.floor(row/3) + Math.floor(col/3);
let indexOf = (row,col) => boxOf(row,col)*9 + 3*(row%3) + col%3
let boxInGrid = (index) => Math.floor(index/9);
let cellInBox = index => index%9;
let rowOf = (index) => Math.floor(cellInBox(index)/3)+ 3*Math.floor(boxInGrid(index)/3);
let colOf = (index) => cellInBox(index)%3 + 3*(boxInGrid(index)%3);
class SudokuCell{
  constructor() {
    this.value = 0;
    this.fixed = false;
    this.avSet = null;
  }
  hasValue() {
    return this.value !== 0;
  }
  safeAvSetRemove(num){
    if(!this.hasValue() && this.avSet.has(num)){
      this.avSet.delete(num);
    }
  }
}

class BracketImage{
  constructor(n) {
    this.allBrackets = new Array(3*n);
    this.row = new Array(n);
    this.col = new Array(n);
    this.box = new Array(n);
    for(let i = 0; i < 3*n; i++){
      this.allBrackets[i] = new Set();
    }
    for(let i = 0; i < n; i++){
      this.row[i] = this.allBrackets[i];
      this.col[i] = this.allBrackets[n+i];
      this.box[i] = this.allBrackets[2*n+i];
    }
  }
}

class SudokuGrid{
  boxOf(row, col){
    return 3*Math.floor(row/3) + Math.floor(col/3);
  }
  boxIndexes(row, col){
    let res = new Array();
    let root = Math.floor(Math.sqrt(this.n)), startRow = root*Math.floor(row/root), startCol = root*Math.floor(col/root);
    for(let i = 0; i < 3; i++){
      for(let j =0; j < 3; j++){
        res.push([startRow+i, startCol+j]);
      }
    }
    return res;
  }
  fillBracketImages(){
    this.images = new BracketImage(this.n);
    let row, col;
    let cell;
    for(row = 0; row < 9; row++){
      for(col = 0; col < 9; col++){
        cell = this.grid[row][col];
        if(cell.hasValue()){
          if(this.images.row[row].has(cell.value) || this.images.col[col].has(cell.value) || this.images.box[this.boxOf(row, col)].has(cell.value)) {
            throw "Group constraint violated";
          }
          else{
            this.images.row[row].add(cell.value);
            this.images.col[col].add(cell.value);
            this.images.box[this.boxOf(row, col)].add(cell.value);
          }
        }
      }
    }
  }
  defineAvailableSets(){
    let row, col, val;
    let cell;
    for(row = 0; row < this.n; row++){
      for(col = 0; col < this.n; col++){
        cell = this.grid[row][col];
        if(!cell.hasValue()){
          for(val = 0; val <= this.n; val++){
            if(this.images.row[row].has(val) || this.images.col[col].has(val) || this.images.box[this.boxOf(row,col)].has(val)){
              cell.avSet.delete(val);
            }
          }
        }
      }
    }
  }
  updateNeighborsAvailableSet(row, col, num){
    let boxIdx = this.boxIndexes(row,col);
    for(let it = 0; it < this.n; it++){
      this.grid[row][it].safeAvSetRemove(num);
      this.grid[it][col].safeAvSetRemove(num);
      this.grid[boxIdx[it][0]][boxIdx[it][1]].safeAvSetRemove(num);
    }
}
  updateCell(row, col, num){
    this.grid[row][col].value = num;
    this.grid[row][col].avSet = null;
    this.images.row[row].add(num);
    this.images.col[col].add(num);
    this.images.box[this.boxOf(row,col)].add(num);
    this.updateNeighborsAvailableSet(row,col,num);
  }

  stageOne(){
    let affectedCells = false;
    let row, col;
    for(row in this.I){
      for(col in this.I){
        let cell = this.grid[row][col];
        if(!cell.hasValue() && cell.avSet.size === 1){
          affectedCells = true;
          let [num] = cell.avSet;
          this.updateCell(row, col, num);
        }
      }
    }
    if(affectedCells){
      this.stageOne();
    }
  }
  solve(){
    this.stageOne();
  }
  constructor(numberGrid, n){
    this.n = n;
    this.I = Array.from(Array(n).keys())
    this.Omega = Array.from({length: n}, (_, i) => i + 1)
    this.grid = new Array(9);
    for(let i=0; i<9; i++) {
      this.grid[i] = new Array(9);
      for(let j = 0; j < 9; j++){
        this.grid[i][j] = new SudokuCell();
      }
    }
    let i, j, value;
    for(i = 0; i < this.n; i++){
      for(j = 0; j < this.n; j++){
        value = numberGrid[i][j];
        if(value !== 0){
          this.grid[i][j].value = value;
          this.grid[i][j].fixed = true;
        }
        else{
          this.grid[i][j].avSet = new Set();
          for(let k = 1; k <= n; k++){
            this.grid[i][j].avSet.add(k);
          }
        }
      }
    }
    this.fillBracketImages();
    this.defineAvailableSets();

  }
}
