import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "Welcome to the Bloom Beauty Management System API" in data["message"]

def test_register_user(client):
    new_user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "ph_address": "123 Main St",
        "password": "test_password",
        "telephone": 1234567890,
        "city_town": "Sample City"
    }
    response = client.post('/register', json=new_user_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "message" in data
    assert "access_token" in data

def test_login_user(client):
    login_data = {
        "username": "johndoe",
        "password": "test_password"
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data

def test_get_user_profile(client):
    response = client.get('/profile/1')  # Assuming 1 is the ID of the user created during registration
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "first_name" in data
    assert "last_name" in data
    assert "username" in data
    assert "email" in data

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_product(client):
    new_product_data = {
        "image": "product_image_url",
        "p_name": "Product Name",
        "description": "Product description",
        "price": 99.99,
        "category": "Sample Category",
        "brand": "Sample Brand"
    }
    response = client.post('/products', json=new_product_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data
    assert "p_name" in data
    assert "description" in data
    assert "price" in data


if __name__ == "__main__":
    pytest.main()
