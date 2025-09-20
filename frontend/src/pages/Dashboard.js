import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import SkuList from '../components/SkuList';
import { getCities, getSkuStatusByCity } from '../services/api';

function Dashboard() {
  const [cities, setCities] = useState([]);
  const [currentCity, setCurrentCity] = useState('Cortina'); // Default city
  const [skuData, setSkuData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        // Fetch cities only once or when needed
        if (cities.length === 0) {
            const citiesData = await getCities();
            setCities(citiesData);
        }

        const initialSkuData = await getSkuStatusByCity(currentCity);
        setSkuData(initialSkuData);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, [currentCity]); // Re-fetch SKU data when currentCity changes

  const handleCityChange = (cityName) => {
    setCurrentCity(cityName);
  };

  return (
    <>
      <Header
        cities={cities}
        currentCity={currentCity}
        onCityChange={handleCityChange}
      />
      <main>
        {loading && <p>Loading data...</p>}
        {error && <p className="error-message">Error: {error}</p>}
        {!loading && !error && <SkuList city={currentCity} skuData={skuData} />}
      </main>
    </>
  );
}

export default Dashboard;
