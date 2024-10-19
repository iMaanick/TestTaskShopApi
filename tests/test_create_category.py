
def test_create_category_success(client, mock_uow):
    response = client.post("/categories", json={
        "name": "New Category",
    })
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"category_id": 1}


def test_create_category_invalid_data(client, mock_uow):
    response = client.post("/categories", json={"invalid_field": "Invalid"})
    assert response.status_code == 422


def test_create_category_empty_body(client, mock_uow):
    response = client.post("/categories", json={})
    assert response.status_code == 422
