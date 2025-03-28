import os
import pytest
import uuid
from httpx import ASGITransport, AsyncClient
from database.database import Database
from main import app


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]})
    response_data = response.json()
    
    assert response.status_code == 201
    assert response_data["name"] == "Test Product"
    assert response_data["price"] == 10.0


@pytest.mark.asyncio
async def test_get_product_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/products/{uuid.uuid4()}")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # first create a product to retrieve
        create_response = await ac.post("/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]})
        product_id = create_response.json()["id"]
        
        # now retrieve the product
        response = await ac.get(f"/products/{product_id}")
    
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["name"] == "Test Product"
    assert response_data["price"] == 10.0


@pytest.mark.asyncio
async def test_update_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # first create a product to update
        create_response = await ac.post("/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]})
        product_id = create_response.json()["id"]
        
        # now update the product
        update_response = await ac.put(f"/products/{product_id}", json={"name": "Updated Product", "price": 15.0, "tags": ["fitness"]})
    
    response_data = update_response.json()
    assert update_response.status_code == 200
    assert response_data["name"] == "Updated Product"
    assert response_data["price"] == 15.0


@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # first create a product to delete
        create_response = await ac.post("/products", json={"name": "Test Product", "price": 10.0, "tags": ["fitness"]})
        product_id = create_response.json()["id"]
        
        # now delete the product
        delete_response = await ac.delete(f"/products/{product_id}")
        get_response = await ac.get(f"/products/{product_id}")

    
    assert delete_response.status_code == 204

    # verify that the product has been deleted
    assert get_response.status_code == 404
