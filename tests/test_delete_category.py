from unittest.mock import Mock

from starlette.testclient import TestClient


def test_delete_category_success(client: TestClient, mock_uow: Mock) -> None:
    response = client.delete("/categories/1")
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Category 1",
        "description": None
    }


def test_delete_category_not_found(client: TestClient) -> None:
    response = client.delete("/categories/999")
    assert response.status_code == 404


def test_delete_category_invalid_data(client: TestClient) -> None:
    response = client.delete("/categories/gffg")
    assert response.status_code == 422
