from starlette.testclient import TestClient


def test_get_product_by_id_success(client: TestClient) -> None:
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_product_by_id_not_found(client: TestClient) -> None:
    response = client.get("/products/999")
    assert response.status_code == 404


def test_get_product_by_id_invalid_id(client: TestClient) -> None:
    response = client.get("/products/fgvfg")
    assert response.status_code == 422
