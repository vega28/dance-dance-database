import './App.css'

function ArtistTable({ artists }) {

  function ArtistRow({ artist }) {
    return (
      <tr>
        <td>{artist.name}</td>
        {/* <td>{artist.id}</td> */}
        {/* <td>{artist.songs}</td> */}
      </tr>
    );
  }

  const rows = [];

  artists.forEach((artist) => {
    rows.push(
      <ArtistRow
        artist={artist}
        key={artist.name} />
    );
  })

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            {/* <th>Artist ID</th> */}
            {/* <th>Songs</th> */}
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  );
}

export { ArtistTable }