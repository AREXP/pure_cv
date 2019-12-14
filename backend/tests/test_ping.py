


async def test_ping(test_client):
    resp = await test_client.get('/ping')
    assert resp.status == 200
    text = await resp.text()
    assert text == 'pong'
