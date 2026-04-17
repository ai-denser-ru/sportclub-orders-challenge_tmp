"""Integration tests for API endpoints."""

def test_get_orders_returns_200(client):
    response = client.get("/api/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
