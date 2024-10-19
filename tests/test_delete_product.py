from unittest.mock import Mock

from starlette.testclient import TestClient


def test_delete_product_success(client: TestClient, mock_uow: Mock) -> None:
    response = client.delete("/products/1")
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_delete_product_not_found(client: TestClient, mock_uow: Mock) -> None:
    response = client.delete("/products/999")
    assert response.status_code == 404


def test_delete_product_invalid_data(client: TestClient) -> None:
    response = client.delete("/products/gffg")
    assert response.status_code == 422
