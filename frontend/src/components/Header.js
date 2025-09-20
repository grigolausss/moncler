import React from 'react';
import { Link } from 'react-router-dom';
import CitySelector from './CitySelector';
import './Header.css';

const Header = ({ cities, currentCity, onCityChange }) => {
  return (
    <header className="app-header">
      <div className="logo-container">
        <h1>Moncler Stock</h1>
      </div>
      <nav className="main-nav">
        <CitySelector
          cities={cities}
          selectedCity={currentCity}
          onSelect={onCityChange}
        />
        <Link to={`/stores/${currentCity}`} className="nav-link">Negozi</Link>
        <Link to="/search" className="nav-link">Ricerca</Link>
      </nav>
    </header>
  );
};

export default Header;
