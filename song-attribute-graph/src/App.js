import React, { useState } from "react";
import SongInputScreen from "./components/SongInputScreen";
import ParameterSelectionScreen from "./components/ParameterSelectionScreen";
import VisualizationScreen from "./components/VisualizationScreen";

const App = () => {
  const [songName, setSongName] = useState(""); 
  const [selectedAttrs, setSelectedAttrs] = useState({ x: "", y: "" });
  const [attributes, setAttributes] = useState(null);
  const [currentScreen, setCurrentScreen] = useState(0);

  const fetchSongAttributes = async () => {
    const apiData = {
      danceability: Math.random(),
      acousticness: Math.random(),
      instrumentalness: Math.random(),
      liveness: Math.random(),
      mode: Math.random(),
      speechiness: Math.random(),
      tempo: Math.random(),
      valence: Math.random(),
      spectral_contrast: Math.random(),
      chroma_mean: Math.random(),
      mfecs_mean: Math.random(),
      spectral_contrast_std: Math.random(),
      chroma_std: Math.random(),
      mfecs_std: Math.random(),
    };
    setAttributes(apiData);
    setCurrentScreen(1); // Move to the next screen
  };

  const handleAttrSelection = (e) => {
    setSelectedAttrs({ ...selectedAttrs, [e.target.name]: e.target.value });
  };

  return (
    <div>
      {currentScreen === 0 && (
        <SongInputScreen
          songName={songName}
          setSongName={setSongName}
          fetchSongAttributes={fetchSongAttributes}
        />
      )}
      {currentScreen === 1 && (
        <ParameterSelectionScreen
          attributes={attributes}
          selectedAttrs={selectedAttrs}
          setCurrentScreen={setCurrentScreen}
          handleAttrSelection={handleAttrSelection}
        />
      )}
      {currentScreen === 2 && (
        <VisualizationScreen
          songName={songName} // Pass the songName to display it
          attributes={attributes}
          selectedAttrs={selectedAttrs}
          setCurrentScreen={setCurrentScreen}
        />
      )}
    </div>
  );
};

export default App;
