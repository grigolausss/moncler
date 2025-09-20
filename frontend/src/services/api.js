const API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Fetches all cities from the backend.
 * @returns {Promise<Array>} A promise that resolves to an array of city objects.
 */
export const getCities = async () => {
  const response = await fetch(`${API_BASE_URL}/cities`);
  if (!response.ok) {
    throw new Error('Failed to fetch cities');
  }
  return response.json();
};

/**
 * Searches for availability of a given SKU and size.
 * @param {string} sku - The SKU to search for.
 * @param {string} size - The size to search for.
 * @returns {Promise<Array>} A promise that resolves to an array of availability results.
 */
export const searchAvailability = async (sku, size) => {
  const response = await fetch(`${API_BASE_URL}/search_availability?sku=${sku}&size=${size}`);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Search failed');
  }
  return response.json();
};

/**
 * Fetches all stores for a given city.
 * @param {string} cityName - The name of the city.
 * @returns {Promise<Array>} A promise that resolves to an array of store objects.
 */
export const getStoresByCity = async (cityName) => {
  const response = await fetch(`${API_BASE_URL}/stores/${cityName}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch stores for ${cityName}`);
  }
  return response.json();
};

/**
 * Fetches the SKU status for a given city.
 * @param {string} cityName - The name of the city.
 * @returns {Promise<Array>} A promise that resolves to an array of SKU status objects.
 */
export const getSkuStatusByCity = async (cityName) => {
  const response = await fetch(`${API_BASE_URL}/sku_status/${cityName}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch SKU status for ${cityName}`);
  }
  return response.json();
};

/**
 * Adds a new city.
 * @param {string} cityName - The name of the new city.
 * @returns {Promise<Object>} A promise that resolves to the new city object.
 */
export const addCity = async (cityName) => {
    const response = await fetch(`${API_BASE_URL}/cities`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: cityName }),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to add city');
    }
    return response.json();
};

/**
 * Adds a new product (SKU).
 * @param {Object} productData - The data for the new product { sku, name, color }.
 * @returns {Promise<Object>} A promise that resolves to the new product object.
 */
export const addSku = async (productData) => {
    const response = await fetch(`${API_BASE_URL}/products`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(productData),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to add SKU');
    }
    return response.json();
};
