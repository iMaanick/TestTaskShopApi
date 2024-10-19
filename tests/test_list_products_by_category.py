from starlette.testclient import TestClient


def test_list_products_by_category_success(client: TestClient) -> None:
    response = client.get("/categories/1/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Product 1"
    assert data[1]["name"] == "Product 2"


def test_list_products_by_category_single_product(client: TestClient) -> None:
    response = client.get("/categories/2/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Product 3"


def test_list_products_by_category_empty(client: TestClient) -> None:
    response = client.get("/categories/3/products")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products_by_category_not_found(client: TestClient) -> None:
    response = client.get("/categories/666/products")
    assert response.status_code == 404


def test_list_products_by_category_invalid_id(client: TestClient) -> None:
    response = client.get("/categories/invalid/products")
    assert response.status_code == 422
