import pytest
import uuid
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_create_product(client):
    response = client.post(
        "/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]}
    )
    response_data = response.json()

    assert response.status_code == 201
    assert response_data["name"] == "Test Product"
    assert response_data["price"] == 10.0


def test_get_product_not_found(client):
    response = client.get(f"/products/{uuid.uuid4()}")
    assert response.status_code == 404


def test_get_product(client):
    # first create a product to retrieve
    create_response = client.post(
        "/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]}
    )
    product_id = create_response.json()["id"]

    # now retrieve the product
    response = client.get(f"/products/{product_id}")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == "Test Product"
    assert response_data["price"] == 10.0


def test_update_product(client):
    # first create a product to update
    create_response = client.post(
        "/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]}
    )
    product_id = create_response.json()["id"]

    # now update the product
    update_response = client.put(
        f"/products/{product_id}",
        json={"name": "Updated Product", "price": 15.0, "tags": ["fitness"]},
    )

    response_data = update_response.json()
    assert update_response.status_code == 200
    assert response_data["name"] == "Updated Product"
    assert response_data["price"] == 15.0


def test_delete_product(client):
    # first create a product to delete
    create_response = client.post(
        "/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]}
    )
    product_id = create_response.json()["id"]

    # now delete the product
    delete_response = client.delete(f"/products/{product_id}")
    get_response = client.get(f"/products/{product_id}")

    assert delete_response.status_code == 204

    # verify that the product has been deleted
    assert get_response.status_code == 404
