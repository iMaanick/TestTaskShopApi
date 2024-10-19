from unittest.mock import Mock

from starlette.testclient import TestClient


def test_create_product_success(client: TestClient, mock_uow: Mock) -> None:
    response = client.post("/products", json={"name": "New Product", "price": 100.0, "in_stock": 10})
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_product_invalid_data(client: TestClient, mock_uow: Mock) -> None:
    response = client.post("/products", json={"name": ""})
    assert response.status_code == 422


def test_create_product_empty_body(client: TestClient, mock_uow: Mock) -> None:
    response = client.post("/products", json={})
    assert response.status_code == 422
