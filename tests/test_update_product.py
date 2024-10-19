from unittest.mock import Mock

from starlette.testclient import TestClient


def test_update_product_success(client: TestClient, mock_uow: Mock) -> None:
    response = client.put("/products/1", json={"name": "Updated Product", "price": 150.0, "in_stock": 15})
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"


def test_update_product_not_found(client: TestClient, mock_uow: Mock) -> None:
    response = client.put("/products/999", json={"name": "Updated Product", "price": 150.0, "in_stock": 15})
    assert response.status_code == 404


def test_update_invalid_product_id(client: TestClient, mock_uow: Mock) -> None:
    response = client.put("/products/sgrdr", json={"name": "Updated Product", "price": 150.0, "in_stock": 15})
    assert response.status_code == 422


def test_update_category_invalid_data(client: TestClient, mock_uow: Mock) -> None:
    response = client.put("/products/999", json={"invalid_field": "Invalid"})
    assert response.status_code == 422
