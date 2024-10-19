def test_update_category_success(client, mock_uow):
    response = client.put("/categories/1", json={"name": "Updated Category"})
    mock_uow.commit.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Category 1",
        "description": None
    }


def test_update_category_not_found(client, mock_uow):
    response = client.put("/categories/999", json={"name": "Non-existent"})
    assert response.status_code == 404


def test_update_category_invalid_data(client, mock_uow):
    response = client.put("/categories/1", json={"invalid_field": "Invalid"})
    assert response.status_code == 422


def test_update_category_invalid_category_id(client, mock_uow):
    response = client.put("/categories/gf", json={"invalid_field": "Invalid"})
    assert response.status_code == 422
