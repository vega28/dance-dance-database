import { useState } from 'react'
import './App.css'

function FilterableSongTable({ songs }) {
  const [filterText, setFilterText] = useState('');
  const [learnedOnly, setLearnedOnly] = useState(false);

  function SongRow({ song }) {
    return (
      <tr>
        <td>{song.title}</td>
        <td>{song.artist}</td>
        <td>{song.status}</td>
      </tr>
    );
  }

  function SongTable({ songs, filterText, learnedOnly }) {
    const rows = [];

    songs.forEach((song) => {
      if (
        song.title.toLowerCase().indexOf(
          filterText.toLowerCase()
        ) === -1
      ) {
        return;
      }
      if (learnedOnly && song.status != "done") {
        console.log(learnedOnly);
        return;
      }
      rows.push(
        <SongRow
          song={song}
          key={song.title} />
      );
    })

    return (
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Artist</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    );
  }

  function SearchBar({
    filterText,
    learnedOnly,
    onFilterTextChange,
    onLearnedOnlyChange
  }) {
    return (
      <form>
        <input
          id="filterTextbox"
          type="text"
          value={filterText}
          placeholder="search by song title..."
          onChange={(e) => onFilterTextChange(e.target.value)} />
        <label>
          <input
            id="learnedOnlyCheckbox"
            type="checkbox"
            checked={learnedOnly}
            onChange={(e) => onLearnedOnlyChange(e.target.checked)} />
          {' '}
          only show songs that are done and learned
        </label>
      </form>
    );
  }

  return (
    <div>
      <SearchBar
        filterText={filterText}
        learnedOnly={learnedOnly}
        onFilterTextChange={setFilterText}
        onLearnedOnlyChange={setLearnedOnly} />
      <SongTable
        songs={songs}
        filterText={filterText}
        learnedOnly={learnedOnly} />
    </div>
  );
}

export { FilterableSongTable }