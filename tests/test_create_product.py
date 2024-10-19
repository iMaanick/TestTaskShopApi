def test_create_product_success(client, mock_uow):
    response = client.post("/products", json={"name": "New Product", "price": 100.0, "in_stock": 10})
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_product_invalid_data(client, mock_uow):
    response = client.post("/products", json={"name": ""})
    assert response.status_code == 422


def test_create_product_empty_body(client, mock_uow):
    response = client.post("/products", json={})
    assert response.status_code == 422
