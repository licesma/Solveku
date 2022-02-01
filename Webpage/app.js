// HTML Elements
const statusDiv = document.querySelector('.status');
const resetDiv = document.querySelector('.reset');
const cellDivs = document.querySelectorAll('.cell');
var selectedCell = null ;
// game constants
const xSymbol = '×';
const oSymbol = '○';

// game variables
let gameIsLive = true;
let xIsNext = true;

window.onload = function(){
  console.log("okf");
  document.addEventListener("keypress", keyPush);
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
  for (const cellDiv of cellDivs) {
    const classList = cellDiv.classList;
    if(1 < classList.length){
      cellDiv.classList.remove(classList.item(1));
    }
  }
};
const handleCellClick = (e) => {
  var newCell = e.target;
  if(selectedCell != null){
      selectedCell.style.backgroundColor = "#D1DDE5";
    }
  if(newCell == selectedCell){
    selectedCell = null
  }
  else{
  selectedCell = e.target;
  selectedCell.style.backgroundColor = "#52BBF7";
  }
  return;
};
function keyPush(key){
  const keyCode = key.keyCode;
  if(49 <= keyCode && keyCode <= 57){
    if(selectedCell != null){
    const classList = selectedCell.classList;
    let text = "n" + String.fromCharCode(keyCode);
    classList.remove(classList.item(1));
    classList.add(text);
    checkGameStatus();
  }
  }
  else if(keyCode == 32 ){
    if(selectedCell != null){
    console.log("ok");
    classList = selectedCell.classList
    if(1 < classList.length){
      selectedCell.classList.remove(classList.item(1));
    }
  }
}
}



// event listeners
resetDiv.addEventListener('click', handleReset);

for (const cellDiv of cellDivs) {
  cellDiv.addEventListener('click', handleCellClick);
}
