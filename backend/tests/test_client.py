# def test_home(test_client):
#     response = test_client.get("/")

#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello Fast_API 🚀"}


def test_health(test_client):
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
