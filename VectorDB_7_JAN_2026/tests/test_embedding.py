def test_get_embedding(mocker):
    mocker.patch(
        "app.embedding.requests.post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"embedding": [0.1] * 768}
        )
    )

    from app.embedding import get_embedding
    emb = get_embedding("test")
    assert len(emb) == 768
