def test_read_categories_success(client):
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_categories_pagination(client):
    response = client.get("/categories?skip=1&limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_categories_no_data(client):
    response = client.get("/categories?skip=10")
    assert response.status_code == 200
    assert response.json() == []


def test_read_categories_invalid_param_skip(client):
    response = client.get("/categories?skip=-1")
    assert response.status_code == 422


def test_read_categories_invalid_param_limit(client):
    response = client.get("/categories?limit=-1")
    assert response.status_code == 422
