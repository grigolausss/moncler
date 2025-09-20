import React from 'react';
import { useParams } from 'react-router-dom';

const SkuDetail = () => {
  const { city, sku } = useParams();

  // In the next steps, we will use these params to fetch detailed data.

  return (
    <div className="sku-detail-page">
      <header className="detail-header">
        <h1>SKU Details</h1>
        <p>Showing details for SKU: <strong>{sku}</strong> in <strong>{city}</strong></p>
      </header>

      <div className="detail-content">
        <section className="size-quantity-section">
          <h2>Availability by Size</h2>
          {/* Size and quantity list will go here */}
          <p>Loading sizes...</p>
        </section>

        <section className="history-chart-section">
          <h2>Stock History</h2>
          {/* Recharts graph will go here */}
          <p>Loading chart...</p>
        </section>

        <section className="event-log-section">
          <h2>Event History</h2>
          {/* Event log will go here */}
          <p>Loading events...</p>
        </section>
      </div>
    </div>
  );
};

export default SkuDetail;
