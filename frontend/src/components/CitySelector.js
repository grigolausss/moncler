import React from 'react';
import './CitySelector.css';

const CitySelector = ({ cities, selectedCity, onSelect }) => {

  const handleSelection = (e) => {
    onSelect(e.target.value);
  };

  return (
    <div className="city-selector">
      <select value={selectedCity} onChange={handleSelection} className="city-dropdown">
        {cities.map(city => (
          <option key={city.id} value={city.name}>
            {city.name}
          </option>
        ))}
      </select>
      {/* "Add another" button will go here */}
    </div>
  );
};

export default CitySelector;
