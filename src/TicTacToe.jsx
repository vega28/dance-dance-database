import { useState } from 'react'
import './App.css'

function Square({ value, onSquareClick }) {
  return (
    <button
      className="square"
      onClick={onSquareClick}
    >
      {value}
    </button>
  );
}

function reset() {
  window.location.reload();
}

function checkForWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function Board() {
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [turn, setTurn] = useState('x'); // switch every successful click
  const winner = useState(null);

  let status;
  if (checkForWinner(squares)) {
    status = "Winner: " + checkForWinner(squares);
  } else {
    status = "Next player: " + turn;
  }

  function handleClick(i) {
    if (checkForWinner(squares)) {
      alert("game over! " + checkForWinner(squares) + " won!")
    }
    else if (squares[i] === null) {
      const nextSquares = squares.slice();
      nextSquares[i] = turn;
      setSquares(nextSquares);
      if (checkForWinner(nextSquares)) {
        alert("game over! " + checkForWinner(nextSquares) + " won!")
      };
      setTurn(turn === 'x' ? 'o' : 'x');
    }
    else {
      alert("Square already taken!");
    }
  }

  return (
    <div>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
      <button className="reset-button" onClick={() => reset()}>reset game</button>
    </div>
  );
}

export { Board, reset }
