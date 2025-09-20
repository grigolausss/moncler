import React from 'react';
import { Link } from 'react-router-dom';
import './SkuCard.css';

const SkuCard = ({ city, sku }) => {
  if (!sku) {
    return null;
  }

  const isOutdated = sku.last_updated && (new Date() - new Date(sku.last_updated)) > 24 * 60 * 60 * 1000;

  return (
    <Link to={`/${city}/${sku.sku}`} className="sku-card-link">
      <div className="sku-card">
        <div className="card-header">
          <h3>{sku.name}</h3>
          <span className="product-color">{sku.color}</span>
        </div>
        <div className="card-body">
          <div className="status-indicator">
            <div className={`status-light ${sku.status_color}`}></div>
            <span className="availability-text">{sku.availability_text}</span>
          </div>
          <div className="sku-info">
            <span>SKU: {sku.sku}</span>
          </div>
        </div>
        <div className="card-footer">
          <span className="timestamp">
            {sku.last_updated ? `Last updated: ${new Date(sku.last_updated).toLocaleString()}` : 'No update data'}
          </span>
          {isOutdated && (
            <span className="outdated-badge">Dati non aggiornati (&gt;24h)</span>
          )}
        </div>
      </div>
    </Link>
  );
};

export default SkuCard;
