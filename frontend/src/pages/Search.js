import React, { useState } from 'react';
import { searchAvailability } from '../services/api';
import './Search.css';

const Search = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    const terms = searchTerm.trim().split(' ');
    if (terms.length < 2) {
      setError("Please enter SKU and Size separated by a space (e.g., MON123 2)");
      setResults([]);
      return;
    }

    const sku = terms[0];
    const size = terms.slice(1).join(' '); // Handle sizes that might have spaces, though unlikely

    setLoading(true);
    setError(null);
    try {
      const data = await searchAvailability(sku, size);
      setResults(data);
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <h1>Ricerca Disponibilità</h1>
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Cerca SKU + Taglia (es. MON123 2)"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button" disabled={loading}>
          {loading ? 'Searching...' : 'Cerca'}
        </button>
      </form>

      <div className="search-results">
        {error && <p className="error-message">{error}</p>}
        {loading && <p>Loading results...</p>}
        {!loading && !error && results.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Store</th>
                <th>Città</th>
                <th>Disponibilità</th>
                <th>Telefono</th>
              </tr>
            </thead>
            <tbody>
              {results.map(r => (
                <tr key={r.store_id}>
                  <td>{r.store_name}</td>
                  <td>{r.city_name}</td>
                  <td>{r.availability}</td>
                  <td><a href={`tel:${r.phone}`}>{r.phone}</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {!loading && !error && results.length === 0 && searchTerm && <p>Nessun risultato trovato.</p>}
      </div>
    </div>
  );
};

export default Search;
