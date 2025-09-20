import React from 'react';
import SkuCard from './SkuCard';
import './SkuList.css';

const SkuList = ({ city, skuData }) => {
  if (!skuData || skuData.length === 0) {
    return (
      <div className="sku-list-container">
        <p>No SKU data available for this city.</p>
      </div>
    );
  }

  return (
    <div className="sku-list-container">
      <div className="sku-list">
        {skuData.map(sku => (
          <SkuCard key={sku.id} city={city} sku={sku} />
        ))}
      </div>
    </div>
  );
};

export default SkuList;
