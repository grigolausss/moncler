import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SkuDetail from './pages/SkuDetail';
import Stores from './pages/Stores';
import Search from './pages/Search';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stores/:city" element={<Stores />} />
          <Route path="/search" element={<Search />} />
          <Route path="/:city/:sku" element={<SkuDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
