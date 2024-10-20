import React from "react";
import "./ParameterSelectionScreen.css";

const ParameterSelectionScreen = ({
  attributes,
  selectedAttrs,
  setCurrentScreen,
  handleAttrSelection,
}) => {
  return (
    <div className="parameter-selection-container">
      <h2>Select Attributes to Graph</h2>
      <select name="x" onChange={handleAttrSelection}>
        <option value="">Select X-Axis Attribute</option>
        {Object.keys(attributes).map((attr, i) => (
          <option key={i} value={attr}>
            {attr}
          </option>
        ))}
      </select>
      <select name="y" onChange={handleAttrSelection}>
        <option value="">Select Y-Axis Attribute</option>
        {Object.keys(attributes).map((attr, i) => (
          <option key={i} value={attr}>
            {attr}
          </option>
        ))}
      </select>
      <button onClick={() => setCurrentScreen(2)}>Visualize</button>
      <button onClick={() => setCurrentScreen(0)}>Go Back</button>
    </div>
  );
};

export default ParameterSelectionScreen;
