import React, { useEffect, useRef, useState } from "react";
import { Scatter } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import './VisualizationScreen.css';

ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend);

const VisualizationScreen = ({ attributes, selectedAttrs, setCurrentScreen, songName }) => {
  const chartRef = useRef(null);
  const [songsData, setSongsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSong, setSelectedSong] = useState(null); // State for the selected song

  const fetchSongsData = async () => {
    const apiUrl = 'http://localhost:5000/similar_songs'; // Replace with your actual API URL
    const payload = {
      query: songName,
      n: 5, // Number of similar songs to retrieve
    };

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      console.log(response);
      if (!response.ok) {
        throw new Error('Failed to fetch song data');
      }

      const fetchedSongs = await response.json();
      const [originalSong, ...similarSongs] = fetchedSongs;

      setSelectedSong(originalSong);
      setSongsData(similarSongs);
    } catch (error) {
      console.error("Error fetching song data:", error);
    }
  };

  useEffect(() => {
    const getData = async () => {
      setLoading(true);
      await fetchSongsData(); // Call the API
      setLoading(false);
    };

    getData();

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [songName]); // Re-fetch if songName changes

  // Construct the data for the chart
  const graphData = {
    datasets: [
      {
        label: "Selected Song",
        data: selectedSong
          ? [
              {
                x: selectedSong[selectedAttrs.x],
                y: selectedSong[selectedAttrs.y],
                name: selectedSong.name, // Tooltip label for the selected song
              },
            ]
          : [],
        backgroundColor: "rgba(255, 99, 132, 0.5)",
        pointRadius: 10, // Larger point for the selected song
      },
      {
        label: "Other Songs",
        data: songsData.map((song) => ({
          x: song[selectedAttrs.x], // Use actual x-value for other songs
          y: song[selectedAttrs.y], // Use actual y-value for other songs
          name: song.name, // Tooltip label for each song
        })),
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        pointRadius: 5, // Smaller points for the other songs
      },
      {
        label: "Connections",
        data: selectedSong
          ? songsData.flatMap((song) => [
              {
                x: selectedSong[selectedAttrs.x],
                y: selectedSong[selectedAttrs.y],
              },
              {
                x: song[selectedAttrs.x],
                y: song[selectedAttrs.y],
              },
            ])
          : [],
        borderColor: "rgba(75, 192, 192, 0.6)",
        showLine: true,
        pointRadius: 0, // No points for the line
        fill: false,
      },
    ],
  };

  const options = {
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            const songData = context.raw;
            return `Song: ${songData.name || 'Unknown'}`; // Display the song name in the tooltip
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: selectedAttrs.x,
          color: 'white', // to match your dark theme
          font: {
            size: 16, // adjust as needed
            family: 'Geologica',
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.2)', // Light gray color for better visibility
          lineWidth: 2, // Increase line width
        },
      },
      y: {
        title: {
          display: true,
          text: selectedAttrs.y,
          color: 'white', // to match your dark theme
          font: {
            size: 16, // adjust as needed
            family: 'Geologica',
          },
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.2)', // Light gray color for better visibility
          lineWidth: 2, // Increase line width
        },
      },
    },
  };

  return (
    <div className="visualization-container">
      <h2>Song Attribute Visualization</h2>
      {loading ? (
        <p className="loading-message">Loading song data...</p>
      ) : (
        <div className="chart-container">
          <Scatter ref={chartRef} data={graphData} options={options} />
        </div>
      )}
      <button onClick={() => setCurrentScreen(0)}>Add More Songs</button>
    </div>
  );
};

export default VisualizationScreen;
