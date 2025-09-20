import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getStoresByCity } from '../services/api';
import './Stores.css';

const Stores = () => {
  const { city } = useParams();
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStores = async () => {
      setLoading(true);
      try {
        const data = await getStoresByCity(city);
        setStores(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (city) {
      fetchStores();
    }
  }, [city]);

  if (loading) return <p>Loading stores...</p>;
  if (error) return <p className="error-message">Error: {error}</p>;

  return (
    <div className="stores-page">
      <h1>Stores in {city}</h1>
      <div className="stores-list">
        {stores.map(store => (
          <div key={store.id} className="store-card">
            <div className="store-header">
                <h3>{store.name}</h3>
                {store.is_open_now && <span className="open-chip">Aperto ora</span>}
            </div>
            <p><strong>Telefono:</strong> <a href={`tel:${store.phone}`}>{store.phone || 'n/d'}</a></p>
            <div className="opening-hours">
                <strong>Orari:</strong>
                <ul>
                    {store.opening_hours ? Object.entries(store.opening_hours).map(([day, time]) => (
                        <li key={day}><span>{day}:</span> {time}</li>
                    )) : <li>n/d</li>}
                </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Stores;
