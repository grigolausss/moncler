import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_get_cities():
    """Tests the GET /cities endpoint."""
    print("--- Testing GET /api/cities ---")
    try:
        response = requests.get(f"{BASE_URL}/cities")
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_get_sku_status():
    """Tests the GET /sku_status/<city> endpoint."""
    city_name = "Milano"
    print(f"\n--- Testing GET /api/sku_status/{city_name} ---")
    try:
        response = requests.get(f"{BASE_URL}/sku_status/{city_name}")
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def test_add_city():
    """Tests the POST /cities endpoint."""
    new_city = {"name": "Test City"}
    print(f"\n--- Testing POST /api/cities with {new_city} ---")
    try:
        response = requests.post(f"{BASE_URL}/cities", json=new_city)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))

        # Verify it was added
        verify_response = requests.get(f"{BASE_URL}/cities")
        all_cities = [city['name'] for city in verify_response.json()]
        print(f"Verification: 'Test City' in city list? {'Test City' in all_cities}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def add_product(sku, name, color=None):
    """Adds a new product by calling the POST /api/products endpoint."""
    product_data = {"sku": sku, "name": name, "color": color}
    print(f"\n--- Adding new product: {name} ({sku}) ---")
    try:
        response = requests.post(f"{BASE_URL}/products", json=product_data)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
        print(f"Successfully added product '{name}'.")
    except requests.exceptions.RequestException as e:
        # It's common to get a 409 Conflict if the product already exists,
        # which is not necessarily an error in this script's context.
        if e.response and e.response.status_code == 409:
            print(f"Status Code: {e.response.status_code} (Conflict)")
            print("Product with this SKU already exists. Skipping.")
        else:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    # You can run this script to manually add products or test endpoints.

    # Example: Add the "Piumino Maya" that the user was looking for
    add_product(sku="K20911A5360068950", name="Piumino Maya", color="Nero")

    # You can add more products here if you want
    # add_product(sku="XYZ789", name="Another Jacket", color="Blue")

    # --- You can also uncomment the lines below to test other endpoints ---
    # test_get_cities()
    # test_get_sku_status()
    # test_add_city()
