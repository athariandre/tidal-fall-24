import React, { useState, useEffect } from "react";
import './SongInputScreen.css';

const SongInputScreen = ({ songName, setSongName, fetchSongAttributes }) => {
  const [songList, setSongList] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        const response = await fetch('songs_and_artists.txt');
        const text = await response.text();
        const songs = text.split('\n').map(song => song.trim()).filter(song => song !== '');
        setSongList(songs);
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    };

    fetchSongs();
  }, []);

  const handleSongInputChange = (e) => {
    const query = e.target.value;
    setSongName(query);

    if (query.length > 1) {
      const filtered = songList.filter((song) =>
        song.toLowerCase().includes(query.toLowerCase())
      );
      setSuggestions(filtered);
    } else {
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (song) => {
    setSongName(song);
    setSuggestions([]);
  };

return (
    <div className="song-input-container" style={{ marginLeft: '10px' }}>
        <h2>Type the name of the song</h2>
        <input
            type="text"
            placeholder="Song Name"
            value={songName}
            onChange={handleSongInputChange}
        />

        {suggestions.length > 0 && (
            <ul className="suggestions-list">
                {suggestions.slice(0, 10).map((song, index) => (
                    <li
                        key={index}
                        onClick={() => handleSuggestionClick(song)}
                        className="suggestion-item"
                        style={{ listStyleType: 'none' }}
                    >
                        <span role="img" aria-label="musical note">🎵</span> {song}
                    </li>
                ))}
            </ul>
        )}

        <button onClick={fetchSongAttributes} disabled={!songName}>
            Next
        </button>
    </div>
);
};



export default SongInputScreen;
