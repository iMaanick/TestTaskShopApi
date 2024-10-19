from starlette.testclient import TestClient


def test_read_category_success(client: TestClient) -> None:
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Category 1",
        "description": None
    }


def test_read_category_not_found(client: TestClient) -> None:
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_read_category_invalid_data(client: TestClient) -> None:
    response = client.get("/categories/gffg")
    assert response.status_code == 422
