import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import Header from './Header';

test('renders the header with logo and city selector', () => {
  const cities = [{ id: 1, name: 'Milano' }];
  const currentCity = 'Milano';
  const onCityChange = jest.fn();

  render(
    <Router>
      <Header
        cities={cities}
        currentCity={currentCity}
        onCityChange={onCityChange}
      />
    </Router>
  );

  // Check for the main title
  expect(screen.getByText(/Moncler Stock/i)).toBeInTheDocument();

  // Check if the city selector is rendered with the correct city
  expect(screen.getByDisplayValue('Milano')).toBeInTheDocument();
});
