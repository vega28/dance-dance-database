import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import dino from './assets/dino.png'
import { FilterableSongTable } from './SongTable.jsx'
import { ArtistTable } from './ArtistTable.jsx'
import './App.css'


function reset() {
  window.location.reload();
}

function App() {
  const [songs, setSongs] = useState([]);
  // songs only need to be fetched once so they don't need to be state...
  const [artists, setArtists] = useState([]);

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

  useEffect(() => {
    fetch('/api/artists')
      .then(res => res.json())
      .then(data => {
        console.log(data);
        setArtists(data);
      })
      .catch((err) => {
        console.log(err.message);
      })
  }, []);

  return (
    <>
      <div className="title-container">
        <a href="https://github.com/vega28/dance-dance-database" target="_blank">
          <img src={dino} className="logo" alt="vega28 logo" />
        </a>
        <h1>dance dance database~</h1>
      </div>
      <p className="read-the-docs">
        Click on the dino to see the github repo!
      </p>
      <div className="table-container">
        <div className="table-card">
          <h2>songs</h2>
          <FilterableSongTable songs={songs} />
        </div>
        <div className="table-card">
          <h2>artists</h2>
          <ArtistTable artists={artists} />
        </div>
      </div>
      <div className="card">
        <button onClick={() => alert('coming soon!')}>
          add new song
        </button>
      </div>
    </>
  )
}

export default App
