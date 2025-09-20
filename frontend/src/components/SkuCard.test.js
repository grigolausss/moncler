import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import SkuCard from './SkuCard';

test('renders SkuCard with correct data and status color', () => {
  const mockSku = {
    id: 1,
    name: "Giacca Test",
    color: "Rosso",
    sku: "TEST123",
    status_color: "red",
    availability_text: "1/10 available",
    last_updated: new Date().toISOString()
  };

  render(
    <Router>
      <SkuCard city="TestCity" sku={mockSku} />
    </Router>
  );

  // Check for product name, color, and SKU
  expect(screen.getByText('Giacca Test')).toBeInTheDocument();
  expect(screen.getByText('Rosso')).toBeInTheDocument();
  expect(screen.getByText(/SKU: TEST123/i)).toBeInTheDocument();

  // Check for availability text
  expect(screen.getByText('1/10 available')).toBeInTheDocument();

  // Check if the status light has the correct class
  const statusLight = screen.getByText('', { selector: '.status-light' });
  expect(statusLight).toHaveClass('red');
});
