from unittest.mock import Mock

from starlette.testclient import TestClient


def test_create_category_success(client: TestClient, mock_uow: Mock) -> None:
    response = client.post("/categories", json={
        "name": "New Category",
    })
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"category_id": 1}


def test_create_category_invalid_data(client: TestClient, mock_uow: Mock) -> None:
    response = client.post("/categories", json={"invalid_field": "Invalid"})
    assert response.status_code == 422


def test_create_category_empty_body(client: TestClient, mock_uow: Mock) -> None:
    response = client.post("/categories", json={})
    assert response.status_code == 422
