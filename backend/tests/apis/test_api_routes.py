def test_get_all_folder_colors(test_client):
    response = test_client.get("/fol_color")

    print(response.json())

    assert response.status_code == 404
    # assert response.json() == {"msg": "Hello Fast_API 🚀"}


# def test_get_folder_colors(test_client):
#     response = test_client.get("/health")

#     assert response.status_code == 200
#     assert response.json() == {"status": "OK"}
