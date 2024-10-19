from starlette.testclient import TestClient


def test_read_products_success(client: TestClient) -> None:
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_products_with_filter(client: TestClient) -> None:
    response = client.get("/products?min_price=60")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_products_no_data(client: TestClient) -> None:
    response = client.get("/products?min_price=1000")
    assert response.status_code == 200
    assert response.json() == []


def test_read_products_invalid_min_price(client: TestClient) -> None:
    response = client.get("/products?min_price=-1000")
    assert response.status_code == 422


def test_read_products_invalid_max_price(client: TestClient) -> None:
    response = client.get("/products?max_price=-1000")
    assert response.status_code == 422


def test_read_products_invalid_min_in_stock(client: TestClient) -> None:
    response = client.get("/products?min_in_stock=-1000")
    assert response.status_code == 422


def test_read_products_invalid_max_in_stock(client: TestClient) -> None:
    response = client.get("/products?max_in_stock=-1000")
    assert response.status_code == 422


def test_read_products_invalid_skip(client: TestClient) -> None:
    response = client.get("/products?skip=-1000")
    assert response.status_code == 422


def test_read_products_invalid_limit(client: TestClient) -> None:
    response = client.get("/products?limit=-1000")
    assert response.status_code == 422
