def test_upsert(client, mocker):
    mocker.patch("app.router.vector.get_embedding", return_value=[0.1] * 768)
    mocker.patch("app.chroma.collection.add")

    res = client.post("/vector/upsert", json={"id": "1", "text": "hello"})
    assert res.status_code == 200
