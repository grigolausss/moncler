import pytest
from backend.app import create_app
from backend.extensions import db

@pytest.fixture
def test_client():
    """Create a test client for the Flask application."""
    config_overrides = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ECHO": False # Turn off SQL logging for cleaner test output
    }
    flask_app = create_app(config_overrides)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            # Note: We would normally seed the test database here.
            # For simplicity, we'll rely on the app's behavior with an empty DB
            # or add specific data within tests.
        yield testing_client

def test_stores_endpoint(test_client):
    """Test the /api/stores/<city> endpoint."""
    # This test assumes an empty database, so it should return 404 for any city.
    response = test_client.get('/api/stores/Milano')
    assert response.status_code == 404

def test_search_endpoint_no_params(test_client):
    """Test the /api/search_availability endpoint with no parameters."""
    response = test_client.get('/api/search_availability')
    assert response.status_code == 400
    json_data = response.get_json()
    assert "SKU and Size parameters are required" in json_data['error']

def test_search_endpoint_not_found(test_client):
    """Test the /api/search_availability endpoint for a non-existent SKU."""
    response = test_client.get('/api/search_availability?sku=FAKE123&size=1')
    assert response.status_code == 404
    json_data = response.get_json()
    assert "SKU 'FAKE123' not found" in json_data['error']

# A more comprehensive test would involve seeding the in-memory database
# with test data and then asserting the responses.
# For example:
# 1. Add a City, Store, Product, Size.
# 2. Add a Stock record.
# 3. Call the search endpoint with the correct SKU/size.
# 4. Assert the response contains the seeded store.
