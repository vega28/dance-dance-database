import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import dino from './assets/dino.png'
import { FilterableSongTable } from './SongTable.jsx'
import './App.css'


function reset() {
  window.location.reload();
}

function App() {
  const [songs, setSongs] = useState([]);
  // songs only need to be fetched once so they don't need to be state...

  useEffect(() => {
    fetch('/api/songs')
      .then(res => res.json())
      .then(data => {
        console.log(data);
        setSongs(data);
      })
      .catch((err) => {
        console.log(err.message);
      })
  }, []);

  return (
    <>
      <div>
        <a href="https://github.com/vega28/dance-dance-database" target="_blank">
          <img src={dino} className="logo" alt="vega28 logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <p className="read-the-docs">
        Click on the dino and React logos to learn more!
      </p>
      <h1>dance dance database~</h1>
      <div className="card">
        <button onClick={() => alert('coming soon!')}>
          add new song
        </button>
      </div>
      <div className="card">
        <h2>songs!</h2>
        <FilterableSongTable songs={songs} />
      </div>
    </>
  )
}

export default App
