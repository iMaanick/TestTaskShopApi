def test_read_product_success(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_read_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_read_product_invalid_id(client):
    response = client.get("/products/fgvfg")
    assert response.status_code == 422
