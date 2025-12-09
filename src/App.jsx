import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'


function reset() {
  window.location.reload();
}

function App() {
  const [count, setCount] = useState(0)
  const [currentTime, setCurrentTime] = useState(0);
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    fetch('/api/time')
      .then(res => res.json())
      .then(data => {
        setCurrentTime(data.time);
      });
  }, []);

  function getSongs() {
    return (
      fetch('/api/songs')
        .then(res => res.json())
        .then(data => {
          console.log(data);
          setSongs(data);
        })
        .catch((err) => {
          console.log(err.message);
        })
    );
  };

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <h2>flask api demo</h2>
      <div className="card">
        <p>Current time is {new Date(currentTime).toLocaleString()}. (...maybe not)</p>
      </div>
      <div>
        <h3>songs!</h3>
        <button className="square" onClick={() => getSongs()}>get songs</button>
        <div>
          {songs.map((song) => {
            return (
              <div key={song.id}>
                <p>{song.title} by {song.artist}</p>
              </div>
            )
          })}
        </div>
        <button className="reset-button" onClick={() => reset()}>reset</button>
      </div>
    </>
  )
}

export default App
